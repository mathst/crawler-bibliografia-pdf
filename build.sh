#!/bin/bash

# Script universal de build - Constrói para todas as plataformas
echo "🚀 BIBLIOGRAFIA CRAWLER - BUILD MULTIPLATAFORMA"
echo "================================================"
echo ""

# Detecta plataforma atual
if grep -qEi "(Microsoft|WSL)" /proc/version &> /dev/null 2>&1; then
    PLATAFORMA="WSL"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATAFORMA="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATAFORMA="macOS"
else
    PLATAFORMA="Desconhecida"
fi

echo "📍 Plataforma detectada: $PLATAFORMA"
echo ""
🌐 Construindo versão WEB..."
        chmod +x build_web.sh
        ./build_web.sh
        ;;
    2)
        echo ""
        echo "🤖 Construindo Android APK..."
        chmod +x build_android.sh
        ./build_android.shormas"
echo ""
read -p "Opção [1-5]: " opcao

case $opcao in
    1)
        echo ""
        echo "📱 Construindo Android APK..."
        chmod +x build_android.sh
        ./build_android.sh
        ;;
    2)
        echo ""
        echo "📱 Construindo Android AAB para Google Play..."
        uv run flet build aab
        ;;
    3)
        echo ""
        echo "🪟 Construindo Windows EXE..."
        chmod +x build_windows.sh
        ./build_windows.sh
        ;;
    4)
        echo ""
        echo "🐧 Construindo Linux..."
        chmod +x build_linux.sh
        ./build_linux.sh
        ;;
    5)
        echo ""
        echo "🌍 Construindo para TODAS as plataformas..."
        echo ""
        web.sh build_android.sh build_windows.sh build_linux.sh
        
        echo "1/4 - Versão WEB..."
        ./build_web.sh
        
        echo ""
        echo "2/4 - Android APK..."
        ./build_android.shAB..."
        uv run flet build aab
        
        echo ""
        echo "3/4 - Windows EXE..."
        ./build_windows.sh
        
        echo ""
        echo "4/4 - Linux..."
        ./build_linux.sh
        
        echo ""
        echo "✅ BUILD COMPLETO!"
        echo "📂 Todos os executáveis estão em: build/"
        ;;
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "================================================"
echo "✨ Build finalizado com sucesso!"
