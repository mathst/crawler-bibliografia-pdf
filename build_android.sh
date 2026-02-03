#!/bin/bash

# Script para build Android APK
# AVISO: Requer Android SDK instalado!

echo "🤖 Construindo APK para Android..."
echo ""

echo "⚠️  ATENÇÃO: Build Android requer:"
echo "   - Android SDK instalado"
echo "   - Java JDK 11+"
echo "   - Variáveis de ambiente configuradas (ANDROID_HOME)"
echo ""
echo "💡 ALTERNATIVA: Use build_web.sh para criar versão web (funciona em qualquer dispositivo)"
echo ""
read -p "Continuar? [y/N]: " resposta
if [[ ! "$resposta" =~ ^[Yy]$ ]]; then
    echo "❌ Build cancelado"
    exit 1
fi

# Verifica se flet está instalado
if ! command -v flet &> /dev/null; then
    echo "📦 Instalando Flet CLI..."
    uv sync
fi

# Build do APK
echo "📦 Gerando APK..."
echo "⏳ Isso pode demorar MUITO... (Flutter SDK e Android SDK serão configurados)"
echo ""
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
