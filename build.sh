#!/bin/bash

# Script universal de build - Constrói para todas as plataformas
echo "🚀 BIBLIOGRAFIA CRAWLER - BUILD MULTIPLATAFORMA"
echo "================================================"
echo ""

# Menu de seleção
echo "Selecione a plataforma:"
echo "  1) Android APK"
echo "  2) Android AAB (Google Play)"
echo "  3) Windows EXE"
echo "  4) Linux"
echo "  5) Todas as plataformas"
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
        
        chmod +x build_android.sh build_windows.sh build_linux.sh
        
        echo "1/4 - Android APK..."
        ./build_android.sh
        
        echo ""
        echo "2/4 - Android AAB..."
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
