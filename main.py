import asyncio
import random
import os
import logging
import hashlib
from urllib.parse import quote_plus, urlparse
from typing import Callable, Optional, Set
from playwright.async_api import async_playwright
from playwright_stealth.stealth import Stealth
from fake_useragent import UserAgent
import pymupdf

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

UA = UserAgent()
DOWNLOAD_DIR = "bibliografia_pdf"
MIN_PAGINAS = 50

# Cache global de URLs já testadas (evita testar mesmo PDF 2x)
urls_testadas: Set[str] = set()
hashes_pdfs: Set[str] = set()  # Evita baixar PDFs duplicados

# Níveis de busca: define quantos links PDF tentar
NIVEIS_BUSCA = {
    "rapido": 5,      # Testa 5 PDFs por query
    "moderado": 15,   # Testa 15 PDFs por query
    "completo": 999,  # Testa TODOS os PDFs encontrados (busca exaustiva)
}

LISTA_LIVROS_PADRAO = []


async def configurar_navegador(p):
    browser = await p.chromium.launch(headless=True)
    context = await browser.new_context(
        user_agent=UA.random,
        viewport={"width": 1920, "height": 1080},
        accept_downloads=True,
        ignore_https_errors=True,
    )
    page = await context.new_page()
    await Stealth().apply_stealth_async(page)
    return browser, page


