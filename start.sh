#!/bin/bash
# Script de instalação e execução rápida

echo "📚 Bibliografia Crawler - Instalação"
echo "===================================="
echo ""

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale Python 3.10+ primeiro."
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Verifica uv
if ! command -v uv &> /dev/null; then
    echo "⚠️  uv não encontrado. Instalando..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "✅ uv encontrado: $(uv --version)"
echo ""

# Instala dependências
echo "📦 Instalando dependências..."
uv sync

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

echo "✅ Dependências instaladas"
echo ""

# Instala Chromium do Playwright
echo "🌐 Instalando navegador Chromium..."
uv run playwright install chromium

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar Chromium"
    exit 1
fi

echo "✅ Chromium instalado"
echo ""

# Executa a aplicação
echo "🚀 Iniciando interface gráfica..."
echo ""
uv run python app.py
