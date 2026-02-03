#!/bin/bash

# Script para build Android APK
# Requer: Python 3.10+, Flet, Android SDK

echo "🤖 Construindo APK para Android..."
echo ""

# Verifica se flet está instalado
if ! command -v flet &> /dev/null; then
    echo "❌ Flet não encontrado. Instalando..."
    uv sync
fi

# Build do APK
echo "📦 Gerando APK..."
uv run flet build apk

echo ""
if [ -d "build/apk" ]; then
    echo "✅ APK criado com sucesso!"
    echo "📂 Localização: build/apk/"
    ls -lh build/apk/*.apk 2>/dev/null || echo "   (verifique a pasta build/apk/)"
else
    echo "❌ Erro ao criar APK"
    exit 1
fi
