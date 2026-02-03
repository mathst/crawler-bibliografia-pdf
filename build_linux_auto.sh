#!/bin/bash

# Script de build automatizado para Linux
# Instala tudo que precisa e faz o build

set -e  # Para na primeira falha

echo "🐧 BUILD AUTOMATIZADO - LINUX"
echo "=============================="
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Detectar distribuição
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    DISTRO="unknown"
fi

# 1. Verificar/Instalar Python
echo -e "${YELLOW}🐍 Verificando Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}   ✅ Python já instalado: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}   ❌ Python não encontrado!${NC}"
    echo -e "${YELLOW}   📥 Instalando Python...${NC}"
    
    case $DISTRO in
        ubuntu|debian)
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv
            ;;
        fedora|rhel|centos)
            sudo dnf install -y python3 python3-pip
            ;;
        arch|manjaro)
            sudo pacman -S --noconfirm python python-pip
            ;;
        *)
            echo -e "${RED}   ⚠️  Distribuição não reconhecida. Instale Python manualmente.${NC}"
            exit 1
            ;;
    esac
    
    echo -e "${GREEN}   ✅ Python instalado!${NC}"
fi

echo ""

# 2. Verificar/Instalar uv
echo -e "${YELLOW}📦 Verificando uv...${NC}"
if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version)
    echo -e "${GREEN}   ✅ uv já instalado: $UV_VERSION${NC}"
else
    echo -e "${RED}   ❌ uv não encontrado!${NC}"
    echo -e "${YELLOW}   📥 Instalando uv...${NC}"
    
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Adicionar ao PATH da sessão atual
    export PATH="$HOME/.cargo/bin:$PATH"
    
    echo -e "${GREEN}   ✅ uv instalado!${NC}"
fi

echo ""

# 3. Instalar dependências do sistema para build Linux
echo -e "${YELLOW}🔧 Verificando dependências do sistema...${NC}"

MISSING_DEPS=()

if ! command -v clang++ &> /dev/null; then
    MISSING_DEPS+=("clang")
fi

if ! command -v cmake &> /dev/null; then
    MISSING_DEPS+=("cmake")
fi

if ! command -v ninja &> /dev/null; then
    MISSING_DEPS+=("ninja-build")
fi

if ! pkg-config --exists gtk+-3.0 2>/dev/null; then
    MISSING_DEPS+=("libgtk-3-dev")
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo -e "${YELLOW}   📥 Instalando dependências do sistema: ${MISSING_DEPS[*]}${NC}"
    
    case $DISTRO in
        ubuntu|debian)
            sudo apt update
            sudo apt install -y clang cmake ninja-build libgtk-3-dev mesa-utils pkg-config
            ;;
        fedora|rhel|centos)
            sudo dnf install -y clang cmake ninja-build gtk3-devel mesa-utils
            ;;
        arch|manjaro)
            sudo pacman -S --noconfirm clang cmake ninja gtk3 mesa
            ;;
        *)
            echo -e "${RED}   ⚠️  Instale manualmente: ${MISSING_DEPS[*]}${NC}"
            ;;
    esac
    
    echo -e "${GREEN}   ✅ Dependências do sistema instaladas!${NC}"
else
    echo -e "${GREEN}   ✅ Todas as dependências já instaladas!${NC}"
fi

echo ""

# 4. Instalar dependências do projeto
echo -e "${YELLOW}📚 Instalando dependências do projeto...${NC}"
uv sync
echo -e "${GREEN}   ✅ Dependências instaladas!${NC}"

echo ""

# 5. Fazer o build
echo -e "${YELLOW}🏗️  Iniciando build do executável...${NC}"
echo -e "${CYAN}   ⏳ Isso pode demorar 10-20 minutos na primeira vez...${NC}"
echo -e "${CYAN}   (Flutter SDK será baixado automaticamente)${NC}"
echo ""

uv run flet build linux

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}==============================${NC}"
    echo -e "${GREEN}✅ BUILD CONCLUÍDO COM SUCESSO!${NC}"
    echo -e "${GREEN}==============================${NC}"
    echo ""
    echo -e "${CYAN}📂 Executável criado em: build/linux/${NC}"
    echo ""
    
    # Listar arquivos gerados
    if [ -d "build/linux" ]; then
        echo -e "${YELLOW}📄 Arquivos gerados:${NC}"
        find build/linux -type f -executable -exec ls -lh {} \; | awk '{printf "   • %s (%s)\n", $9, $5}'
    fi
    
    echo ""
    echo -e "${YELLOW}Para executar:${NC}"
    echo -e "${CYAN}   cd build/linux${NC}"
    echo -e "${CYAN}   ./<nome_do_executavel>${NC}"
    echo ""
    echo -e "${GREEN}🎉 Pronto para distribuir!${NC}"
else
    echo ""
    echo -e "${RED}❌ ERRO AO CRIAR EXECUTÁVEL${NC}"
    echo ""
    echo -e "${YELLOW}💡 Possíveis soluções:${NC}"
    echo "   1. Verifique sua conexão com internet"
    echo "   2. Execute com sudo se necessário"
    echo "   3. Tente: uv run python app.py (para testar sem build)"
    exit 1
fi