def calcular_hash_pdf(caminho: str) -> str:
    """Calcula hash MD5 do PDF para detectar duplicatas."""
    try:
        with open(caminho, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return ""


def normalizar_url(url: str) -> str:
    """Normaliza URL para comparação (remove query params variáveis)."""
    parsed = urlparse(url)
    # Remove parâmetros de sessão/tracking comuns
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


async def encontrar_links_pdf(page, nivel: str = "moderado", motor: str = "bing") -> list[str]:
    """Extrai todos os links PDF únicos dos resultados do motor de busca."""
    # Extração mais agressiva de links PDF
    links = await page.evaluate("""() => {
        const allLinks = [];
        
        // Verifica se a página está carregada
        if (!document.body) {
            return [];
        }
        
        // 1. Links diretos para PDF
        document.querySelectorAll('a').forEach(a => {
            if (a.href && a.href.match(/\\.pdf(\\?|#|$)/i)) {
                allLinks.push(a.href);
            }
        });
        
        // 2. Links em atributos data-* e onclick
        document.querySelectorAll('[data-url], [data-href], [onclick]').forEach(el => {
            const dataUrl = el.getAttribute('data-url') || el.getAttribute('data-href');
            if (dataUrl && dataUrl.match(/\\.pdf/i)) {
                allLinks.push(dataUrl);
            }
        });
        
        // 3. Procura por URLs em texto (resultados de busca)
        try {
            const pageText = document.body ? document.body.innerText : '';
            const urlPattern = /https?:\\/\\/[^\\s]+\\.pdf/gi;
            const matches = pageText.matchAll(urlPattern);
            for (const match of matches) {
                allLinks.push(match[0]);
            }
        } catch (e) {
            // Ignora erros na extração de texto
        }
        
        return allLinks.filter(href => href.startsWith('http'));
    }""")

    # Remove duplicatas e URLs já testadas
    unicos = []
    for href in links:
        url_norm = normalizar_url(href)
        if url_norm not in urls_testadas:
            urls_testadas.add(url_norm)
            unicos.append(href)
    
    # Prioriza fontes confiáveis
    def prioridade_fonte(url: str) -> int:
        url_lower = url.lower()
        if any(x in url_lower for x in ['academia.edu', 'researchgate', 'scielo']):
            return 0
        elif any(x in url_lower for x in ['.edu', '.gov', 'biblioteca', 'repository']):
            return 1
        elif any(x in url_lower for x in ['archive.org', 'pdftop']):
            return 2
        else:
            return 3
    
    unicos.sort(key=prioridade_fonte)
    
    # Limita quantidade de links baseado no nível
    max_links = NIVEIS_BUSCA.get(nivel, 6)
    return unicos[:max_links]


def validar_pdf(caminho: str, termo_busca: str = "") -> bool:
    """Verifica se o arquivo é um PDF válido com no mínimo MIN_PAGINAS páginas
    e se o termo de busca aparece nas primeiras páginas."""
    try:
        # Verifica duplicatas por hash
        hash_pdf = calcular_hash_pdf(caminho)
        if hash_pdf and hash_pdf in hashes_pdfs:
            log.warning("PDF descartado: duplicata já baixada")
            return False
        
        doc = pymupdf.open(caminho)
        num_paginas = len(doc)
        
        # Valida número mínimo de páginas
        if num_paginas < MIN_PAGINAS:
            doc.close()
            log.warning("PDF descartado: apenas %d páginas (mínimo %d)", num_paginas, MIN_PAGINAS)
            return False
        
        # Verifica metadados do PDF (autor/título)
        metadata = doc.metadata
        texto_metadata = ""
        if metadata:
            texto_metadata = f"{metadata.get('title', '')} {metadata.get('author', '')}".lower()
        
        # Valida conteúdo nas primeiras páginas
        if termo_busca:
            # Extrai texto das primeiras 10 páginas (capa, contracapa, título, índice)
            texto_inicial = ""
            paginas_para_verificar = min(10, num_paginas)
            for i in range(paginas_para_verificar):
                texto_inicial += " " + doc[i].get_text().lower()
            
            # Adiciona metadados ao texto de validação
            texto_completo = texto_inicial + " " + texto_metadata
            doc.close()
            
            # Remove acentos para comparação mais flexível
            import unicodedata
            def remover_acentos(texto):
                return ''.join(c for c in unicodedata.normalize('NFD', texto) 
                              if unicodedata.category(c) != 'Mn')
            
            texto_normalizado = remover_acentos(texto_completo)
            termo_normalizado = remover_acentos(termo_busca.lower())
            
            # Separa palavras significativas (>3 caracteres, sem palavras comuns)
            palavras_ignorar = {'com', 'para', 'sobre', 'uma', 'dos', 'das', 'the', 'and', 'livro', 'ebook', 'pdf'}
            palavras_termo = [
                remover_acentos(p.lower()) 
                for p in termo_busca.split() 
                if len(p) > 3 and p.lower() not in palavras_ignorar
            ]
            
            if not palavras_termo:
                # Se não há palavras significativas, aceita
                if hash_pdf:
                    hashes_pdfs.add(hash_pdf)
                log.info("PDF válido: %d páginas", num_paginas)
                return True
            
            # Conta quantas palavras aparecem no texto
            palavras_encontradas = sum(1 for palavra in palavras_termo if palavra in texto_normalizado)
            percentual = palavras_encontradas / len(palavras_termo)
            
            # VALIDAÇÃO RIGOROSA: Pelo menos 70% das palavras devem estar presentes
            if percentual < 0.7:
                log.warning("PDF descartado: conteúdo não corresponde ao termo '%s'", termo_busca)
                log.warning("Palavras encontradas: %d/%d (%.0f%%)", 
                           palavras_encontradas, len(palavras_termo), percentual * 100)
                log.debug("Palavras buscadas: %s", palavras_termo)
                return False
            
            # PDF válido - adiciona hash ao cache
            if hash_pdf:
                hashes_pdfs.add(hash_pdf)
            
            log.info("PDF válido: %d páginas, %d/%d palavras encontradas (%.0f%%)", 
                    num_paginas, palavras_encontradas, len(palavras_termo), percentual * 100)
            return True
        else:
            doc.close()
        
        if hash_pdf:
            hashes_pdfs.add(hash_pdf)
        log.info("PDF válido: %d páginas", num_paginas)
        return True
        
    except Exception as e:
        log.warning("Arquivo não é um PDF válido: %s", e)
        return False


async def baixar_pdf(page, url: str, download_path: str) -> bool:
    """Baixa o PDF via request direto do Playwright."""
    try:
        response = await page.request.get(url, timeout=60000)  # 60 segundos para arquivos grandes
        if response.ok:
            body = await response.body()
            tamanho_mb = len(body) / (1024 * 1024)
            
            with open(download_path, "wb") as f:
                f.write(body)
            
            log.info("⬇️ Baixado: %.1f MB", tamanho_mb)
            return True
        log.warning("Resposta HTTP %s para: %s", response.status, url)
    except Exception as e:
        if "Timeout" in str(e):
            log.error("⏱️ Timeout ao baixar (arquivo muito grande): %s", url[:80])
        else:
            log.error("Download falhou: %s", str(e)[:200])
    return False


async def tentar_busca(page, query_str: str, download_path: str, termo_original: str, nivel: str = "moderado", motor: str = "bing") -> bool:
    """Executa uma busca e tenta baixar um PDF válido dos resultados."""
    # Suporta múltiplos motores de busca
    motores = {
        "bing": f"https://www.bing.com/search?q={quote_plus(query_str)}",
        "duckduckgo": f"https://duckduckgo.com/?q={quote_plus(query_str)}",
        "google": f"https://www.google.com/search?q={quote_plus(query_str)}",
        "yandex": f"https://yandex.com/search/?text={quote_plus(query_str)}",
        "brave": f"https://search.brave.com/search?q={quote_plus(query_str)}",
        "startpage": f"https://www.startpage.com/do/search?q={quote_plus(query_str)}",
        "qwant": f"https://www.qwant.com/?q={quote_plus(query_str)}",
    }
    
    search_url = motores.get(motor, motores["bing"])

    try:
        await page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
        await asyncio.sleep(random.uniform(2, 4))
        
        # Aguarda corpo da página estar disponível
        await page.wait_for_selector("body", timeout=5000)
    except Exception as e:
        log.error("Erro ao acessar motor de busca %s: %s", motor, str(e)[:100])
        return False

    links_pdf = await encontrar_links_pdf(page, nivel, motor)
    if not links_pdf:
        log.debug("🚫 Nenhum link PDF encontrado com motor %s", motor)
        return False

    log.info("✅ Encontrados %d links únicos no %s (testando até %d)", 
             len(links_pdf), motor, NIVEIS_BUSCA.get(nivel, 6))

    for i, url_pdf in enumerate(links_pdf):
        log.info("🔍 Tentativa %d/%d: %s", i + 1, len(links_pdf), url_pdf[:100])

        if not await baixar_pdf(page, url_pdf, download_path):
            await asyncio.sleep(random.uniform(0.5, 1))  # Delay menor entre falhas
            continue

        if validar_pdf(download_path, termo_original):
            return True

        os.remove(download_path)
        await asyncio.sleep(random.uniform(0.3, 0.8))  # Delay menor

    return False


def gerar_queries_inteligentes(termo: str) -> list[tuple[str, str]]:
    """Gera queries otimizadas com múltiplos motores de busca."""
    # Tenta separar autor e título se possível
    palavras = termo.split()
    autor = " ".join(palavras[-2:]) if len(palavras) > 2 else ""
    titulo = " ".join(palavras[:-2]) if len(palavras) > 2 else termo
    
    queries_base = [
        # Queries exatas - distribuídas entre motores
        (f'"{termo}" filetype:pdf', "bing"),
        (f'"{termo}" pdf', "google"),
        (f'"{termo}" pdf download', "duckduckgo"),
        (f'"{termo}" книга pdf', "yandex"),  # Russo: "livro"
        (f'"{termo}" filetype:pdf', "brave"),
        
        # Telegram - Links públicos indexados
        (f'{termo} site:t.me pdf', "google"),
        (f'{termo} telegram pdf download', "bing"),
        (f'{termo} pdf t.me', "duckduckgo"),
        (f'"{termo}" site:t.me', "google"),
        (f'{termo} grupo telegram pdf', "bing"),
        (f'{termo} canal telegram livro pdf', "google"),
        
        # Queries com variações
        (f"livro {termo} filetype:pdf", "google"),
        (f"{termo} pdf completo", "duckduckgo"),
        (f"download pdf {termo}", "bing"),
        (f"{termo} pdf gratis download", "startpage"),
        (f"baixar {termo} pdf", "bing"),
        (f"ebook {termo} pdf", "duckduckgo"),
        (f"{termo} pdf portugues", "google"),
        (f"{termo} livro pdf download", "qwant"),
        (f"pdf {termo} completo gratis", "brave"),
        (f"{termo} book pdf", "google"),
        (f"free pdf {termo}", "bing"),
        
        # Queries específicas
        (f"{termo} pdf online", "google"),
        (f"{termo} epub pdf", "duckduckgo"),
        (f"download gratis {termo} pdf", "yandex"),
        (f"{termo} pdf ler online", "startpage"),
        
        # Sites específicos - distribuídos
        (f"{termo} site:archive.org", "google"),
        (f"{termo} pdf site:academia.edu", "google"),
        (f"{termo} pdf site:researchgate.net", "startpage"),
        (f"{termo} site:scribd.com", "bing"),
        (f"{termo} pdf site:z-lib.org", "brave"),
        (f"{termo} pdf site:libgen", "yandex"),
        (f"{termo} site:pdfdrive.com", "qwant"),
        (f"{termo} pdf site:bookfi.net", "duckduckgo"),
        (f"{termo} site:epdf.pub", "google"),
        (f"{termo} pdf site:1lib.domains", "brave"),
        
        # Redes sociais e fóruns
        (f"{termo} pdf site:reddit.com", "google"),
        (f"{termo} livro pdf site:facebook.com", "bing"),
        
        # Queries com autor separado (se detectado)
        (f'{autor} "{titulo}" pdf', "google") if autor else (f"{termo} pdf", "google"),
        (f'livro {titulo} {autor} pdf', "bing") if autor else (f"livro {termo} pdf", "bing"),
        (f'{autor} {titulo} filetype:pdf', "startpage") if autor else (f"{termo} filetype:pdf", "startpage"),
        
        # Queries alternativas - diversos motores
        (f"{termo.replace(' ', '+')} filetype:pdf", "bing"),
        (f"{termo} pdf free download", "duckduckgo"),
        (f"{termo} pdf full book", "google"),
        (f"{termo} complete pdf", "brave"),
        (f"{termo} полный pdf", "yandex"),  # Russo: "completo"
        (f"{termo} libro completo pdf", "qwant"),  # Espanhol
        (f"{termo} livre complet pdf", "startpage"),  # Francês
    ]
    
    return queries_base


async def buscar_e_baixar(
    page, 
    termo: str, 
    nivel: str = "moderado",
    callback_progresso: Optional[Callable[[str, str], None]] = None
) -> bool:
    """Busca e baixa um PDF válido. Retorna True se conseguiu."""
    nome_arquivo = f"{termo[:50].replace(' ', '_').replace(':', '')}.pdf"
    download_path = os.path.join(DOWNLOAD_DIR, nome_arquivo)

    if callback_progresso:
        callback_progresso(termo, "verificando")

    if os.path.exists(download_path) and validar_pdf(download_path, termo):
        log.info("Já baixado: %s", nome_arquivo)
        if callback_progresso:
            callback_progresso(termo, "sucesso")
        return True

    # Gera queries com múltiplos motores de busca
    queries = gerar_queries_inteligentes(termo)

    try:
        # Tenta com motores diferentes para diversificar resultados
        for query, motor in queries:
            log.info("Buscando [%s]: %s", motor.upper(), query[:60])
            if callback_progresso:
                callback_progresso(termo, "buscando")
            
            if await tentar_busca(page, query, download_path, termo, nivel, motor):
                log.info("✅ Download concluído: %s", nome_arquivo)
                if callback_progresso:
                    callback_progresso(termo, "sucesso")
                return True
            
            # Delay entre queries para evitar bloqueio
            await asyncio.sleep(random.uniform(2, 4))

        log.warning("❌ Nenhum PDF válido encontrado para: %s", termo)
        if callback_progresso:
            callback_progresso(termo, "falhou")
        return False

    except Exception as e:
        log.error("Erro ao buscar '%s': %s", termo, e)
        if callback_progresso:
            callback_progresso(termo, "erro")
        return False


async def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    async with async_playwright() as p:
        browser, page = await configurar_navegador(p)
        falhas = []

        try:
            for livro in LISTA_LIVROS_PADRAO:
                sucesso = await buscar_e_baixar(page, livro, nivel="moderado")
                if not sucesso:
                    falhas.append(livro)
                await asyncio.sleep(random.uniform(5, 10))

            # Segunda rodada para os que falharam
            if falhas:
                log.info("=== Retry: %d livros falharam, tentando novamente ===", len(falhas))
                for livro in falhas:
                    await buscar_e_baixar(page, livro, nivel="moderado")
                    await asyncio.sleep(random.uniform(5, 10))

        finally:
            await browser.close()

    # Relatório final
    baixados = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".pdf")]
    log.info("=== Resultado: %d/%d PDFs baixados ===", len(baixados), len(LISTA_LIVROS_PADRAO))
    if falhas:
        log.warning("Livros sem PDF válido:")
        for f in falhas:
            log.warning("  - %s", f)


