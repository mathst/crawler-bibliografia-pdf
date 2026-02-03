#!/bin/bash

# Script para build WEB - Funciona em qualquer plataforma
echo "🌐 Construindo versão WEB..."
echo ""

# Verifica se flet está instalado
if ! command -v flet &> /dev/null; then
    echo "❌ Flet não encontrado. Instalando..."
    uv sync
fi

# Build da versão Web
echo "📦 Gerando aplicação WEB..."
uv run flet build web

echo ""
if [ -d "build/web" ]; then
    echo "✅ Versão WEB criada com sucesso!"
    echo "📂 Localização: build/web/"
    echo ""
    echo "Para testar:"
    echo "  cd build/web"
    echo "  python -m http.server 8000"
    echo "  Acesse: http://localhost:8000"
else
    echo "❌ Erro ao criar versão WEB"
    exit 1
fi
