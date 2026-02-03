#!/bin/bash

# Script para build Windows EXE
# AVISO: Este build deve ser executado no Windows, não no WSL!

echo "🪟 Construindo executável para Windows..."
echo ""

# Detecta se está rodando no WSL
if grep -qEi "(Microsoft|WSL)" /proc/version &> /dev/null ; then
    echo "⚠️  AVISO: Você está no WSL (Windows Subsystem for Linux)"
    echo "📌 Para criar EXE Windows, você precisa:"
    echo "   1. Abrir PowerShell ou CMD no Windows"
    echo "   2. Navegar até esta pasta"
    echo "   3. Executar: uv run flet build windows"
    echo ""
    echo "💡 ALTERNATIVA: Use build_web.sh para criar versão web (funciona em qualquer lugar)"
    echo ""
    read -p "Continuar mesmo assim? (pode falhar) [y/N]: " resposta
    if [[ ! "$resposta" =~ ^[Yy]$ ]]; then
        echo "❌ Build cancelado"
        exit 1
    fi
fi

# Verifica se flet está instalado
if ! command -v flet &> /dev/null; then
    echo "📦 Instalando Flet CLI..."
    uv sync
fi

# Build do EXE
echo "📦 Gerando EXE..."
echo "⏳ Isso pode demorar... (Flutter SDK será baixado se necessário)"
echo ""
uv run flet build windows

echo ""
if [ -d "build/windows" ]; then
    echo "✅ Executável Windows criado com sucesso!"
    echo "📂 Localização: build/windows/"
else
    echo "❌ Erro ao criar executável"
    exit 1
fi
