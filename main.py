import asyncio
import random
import os
import logging
from urllib.parse import quote_plus
from typing import Callable, Optional
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

# Níveis de busca: define quantos links PDF tentar
NIVEIS_BUSCA = {
    "rapido": 2,      # Apenas os 2 primeiros PDFs
    "moderado": 4,    # Até 4 PDFs
    "completo": 6,    # Até 6 PDFs
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


async def encontrar_links_pdf(page, nivel: str = "moderado") -> list[str]:
    """Extrai todos os links PDF únicos dos resultados do Bing."""
    links = await page.evaluate("""() => {
        return Array.from(document.querySelectorAll('a'))
            .map(a => a.href)
            .filter(href => href.match(/\\.pdf(\\?|#|$)/i))
            .filter(href => href.startsWith('http'))
    }""")

    seen = set()
    unicos = []
    for href in links:
        if href not in seen:
            seen.add(href)
            unicos.append(href)
    
    # Limita quantidade de links baseado no nível
    max_links = NIVEIS_BUSCA.get(nivel, 4)
    return unicos[:max_links]


def validar_pdf(caminho: str) -> bool:
    """Verifica se o arquivo é um PDF válido com no mínimo MIN_PAGINAS páginas."""
    try:
        doc = pymupdf.open(caminho)
        num_paginas = len(doc)
        doc.close()
        if num_paginas >= MIN_PAGINAS:
            log.info("PDF válido: %d páginas", num_paginas)
            return True
        log.warning("PDF descartado: apenas %d páginas (mínimo %d)", num_paginas, MIN_PAGINAS)
        return False
    except Exception as e:
        log.warning("Arquivo não é um PDF válido: %s", e)
        return False


async def baixar_pdf(page, url: str, download_path: str) -> bool:
    """Baixa o PDF via request direto do Playwright."""
    try:
        response = await page.request.get(url, timeout=30000)
        if response.ok:
            body = await response.body()
            with open(download_path, "wb") as f:
                f.write(body)
            return True
        log.warning("Resposta HTTP %s para: %s", response.status, url)
    except Exception as e:
        log.error("Download falhou: %s", e)
    return False


async def tentar_busca(page, query_str: str, download_path: str, nivel: str = "moderado") -> bool:
    """Executa uma busca e tenta baixar um PDF válido dos resultados."""
    search_url = f"https://www.bing.com/search?q={quote_plus(query_str)}"

    await page.goto(search_url, wait_until="load", timeout=20000)
    await asyncio.sleep(random.uniform(2, 4))

    links_pdf = await encontrar_links_pdf(page, nivel)
    if not links_pdf:
        return False

    for i, url_pdf in enumerate(links_pdf):
        log.info("Tentativa %d/%d: %s", i + 1, len(links_pdf), url_pdf)

        if not await baixar_pdf(page, url_pdf, download_path):
            continue

        if validar_pdf(download_path):
            return True

        os.remove(download_path)

    return False


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

    if os.path.exists(download_path) and validar_pdf(download_path):
        log.info("Já baixado: %s", nome_arquivo)
        if callback_progresso:
            callback_progresso(termo, "sucesso")
        return True

    # Queries otimizadas com palavras-chave variadas
    queries = [
        f'"{termo}" filetype:pdf',
        f"livro {termo} filetype:pdf",
        f"download pdf {termo}",
        f"{termo} pdf gratis download",
        f"baixar {termo} pdf",
        f"ebook {termo} pdf",
    ]

    try:
        for q in queries:
            log.info("Buscando: %s", q)
            if callback_progresso:
                callback_progresso(termo, "buscando")
            
            if await tentar_busca(page, q, download_path, nivel):
                log.info("Download concluído: %s", nome_arquivo)
                if callback_progresso:
                    callback_progresso(termo, "sucesso")
                return True

        log.warning("Nenhum PDF válido (>%d páginas) para: %s", MIN_PAGINAS, termo)
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
