#!/bin/bash

# Script para build Windows EXE
# Requer: Python 3.10+, Flet

echo "🪟 Construindo executável para Windows..."
echo ""

# Verifica se flet está instalado
if ! command -v flet &> /dev/null; then
    echo "❌ Flet não encontrado. Instalando..."
    uv sync
fi

# Build do EXE
echo "📦 Gerando EXE..."
uv run flet build windows

echo ""
if [ -d "build/windows" ]; then
    echo "✅ Executável Windows criado com sucesso!"
    echo "📂 Localização: build/windows/"
else
    echo "❌ Erro ao criar executável"
    exit 1
fi
