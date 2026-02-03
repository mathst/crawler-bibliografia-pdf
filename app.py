import asyncio
import atexit
import os
import shutil
import zipfile
import re
from datetime import datetime
import flet as ft
from main import CrawlerBibliografia, DOWNLOAD_DIR, LISTA_LIVROS_PADRAO, NIVEIS_BUSCA


def processar_lista_livros(texto: str) -> list[str]:
    """
    Processa e limpa a lista de livros de forma inteligente.
    
    Remove:
    - Marcadores de lista (-, *, •, >, |)
    - Numeração (1., 2), [3], etc)
    - Espaços extras
    - Linhas muito curtas (< 10 caracteres)
    - Caracteres especiais no início
    
    Returns:
        Lista de livros limpos e prontos para busca
    """
    linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
    livros_processados = []
    
    for linha in linhas:
        # Remove marcadores de lista
        linha = re.sub(r'^[-*•>|#]+\s*', '', linha)
        # Remove numeração (1., 2), [3], etc)
        linha = re.sub(r'^\[?\d+[\.\)\]]\s*', '', linha)
        # Remove espaços extras
        linha = ' '.join(linha.split())
        # Remove caracteres inválidos
        linha = linha.strip('.,;:')
        
        # Aceita apenas linhas com tamanho razoável
        if linha and len(linha) > 10:
            livros_processados.append(linha)
    
    return livros_processados


class BibliografiaCrawlerApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Bibliografia Crawler"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.scroll = ft.ScrollMode.AUTO
        
        self.crawler = None
        self.em_execucao = False
        self.cancelar_busca = False
        self.task_atual = None
        self.resultados = {"sucessos": [], "falhas": []}
        self.mensagem_status = None
        
        # FilePicker para salvar ZIP
        try:
            self.file_picker = ft.FilePicker(on_result=self.salvar_zip_resultado)
            self.page.overlay.append(self.file_picker)
            self.page.update()
        except:
            self.file_picker = None  # Fallback se FilePicker não disponível
        
        # Registra limpeza de PDFs ao fechar o app
        atexit.register(self.limpar_downloads)
        
        self.setup_ui()
    
    def limpar_downloads(self):
        """Remove todos os PDFs baixados ao fechar o app."""
        try:
            if os.path.exists(DOWNLOAD_DIR):
                shutil.rmtree(DOWNLOAD_DIR)
                print(f"✅ Pasta {DOWNLOAD_DIR} removida com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao limpar downloads: {e}")
    
    def mostrar_mensagem(self, texto: str, cor=None):
        """Mostra mensagem de status."""
        if self.mensagem_status:
            self.mensagem_status.value = texto
            if cor:
                self.mensagem_status.color = cor
            self.page.update()
    
    def setup_ui(self):
        """Configura a interface do usuário."""
        
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Text("📚", size=40),
                ft.Column([
                    ft.Text(
                        "Bibliografia Crawler",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900
                    ),
                    ft.Text(
                        "Busca inteligente de livros em PDF",
                        size=13,
                        color=ft.Colors.BLUE_700,
                        italic=True
                    ),
                    ft.Text(
                        "✨ 3 motores de busca • Cache inteligente • Validação MD5 • Metadados PDF",
                        size=10,
                        color=ft.Colors.GREEN_600,
                        weight=ft.FontWeight.W_500
                    ),
                ], spacing=4),
            ], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
            border=ft.Border.only(bottom=ft.BorderSide(2, ft.Colors.BLUE_100))
        )
        
        # Input de lista com container estilizado
        self.input_lista = ft.TextField(
            label="📝 Lista de Livros (um por linha)",
            multiline=True,
            min_lines=8,
            max_lines=20,
            value="\n".join(LISTA_LIVROS_PADRAO),
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE_700,
            hint_text="Cole sua bibliografia aqui...\n\nAceita diversos formatos:\n• AUTOR, Nome. Título do Livro\n• 1. Nome do Livro\n• - Título do livro",
            text_size=14,
            height=280,
        )
        
        input_container = ft.Container(
            content=self.input_lista,
            padding=15,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, ft.Colors.BLUE_200),
            border_radius=10,
            expand=True,
        )
        
        # Seletor de nível
        self.nivel_selector = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(
                    value="rapido",
                    label="🚀 Rápido (5 PDFs/query)",
                    label_style=ft.TextStyle(size=14)
                ),
                ft.Radio(
                    value="moderado",
                    label="⚡ Moderado (15 PDFs/query)",
                    label_style=ft.TextStyle(size=14)
                ),
                ft.Radio(
                    value="completo",
                    label="🔍 Completo (TODOS até achar)",
                    label_style=ft.TextStyle(size=14)
                ),
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            value="moderado"
        )
        
        nivel_info = ft.Container(
            content=ft.Column([
                ft.Text("⚙️ Níveis de Busca", weight=ft.FontWeight.BOLD, size=14),
                self.nivel_selector,
                ft.Text(
                    "� 32 queries × até 15 PDFs = 480 tentativas (moderado) | Extração avançada de links",
                    size=11,
                    color=ft.Colors.GREEN_700,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "⏱️ Rápido: ~60s • Moderado: ~120s • Completo: busca exaustiva (pode levar vários minutos)",
                    size=10,
                    color=ft.Colors.BLUE_600,
                    italic=True,
                    text_align=ft.TextAlign.CENTER
                ),
            ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=15,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=8,
        )
        
        # Botões de ação
        self.btn_iniciar = ft.Button(
            "▶️ Iniciar Busca",
            on_click=self.iniciar_busca,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                padding=15,
            ),
            width=200,
        )
        
        self.btn_parar = ft.Button(
            "⏹️ Parar",
            on_click=self.parar_busca,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.RED_700,
                color=ft.Colors.WHITE,
                padding=15,
            ),
            width=200,
            visible=False,
        )
        
        self.btn_download_zip = ft.Button(
            "📦 Baixar ZIP",
            on_click=self.criar_zip,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE,
                padding=15,
            ),
            width=200,
            visible=False,
        )
        
        botoes = ft.Row([
            self.btn_iniciar,
            self.btn_parar,
            self.btn_download_zip,
        ], spacing=15, alignment=ft.MainAxisAlignment.CENTER)
        
        # Área de progresso
        self.progresso_text = ft.Text(
            "Aguardando...",
            size=14,
            weight=ft.FontWeight.W_500,
            color=ft.Colors.GREY_700,
            text_align=ft.TextAlign.CENTER
        )
        
        self.mensagem_status = ft.Text(
            "",
            size=12,
            color=ft.Colors.BLUE_700,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        
        self.progresso_bar = ft.ProgressBar(
            visible=False,
            color=ft.Colors.BLUE_700,
            bgcolor=ft.Colors.BLUE_100,
            expand=True,
        )
        
        self.progresso_area = ft.Container(
            content=ft.Column([
                self.progresso_text,
                self.progresso_bar,
                self.mensagem_status,
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            border=ft.Border.all(2, ft.Colors.BLUE_200),
            visible=False,
            expand=True,
        )
        
        # Lista de resultados - containers separados
        self.lista_sucessos = ft.Column([], spacing=5, scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.lista_falhas = ft.Column([], spacing=5, scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Container de sucessos (inicialmente oculto)
        self.sucessos_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    "✅ Sucessos", 
                    size=17, 
                    weight=ft.FontWeight.BOLD, 
                    color=ft.Colors.GREEN_700,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(
                    content=self.lista_sucessos,
                    padding=12,
                    height=100,
                    border=ft.Border.all(2, ft.Colors.GREEN_300),
                    border_radius=8,
                    bgcolor=ft.Colors.GREEN_50,
                ),
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            border=ft.Border.all(1, ft.Colors.GREEN_200),
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            visible=False,
            expand=True,
        )
        
        # Container de falhas (inicialmente oculto)
        self.falhas_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    "❌ Falhas", 
                    size=17, 
                    weight=ft.FontWeight.BOLD, 
                    color=ft.Colors.RED_700,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(
                    content=self.lista_falhas,
                    padding=12,
                    height=80,
                    border=ft.Border.all(2, ft.Colors.RED_300),
                    border_radius=8,
                    bgcolor=ft.Colors.RED_50,
                ),
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            border=ft.Border.all(1, ft.Colors.RED_200),
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            visible=False,
            expand=True,
        )
        
        # Layout principal com ref para scroll
        self.scroll_column = ft.Column([
            input_container,
            nivel_info,
            ft.Container(
                content=botoes,
                padding=ft.Padding(top=10, bottom=10, left=0, right=0),
            ),
            self.progresso_area,
            self.sucessos_container,
            self.falhas_container,
        ], 
        spacing=25, 
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        auto_scroll=True)
        
        main_content = ft.Container(
            content=ft.Column([
                header,
                ft.Container(
                    content=self.scroll_column,
                    padding=ft.Padding(left=40, right=40, top=20, bottom=20),
                    expand=True,
                )
            ], spacing=0),
            expand=True,
        )
        
        self.page.add(main_content)
    
    def atualizar_progresso(self, livro: str, status: str):
        """Callback chamado durante o crawler."""
        status_icons = {
            "verificando": "🔍",
            "buscando": "⏳",
            "sucesso": "✅",
            "falhou": "❌",
            "erro": "⚠️",
        }
        
        icon = status_icons.get(status, "📖")
        self.progresso_text.value = f"{icon} {livro[:60]}..."
        
        if status == "sucesso":
            self.lista_sucessos.controls.append(
                ft.Container(
                    content=ft.Text(f"✅ {livro}", size=12),
                    padding=5,
                    bgcolor=ft.Colors.GREEN_50,
                    border_radius=4,
                )
            )
            # Mostra o container de sucessos quando houver pelo menos 1 sucesso
            self.sucessos_container.visible = True
            
        elif status in ["falhou", "erro"]:
            self.lista_falhas.controls.append(
                ft.Container(
                    content=ft.Text(f"❌ {livro}", size=12, color=ft.Colors.RED_700),
                    padding=5,
                    bgcolor=ft.Colors.RED_50,
                    border_radius=4,
                )
            )
            # Mostra o container de falhas quando houver pelo menos 1 falha
            self.falhas_container.visible = True
        
        self.page.update()
    
    async def executar_crawler(self, lista_livros: list[str], nivel: str):
        """Executa o crawler de forma assíncrona."""
        self.crawler = CrawlerBibliografia(callback_progresso=self.atualizar_progresso)
        self.crawler.cancelar = False  # Reset flag
        
        try:
            self.resultados = await self.crawler.executar(lista_livros, nivel)
        except asyncio.CancelledError:
            self.progresso_text.value = "⚠️ Busca cancelada pelo usuário"
            self.mostrar_mensagem("🛑 Busca interrompida", ft.Colors.ORANGE_700)
            self.em_execucao = False
            self.btn_iniciar.visible = True
            self.btn_parar.visible = False
            self.progresso_bar.visible = False
            self.page.update()
            return
        
        # Finaliza
        self.em_execucao = False
        self.progresso_text.value = f"✅ Concluído! {len(self.resultados['sucessos'])}/{self.resultados['total']} encontrados"
        self.progresso_bar.visible = False
        self.btn_iniciar.visible = True
        self.btn_parar.visible = False
        
        if self.resultados['sucessos']:
            self.btn_download_zip.visible = True
        
        self.page.update()
        
        # Rola para mostrar os resultados finais
        asyncio.create_task(self._scroll_to_results())
    
    async def _scroll_to_progress(self):
        """Rola para a área de progresso."""
        await asyncio.sleep(0.2)
        await self.scroll_column.scroll_to(offset=500, duration=300)
        self.page.update()
    
    async def _scroll_to_results(self):
        """Rola para mostrar resultados finais."""
        await asyncio.sleep(0.2)
        await self.scroll_column.scroll_to(offset=-1, duration=500)
        self.page.update()
    
    def iniciar_busca(self, e):
        """Inicia a busca."""
        if self.em_execucao:
            return
        
        # Limpa resultados anteriores
        self.lista_sucessos.controls.clear()
        self.lista_falhas.controls.clear()
        self.resultados = {"sucessos": [], "falhas": []}
        
        # Esconde os containers de resultado
        self.sucessos_container.visible = False
        self.falhas_container.visible = False
        
        # Obtém e processa lista de livros
        texto = self.input_lista.value.strip()
        if not texto:
            self.mostrar_mensagem("❌ Adicione pelo menos um livro", ft.Colors.RED_700)
            return
        
        # Processa lista de forma inteligente
        lista_livros = processar_lista_livros(texto)
        if not lista_livros:
            self.mostrar_mensagem("❌ Nenhum livro válido encontrado na lista", ft.Colors.RED_700)
            return
        
        # DEBUG: Mostra os livros que serão processados
        print(f"\n{'='*60}")
        print(f"📚 LIVROS A BUSCAR ({len(lista_livros)}):")
        for i, livro in enumerate(lista_livros, 1):
            print(f"{i}. {livro}")
        print(f"{'='*60}\n")
            
        nivel = self.nivel_selector.value or "moderado"  #Default se None
        
        # Mapeia nível para quantidade de links
        niveis_info = {
            "rapido": "5 PDFs × 32 queries = 160 tentativas",
            "moderado": "15 PDFs × 32 queries = 480 tentativas",
            "completo": "TODOS os PDFs (busca exaustiva infinita)"
        }
        info_nivel = niveis_info.get(nivel, "15 PDFs")
        
        # Mostra informação sobre otimizações
        self.mostrar_mensagem(
            f"🎯 {len(lista_livros)} livros • {info_nivel} • 3 motores de busca",
            ft.Colors.BLUE_700
        )
        
        # Atualiza UI
        self.em_execucao = True
        self.cancelar_busca = False
        self.btn_iniciar.visible = False
        self.btn_parar.visible = True
        self.btn_download_zip.visible = False
        self.progresso_area.visible = True
        self.progresso_bar.visible = True
        self.progresso_text.value = f"Iniciando busca de {len(lista_livros)} livros (nível: {nivel})..."
        self.page.update()
        
        # Rola para a área de progresso (auto_scroll irá rolar automaticamente)
        asyncio.create_task(self._scroll_to_progress())
        
        # Executa crawler em thread assíncrona e salva a task
        self.task_atual = asyncio.create_task(self.executar_crawler(lista_livros, nivel))
    
    def parar_busca(self, e):
        """Para a busca em andamento."""
        if not self.em_execucao:
            return
        
        # Define flag de cancelamento
        self.cancelar_busca = True
        if self.crawler:
            self.crawler.cancelar = True
        
        # Cancela a task
        if self.task_atual and not self.task_atual.done():
            self.task_atual.cancel()
        
        # Atualiza UI
        self.em_execucao = False
        self.btn_iniciar.visible = True
        self.btn_parar.visible = False
        self.progresso_text.value = "⚠️ Busca parada pelo usuário"
        self.progresso_bar.visible = False
        
        self.mostrar_mensagem("🛑 Busca interrompida com sucesso", ft.Colors.ORANGE_700)
        self.page.update()
    
    def criar_zip(self, e):
        """Cria arquivo ZIP com todos os PDFs baixados."""
        if not os.path.exists(DOWNLOAD_DIR):
            self.mostrar_mensagem("❌ Nenhum PDF encontrado", ft.Colors.RED_700)
            return
        
        pdfs = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.pdf')]
        if not pdfs:
            self.mostrar_mensagem("❌ Nenhum PDF encontrado", ft.Colors.RED_700)
            return
        
        # Tenta usar FilePicker se disponível
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if self.file_picker:
            try:
                self.file_picker.save_file(
                    dialog_title="Salvar ZIP com PDFs",
                    file_name=f"bibliografia_{timestamp}.zip",
                    allowed_extensions=["zip"],
                )
                return
            except:
                pass
        
        # Fallback: salva na pasta atual
        self.salvar_zip_fallback(timestamp, pdfs)
    
    def salvar_zip_fallback(self, timestamp: str, pdfs: list[str]):
        """Salva ZIP na pasta atual se FilePicker falhar."""
        zip_path = f"bibliografia_{timestamp}.zip"
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for pdf in pdfs:
                    pdf_path = os.path.join(DOWNLOAD_DIR, pdf)
                    zipf.write(pdf_path, pdf)
            
            caminho_completo = os.path.abspath(zip_path)
            self.mostrar_mensagem(
                f"✅ ZIP criado com {len(pdfs)} PDFs\n📁 {caminho_completo}", 
                ft.Colors.GREEN_700
            )
        except Exception as ex:
            self.mostrar_mensagem(f"❌ Erro ao criar ZIP: {ex}", ft.Colors.RED_700)
    
    def salvar_zip_resultado(self, e: ft.FilePickerResultEvent):
        """Callback quando usuário escolhe onde salvar o ZIP."""
        if not e.path:
            return
        
        # Cria ZIP no caminho escolhido
        zip_path = e.path
        if not zip_path.endswith('.zip'):
            zip_path += '.zip'
        
        try:
            pdfs = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.pdf')]
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for pdf in pdfs:
                    pdf_path = os.path.join(DOWNLOAD_DIR, pdf)
                    zipf.write(pdf_path, pdf)
            
            self.mostrar_mensagem(f"✅ ZIP salvo: {os.path.basename(zip_path)} ({len(pdfs)} arquivos)", ft.Colors.GREEN_700)
        except Exception as ex:
            self.mostrar_mensagem(f"❌ Erro ao criar ZIP: {ex}", ft.Colors.RED_700)


def main(page: ft.Page):
    BibliografiaCrawlerApp(page)


if __name__ == "__main__":
    ft.run(main)