class CrawlerBibliografia:
    """Classe para gerenciar busca e download de bibliografia."""
    
    def __init__(self, callback_progresso: Optional[Callable[[str, str], None]] = None):
        self.callback_progresso = callback_progresso
        self.sucessos = []
        self.falhas = []
        self.cancelar = False
        
    async def executar(self, lista_livros: list[str], nivel: str = "moderado"):
        """Executa o crawler para uma lista de livros."""
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        self.sucessos = []
        self.falhas = []
        
        async with async_playwright() as p:
            browser, page = await configurar_navegador(p)
            
            try:
                for livro in lista_livros:
                    # Verifica se foi cancelado
                    if self.cancelar:
                        log.warning("Busca cancelada pelo usuário")
                        break
                    
                    sucesso = await buscar_e_baixar(
                        page, 
                        livro, 
                        nivel=nivel,
                        callback_progresso=self.callback_progresso
                    )
                    
                    if sucesso:
                        self.sucessos.append(livro)
                    else:
                        self.falhas.append(livro)
                    
                    await asyncio.sleep(random.uniform(3, 6))
                
            finally:
                await browser.close()
        
        return {
            "sucessos": self.sucessos,
            "falhas": self.falhas,
            "total": len(lista_livros)
        }


if __name__ == "__main__":
    asyncio.run(main())
