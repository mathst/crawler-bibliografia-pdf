# 🪟 Como Fazer Build no Windows

## ✅ O que você precisa instalar

### 1. Python 3.10 ou superior

**Download:**
- Acesse: https://www.python.org/downloads/
- Baixe Python 3.10+ (ou 3.11, 3.12)
- ⚠️ **IMPORTANTE**: Marque "Add Python to PATH" durante instalação

**Verificar se instalou:**
```powershell
python --version
# Deve mostrar: Python 3.10.x ou superior
```

---

### 2. uv (Gerenciador de pacotes - Rápido!)

**Instalação no Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Ou via pip:**
```powershell
pip install uv
```

**Verificar:**
```powershell
uv --version
```

---

### 3. Git (Opcional - para baixar o projeto)

**Download:**
- https://git-scm.com/download/win
- Instale com configurações padrão

---

## 📥 Como pegar o projeto do WSL para Windows

### Opção 1: Acessar pasta do WSL direto no Windows

```powershell
# No Explorador de Arquivos do Windows, digite:
\\wsl$\Ubuntu\home\SEU_USUARIO\docs\projPython\Crawler

# Ou via PowerShell:
cd \\wsl$\Ubuntu\home\SEU_USUARIO\docs\projPython\Crawler
```

### Opção 2: Copiar para Windows

```powershell
# Copiar do WSL para Windows
xcopy \\wsl$\Ubuntu\home\SEU_USUARIO\docs\projPython\Crawler C:\MeusProjetos\Crawler /E /I
cd C:\MeusProjetos\Crawler
```

---

## 🚀 Fazer o Build

### Passo 1: Instalar dependências

```powershell
# No PowerShell, dentro da pasta do projeto:
cd caminho\para\Crawler

# Instalar dependências Python
uv sync
```

### Passo 2: Gerar o EXE

```powershell
# Build Windows
uv run flet build windows
```

⏳ **Atenção:**
- Na **primeira vez**, vai baixar o Flutter SDK (~800 MB)
- Pode demorar **10-20 minutos**
- Nas próximas vezes será mais rápido

### Passo 3: Executável estará pronto!

```
📂 Localização: build\windows\
📄 Arquivo: app.exe (ou nome do projeto)
💾 Tamanho: ~80-150 MB
```

---

## 🎯 Resumo Completo

### No Windows (PowerShell como Administrador):

```powershell
# 1. Instalar Python (se não tiver)
# Baixar de python.org e instalar

# 2. Instalar uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 3. Navegar até o projeto
cd \\wsl$\Ubuntu\home\SEU_USUARIO\docs\projPython\Crawler
# OU
cd C:\caminho\onde\copiou\Crawler

# 4. Instalar dependências
uv sync

# 5. Fazer build
uv run flet build windows

# 6. Executável estará em: build\windows\
```

---

## ⚡ Versão Rápida (Para testar antes do build)

```powershell
# Rodar direto sem fazer build:
uv run python app.py
```

Isso abre o app imediatamente, sem precisar esperar o build!

---

## 🔧 Troubleshooting

### "Python não encontrado"
**Solução:**
1. Reinstale Python marcando "Add to PATH"
2. Ou adicione manualmente: `C:\Python310` ao PATH

### "uv não encontrado"
**Solução:**
1. Reinicie o PowerShell após instalar
2. Ou use: `python -m pip install uv`

### "Build muito lento"
**Solução:**
- É normal na primeira vez (baixa Flutter SDK)
- Use `uv run python app.py` para testar sem build

### "Erro ao baixar Flutter"
**Solução:**
- Verifique conexão com internet
- Desative antivírus temporariamente
- Tente novamente: `uv run flet build windows`

---

## 📊 Comparação de Opções

| Método | Tempo | Tamanho | Instalação Usuario |
|--------|-------|---------|-------------------|
| **Executar direto** (`uv run python app.py`) | 5 seg | - | Precisa Python |
| **Build EXE** (`flet build windows`) | 10-20 min | ~100 MB | Não precisa nada |

---

## 💡 Recomendação

**Para você:**
1. Instale Python + uv no Windows
2. Acesse a pasta do projeto via `\\wsl$\...`
3. Rode `uv sync` uma vez
4. Faça o build: `uv run flet build windows`

**Resultado:**
- Um arquivo `.exe` que roda em qualquer Windows
- Sem precisar Python instalado no PC do usuário final
- Pronto para distribuir!

---

## 🎓 Checklist

- [ ] Python 3.10+ instalado no Windows
- [ ] uv instalado (`uv --version` funciona)
- [ ] Navegou até pasta do projeto
- [ ] Rodou `uv sync` com sucesso
- [ ] Executou `uv run flet build windows`
- [ ] Encontrou o EXE em `build\windows\`

Pronto! 🎉
