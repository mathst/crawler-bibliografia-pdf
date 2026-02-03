#!/bin/bash

# Script para build Linux
# AVISO: Requer dependências do sistema instaladas!

echo "🐧 Construindo executável para Linux..."
echo ""

# Verifica dependências necessárias
MISSING_DEPS=()

if ! command -v clang++ &> /dev/null; then
    MISSING_DEPS+=("clang++")
fi

if ! command -v cmake &> /dev/null; then
    MISSING_DEPS+=("cmake")
fi

if ! command -v ninja &> /dev/null; then
    MISSING_DEPS+=("ninja-build")
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo "⚠️  Dependências faltando: ${MISSING_DEPS[*]}"
    echo ""
    echo "📌 Instale com:"
    echo "   sudo apt install ${MISSING_DEPS[*]} libgtk-3-dev mesa-utils"
    echo ""
    echo "💡 ALTERNATIVA: Use build_web.sh para criar versão web (funciona sem dependências)"
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

# Build do executável Linux
echo "📦 Gerando executável..."
echo "⏳ Isso pode demorar... (Flutter SDK será baixado se necessário)"
echo ""
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
