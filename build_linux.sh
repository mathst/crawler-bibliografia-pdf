#!/bin/bash

# Script para build Linux
# Requer: Python 3.10+, Flet

echo "🐧 Construindo executável para Linux..."
echo ""

# Verifica se flet está instalado
if ! command -v flet &> /dev/null; then
    echo "❌ Flet não encontrado. Instalando..."
    uv sync
fi

# Build do executável Linux
echo "📦 Gerando executável..."
uv run flet build linux

echo ""
if [ -d "build/linux" ]; then
    echo "✅ Executável Linux criado com sucesso!"
    echo "📂 Localização: build/linux/"
    echo ""
    echo "Para executar:"
    echo "  cd build/linux"
    echo "  ./<nome_do_executavel>"
else
    echo "❌ Erro ao criar executável"
    exit 1
fi
