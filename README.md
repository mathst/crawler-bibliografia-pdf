# 📚 Bibliografia Crawler

> **Sistema inteligente de busca e download automático de livros em PDF**

Busca e baixa automaticamente livros em PDF a partir de uma lista de referências bibliográficas usando Playwright + Bing com interface gráfica moderna.

> **Gerenciador de pacotes:** Este projeto usa [uv](https://docs.astral.sh/uv/) - um gerenciador de pacotes Python moderno, ultra-rápido (10-100x mais rápido que pip) e que gerencia ambientes virtuais automaticamente.

---

## 📋 Índice

- [✨ Funcionalidades](#-funcionalidades)
- [💻 Multiplataforma](#-multiplataforma)
- [📦 Instalação](#-instalação)
  - [Instalação Rápida (Linux/Mac)](#instalação-rápida-linuxmac)
  - [Instalação Manual (Todas as Plataformas)](#instalação-manual-todas-as-plataformas)
- [🚀 Como Usar](#-como-usar)
- [⚡ Exemplos de Lista](#-exemplos-de-lista)
- [💡 Dicas e Estratégias](#-dicas-e-estratégias)
- [🎯 Estimativa de Tempo](#-estimativa-de-tempo)
- [❓ Problemas Comuns](#-problemas-comuns)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🔥 Desenvolvimento](#-desenvolvimento)

---

## ✨ Funcionalidades

### 🎨 Interface Gráfica (Flet)
- ✅ **Design minimalista e profissional**
- 📝 **Editor de lista de livros integrado** com auto-detecção de formato
- 🎚️ **3 níveis de busca configuráveis** (Rápido, Moderado, Completo)
- 📊 **Progresso em tempo real** com animações e status detalhado
- ✅ **Visualização de sucessos e falhas** em containers separados
- 📦 **Download em ZIP** com seleção de pasta de destino
- 🛑 **Cancelamento de busca** a qualquer momento
- 📜 **Auto-scroll** para acompanhar progresso

### 🤖 Motor de Busca Inteligente
- 🔍 **6 variações de query** por livro (busca otimizada)
- 🎯 **3 níveis de profundidade configuráveis:**
  - **🚀 Rápido**: 2 links por query (~30s/livro)
  - **⚡ Moderado**: 4 links por query (~60s/livro)
  - **🔍 Completo**: 6 links por query (~90s/livro)
- 🤖 **Anti-bot** com playwright-stealth
- ✅ **Validação automática** de PDFs (mínimo 50 páginas)
- 🔁 **Fallback automático** entre queries
- 💾 **Pula livros já baixados** (evita re-download)
- 🧹 **Auto-detecta formato** da lista (remove marcadores, numeração, etc.)

### 🔍 Variações de Busca

Cada livro é buscado com **6 variações diferentes**:
1. `"termo exato" filetype:pdf` - Busca exata
2. `livro termo filetype:pdf` - Com palavra "livro"
3. `download pdf termo` - Com "download"
4. `termo pdf gratis download` - Palavras-chave populares
5. `baixar termo pdf` - Português
6. `ebook termo pdf` - Formato ebook

---

## 💻 Multiplataforma

O Bibliografia Crawler funciona em **Windows, Linux, macOS e Android** através do Flet.

### 🖥️ **Desktop (Windows, Linux, macOS)**
- Interface nativa usando Flet
- Executável independente
- Sem necessidade de navegador

### 📱 **Android**
- APK instalável
- Interface touch-friendly
- Funciona offline após instalação

### 🌐 **Web (Opcional)**
- Pode ser executado como aplicação web
- Acesso via navegador

### ⚙️ **Requisitos Mínimos**
- **Python**: 3.10+
- **RAM**: 2GB (4GB recomendado)
- **Espaço em disco**: 500MB
- **Internet**: Conexão estável (para busca e download)

---

## 📦 Instalação

### Instalação Rápida (Linux/Mac)

```bash
./start.sh
```

**Este script irá:**
1. ✅ Verificar Python 3.10+
2. 📦 Instalar uv (gerenciador de pacotes)
3. 🔧 Instalar todas as dependências
4. 🌐 Instalar navegador Chromium
5. 🚀 Iniciar a interface gráfica

---

### Instalação Manual (Todas as Plataformas)

#### **1. Instalar uv (Gerenciador de Pacotes)**

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Windows (Scoop):**
```bash
scoop install uv
```

**Windows (pip):**
```bash
pip install uv
```

#### **2. Clonar ou Baixar o Projeto**

```bash
git clone <repo-url>
cd Crawler
```

#### **3. Instalar Dependências**

```bash
uv sync
```

#### **4. Instalar Navegador Chromium**

```bash
uv run playwright install chromium
```

#### **5. Executar**

**Modo Normal:**
```bash
uv run python app.py
```

**Modo Desenvolvimento (hot reload):**
```bash
uv run python app.py --hot-reload
# ou
chmod +x dev.sh && ./dev.sh
```

---

## 🚀 Como Usar

### Interface Gráfica - Passo a Passo

#### **1. Cole sua lista de livros**
- Um livro por linha
- Formato aceito: `AUTOR, Nome. Título do Livro`
- Também aceita: listas numeradas, marcadores, etc.

**Exemplo:**
```
SZWARCFITER, Jayme L.; MARKENZON, Lilian. Estruturas de Dados e seus Algoritmos
TANENBAUM, Andrew S. Redes de computadores
SILBERSCHATZ, A. Fundamentos de Sistemas Operacionais
```

#### **2. Escolha o nível de busca**

| Nível | Links Testados | Tempo/Livro | Quando Usar |
|-------|----------------|-------------|-------------|
| 🚀 **Rápido** | 2 PDFs | ~30s | Listas grandes (>15 livros) |
| ⚡ **Moderado** | 4 PDFs | ~60s | Uso geral (5-15 livros) ⭐ |
| 🔍 **Completo** | 6 PDFs | ~90s | Livros raros (<5 livros) |

> **💡 Dica:** Comece sempre com "Moderado" (padrão)

#### **3. Clique em "▶️ Iniciar Busca"**
- Interface rola automaticamente para o progresso
- Acompanhe em tempo real cada livro sendo buscado
- Veja sucessos e falhas conforme aparecem

#### **4. (Opcional) Pare a busca**
- Clique em "⏹️ Parar" para interromper
- Resultados parciais são preservados

#### **5. Baixe o ZIP**
- Clique em "📦 Baixar ZIP"
- **Escolha onde salvar** o arquivo
- Todos os PDFs encontrados serão compactados

---

## ⚡ Exemplos de Lista

### 📝 Lista Pequena (Teste Rápido)
```
SZWARCFITER, Jayme L. Estruturas de Dados e seus Algoritmos
TANENBAUM, Andrew S. Redes de computadores
```

### 📚 Lista Completa (Ciência da Computação)
```
SZWARCFITER, Jayme L.; MARKENZON, Lilian. Estruturas de Dados e seus Algoritmos
BORIN, Vinicius P. Estrutura de Dados
ELMASRI, R; NAVATHE, S. B. Sistemas de Banco de Dados
DATE, C. J. Introdução a Sistemas de Bancos de Dados
TANENBAUM, Andrew S. Redes de computadores
KUROSE, James F. Redes de Computadores e a internet
SILBERSCHATZ, A. Fundamentos de Sistemas Operacionais
RUSSELL, Stuart J.; NORVIG, Peter. Inteligência artificial
```

### 🔢 Lista com Numeração (Auto-detectada)
```
1. SZWARCFITER, Jayme L. Estruturas de Dados
2. TANENBAUM, Andrew S. Redes de computadores
3. SILBERSCHATZ, A. Sistemas Operacionais
```

### 📌 Lista com Marcadores (Auto-detectada)
```
- SZWARCFITER, Jayme L. Estruturas de Dados
- TANENBAUM, Andrew S. Redes de computadores
- SILBERSCHATZ, A. Sistemas Operacionais
```

> **✨ O sistema detecta automaticamente** o formato e limpa marcadores, numeração e espaços

---

## 💡 Dicas e Estratégias

### 🎯 Para Melhor Resultado

✅ **Use citações completas** (autor + título)  
✅ **Comece com nível "Moderado"**  
✅ **Liste 5-10 livros por vez**  
✅ **Verifique sucessos antes de continuar**  

❌ Evite listas muito genéricas  
❌ Não use apenas o título (sem autor)  
❌ Evite listas com mais de 20 livros de uma vez  

### 📊 Estratégia em 3 Passos

1. **Primeira rodada**: Nível "Rápido" com lista completa (15+ livros)
2. **Segunda rodada**: Nível "Completo" apenas com as falhas
3. **Download final**: Baixe o ZIP com todos os sucessos

### 🎓 Use Cases Específicos

| Situação | Nível Recomendado | Estratégia |
|----------|-------------------|------------|
| TCC/Dissertação | Completo | Lista pequena (5-8), busca completa |
| Revisão Bibliográfica | Rápido → Completo | Duas rodadas, rápido primeiro |
| Livros Específicos | Completo | Busca individual, máxima precisão |
| Grande Quantidade | Rápido | Lotes de 10-15, depois refinar falhas |

---

## 🎯 Estimativa de Tempo

### 📊 Cálculo de Tempo

```
Tempo Total = (Nº de Livros) × (Tempo por Livro do Nível)

Exemplos:
10 livros × Moderado (60s) = ~10 minutos
15 livros × Rápido (30s)   = ~7 minutos
5 livros × Completo (90s)  = ~7 minutos
```

### ⏱️ Tempos Reais (Aproximados)

| Quantidade | Rápido | Moderado | Completo |
|------------|--------|----------|----------|
| 5 livros   | 2-3 min | 5-6 min | 7-8 min |
| 10 livros  | 5-6 min | 10-12 min | 15-18 min |
| 15 livros  | 7-9 min | 15-18 min | 22-27 min |
| 20 livros  | 10-12 min | 20-24 min | 30-36 min |

> **⚠️ Nota:** Tempos podem variar com velocidade da internet e disponibilidade dos PDFs

---

## ❓ Problemas Comuns

### 🖥️ **Interface não abre**

```bash
# Reinstale dependências
uv sync --reinstall

# Verifique versão do Python (mínimo 3.10)
python --version
```

### 🌐 **Chromium não instalado**

```bash
uv run playwright install chromium
```

### 🔒 **Permission denied (Linux/Mac)**

```bash
chmod +x start.sh
chmod +x dev.sh
```

### 📥 **PDFs não baixam**

- ✅ Verifique conexão com internet
- ✅ Alguns livros podem não estar disponíveis online
- ✅ Tente nível "Completo" para mais tentativas
- ✅ Verifique logs no terminal para erros específicos

### 💾 **"Nenhum PDF encontrado" no ZIP**

- Os PDFs são salvos em `bibliografia_pdf/`
- Verifique se a busca encontrou algum sucesso
- Confirme que os arquivos têm mais de 50 páginas

### 🐧 **Linux: Erro de EGL/Mesa**

```
libEGL warning: failed to get driver name for fd -1
MESA: error: ZINK: failed to choose pdev
```

**Solução:** Esses avisos são do sistema gráfico e **não afetam** o funcionamento. Pode ignorar.

---

## 📁 Estrutura do Projeto

```
Crawler/
├── app.py                      # Interface gráfica Flet
├── main.py                     # Motor de busca e crawler
├── pyproject.toml              # Configuração do projeto (uv)
├── requirements.txt            # Dependências (compatibilidade pip)
├── README.md                   # Documentação completa
├── start.sh                    # Script de setup automatizado (Linux/Mac)
├── dev.sh                      # Script de desenvolvimento com hot reload
├── dev_watch.py                # Watchdog para auto-reload avançado
├── exemplo_lista.txt           # Exemplos de listas de livros
└── bibliografia_pdf/           # PDFs baixados (criado automaticamente)
```

### 📦 Dependências Principais

- **flet** ≥ 0.23.2 - Framework UI multiplataforma
- **playwright** - Automação de navegador
- **playwright-stealth** - Anti-detecção de bots
- **fake-useragent** - Rotação de user-agents
- **pymupdf** ≥ 1.26.7 - Validação de PDFs

---

## 🔥 Desenvolvimento

### 🛠️ Modo Desenvolvimento

**Opção 1: Hot Reload Nativo (Recomendado)**
```bash
uv run python app.py --hot-reload
```

**Opção 2: Script Automatizado**
```bash
chmod +x dev.sh
./dev.sh
```

**Opção 3: Watchdog Avançado**
```bash
uv sync --extra dev
uv run python dev_watch.py
```

> **💡 Hot Reload:** Modificações em arquivos `.py` são detectadas automaticamente e a aplicação reinicia

### 📝 Dependências de Desenvolvimento

```bash
uv sync --extra dev
```

Adiciona:
- **watchdog** ≥ 3.0.0 - Monitor de arquivos para auto-reload

### 🏗️ Build para Produção

**Desktop (Windows/Linux/macOS):**
```bash
flet build windows
flet build linux
flet build macos
```

**Android APK:**
```bash
flet build apk
```

**Web:**
```bash
flet build web
```

---

## 📊 Resultados e Estatísticas

### ✅ **O que é considerado Sucesso?**

- PDF encontrado e baixado
- Arquivo válido (não corrompido)
- **Mínimo 50 páginas** (evita fragmentos e resumos)

### ❌ **O que causa Falha?**

- Nenhum PDF encontrado nas buscas
- PDF encontrado mas com menos de 50 páginas
- Erro de download ou arquivo corrompido
- Timeout de conexão

### 📈 **Taxa de Sucesso Esperada**

| Tipo de Bibliografia | Taxa de Sucesso |
|----------------------|-----------------|
| Livros didáticos populares | 70-90% |
| Livros técnicos recentes | 50-70% |
| Livros raros ou antigos | 20-40% |
| Artigos científicos | 30-50% |

> **💡 Dica:** Use nível "Completo" para aumentar chances em livros raros

---

## 🌟 Recursos Avançados

### 🎨 **Interface**

- **Auto-scroll**: Rola automaticamente para progresso e resultados
- **Containers dinâmicos**: Sucessos/Falhas aparecem apenas quando há itens
- **Cancelamento**: Pare a busca a qualquer momento sem perder resultados parciais
- **Seleção de pasta**: Escolha onde salvar o ZIP
- **Mensagens contextuais**: Status coloridos (azul = info, verde = sucesso, vermelho = erro)

### 🔍 **Busca Inteligente**

- **Processamento de lista**: Remove automaticamente:
  - Marcadores (-, *, •, >, |, #)
  - Numeração (1., 2), [3])
  - Espaços extras
  - Linhas muito curtas (< 10 caracteres)
  
- **Debug mode**: Terminal mostra lista exata sendo processada

### 📦 **Download e Organização**

- Todos os PDFs em `bibliografia_pdf/`
- Nomes sanitizados (sem caracteres especiais)
- ZIP com timestamp: `bibliografia_YYYYMMDD_HHMMSS.zip`
- Evita re-download de arquivos existentes

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

- 🐛 Reportar bugs
- 💡 Sugerir novas funcionalidades
- 🔧 Enviar pull requests
- 📖 Melhorar documentação

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🎉 Pronto para Começar?

```bash
# Instalação rápida
./start.sh

# Ou manual
uv sync
uv run playwright install chromium
uv run python app.py
```

**Happy Crawling! 📚🤖**
