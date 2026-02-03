# 🚀 Scripts de Build Automatizados

**NOVIDADE:** Agora os scripts instalam TUDO automaticamente!

## 🪟 Windows - Build Automático

### Passo único:

```powershell
# Abra PowerShell como Administrador
# Clique direito no PowerShell > Executar como Administrador

# Execute:
.\build_windows_auto.ps1
```

### O que ele faz automaticamente:

1. ✅ Verifica se Python está instalado
   - Se não estiver, **baixa e instala Python 3.11**
2. ✅ Verifica se uv está instalado
   - Se não estiver, **instala automaticamente**
3. ✅ Instala todas as dependências do projeto
4. ✅ Baixa Flutter SDK (se necessário)
5. ✅ Faz o build do executável
6. ✅ Mostra onde o `.exe` foi criado

**Resultado:** Executável pronto em `build\windows\`

---

## 🐧 Linux - Build Automático

### Passo único:

```bash
chmod +x build_linux_auto.sh
./build_linux_auto.sh
```

### O que ele faz automaticamente:

1. ✅ Detecta sua distribuição (Ubuntu, Fedora, Arch, etc.)
2. ✅ Instala Python (se necessário)
3. ✅ Instala uv automaticamente
4. ✅ Instala dependências do sistema:
   - clang, cmake, ninja-build
   - libgtk-3-dev, mesa-utils
5. ✅ Instala dependências do projeto
6. ✅ Baixa Flutter SDK (se necessário)
7. ✅ Faz o build do executável

**Resultado:** Executável pronto em `build/linux/`

---

## 💻 WSL - Apenas Executar (Sem Build)

No WSL, **não precisa fazer build**. Execute direto:

```bash
# Instala uv (primeira vez):
curl -LsSf https://astral.sh/uv/install.sh | sh

# Adiciona ao PATH (primeira vez):
export PATH="$HOME/.cargo/bin:$PATH"

# Executa o app:
uv run python app.py
```

Pronto! Abre em 5 segundos. ⚡

---

## ⏱️ Quanto tempo demora?

| Plataforma | Primeira Vez | Próximas Vezes |
|------------|-------------|----------------|
| Windows | 15-25 min | 2-5 min |
| Linux | 15-25 min | 2-5 min |
| WSL (executar) | 5 seg | 2 seg |

**Por que demora na primeira vez?**
- Baixa Flutter SDK (~800 MB)
- Compila todas as dependências
- Cria executável standalone

---

## 📋 Requisitos Mínimos

### Windows:
- Windows 10/11
- 2 GB de RAM livre
- 2 GB de espaço em disco
- Conexão com internet

**NADA MAIS!** O script instala o resto.

### Linux:
- Ubuntu 20.04+, Fedora 35+, Arch, ou similar
- 2 GB de RAM livre
- 2 GB de espaço em disco
- Conexão com internet
- Permissões sudo (para instalar dependências)

**NADA MAIS!** O script instala o resto.

---

## 🎯 Comparação: Scripts Antigos vs Novos

| Tipo | Script Antigo | Script Novo (Auto) |
|------|---------------|-------------------|
| **Windows** | `build_windows.sh` | `build_windows_auto.ps1` ✨ |
| | Precisa instalar tudo manual | **Instala tudo sozinho** |
| **Linux** | `build_linux.sh` | `build_linux_auto.sh` ✨ |
| | Precisa instalar deps manual | **Instala tudo sozinho** |

---

## 💡 Recomendações por Caso

### Caso 1: "Quero distribuir o app para outras pessoas"
**Use:** `build_windows_auto.ps1` (Windows) ou `build_linux_auto.sh` (Linux)
- Gera executável standalone
- Usuário final não precisa instalar nada

### Caso 2: "Quero só testar rápido"
**Use:** `uv run python app.py`
- Abre em segundos
- Não precisa fazer build

### Caso 3: "Estou no WSL"
**Use:** `uv run python app.py`
- WSL não é ideal para builds
- Executar direto é mais rápido

### Caso 4: "Quero app web para qualquer plataforma"
**Use:** `uv run flet build web`
- Funciona em Windows, Linux, Android, iOS
- Acessa pelo navegador

---

## 🆘 Troubleshooting

### Windows: "Não pode executar scripts"
**Solução:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\build_windows_auto.ps1
```

### Linux: "Permission denied"
**Solução:**
```bash
chmod +x build_linux_auto.sh
./build_linux_auto.sh
```

### Geral: "Build muito lento"
**É normal na primeira vez!** Está baixando Flutter SDK (~800 MB).

### Geral: "Erro de conexão"
- Verifique internet
- Desative VPN se tiver
- Tente novamente

---

## ✨ Exemplo Completo - Windows

```powershell
# 1. Abra PowerShell como Administrador

# 2. Navegue até a pasta do projeto
cd C:\MeusProjetos\Crawler

# 3. Execute o script automático
.\build_windows_auto.ps1

# 4. Aguarde... (15-25 min na primeira vez)

# 5. Pronto! Executável em: build\windows\app.exe
```

**Simples assim!** 🎉

---

## ✨ Exemplo Completo - Linux

```bash
# 1. Navegue até a pasta do projeto
cd ~/projetos/Crawler

# 2. Dê permissão de execução
chmod +x build_linux_auto.sh

# 3. Execute o script automático
./build_linux_auto.sh

# 4. Digite sua senha sudo quando pedir (para instalar dependências)

# 5. Aguarde... (15-25 min na primeira vez)

# 6. Pronto! Execute com:
cd build/linux
./<nome_do_executavel>
```

**Simples assim!** 🎉
