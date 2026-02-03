# 📦 Guia de Build - Bibliografia Crawler

## 🎯 Resumo Rápido

### ✅ Recomendado: Versão WEB
```bash
./build_web.sh
```
- Funciona em **qualquer plataforma** (Windows, Linux, macOS, Android, iOS)
- Não precisa instalar nada no dispositivo do usuário
- Acessa pelo navegador
- Mais leve e rápido de gerar

### 📱 Outras Opções

```bash
./build.sh  # Menu interativo com todas as opções
```

---

## 🌐 Build WEB (Recomendado)

**Vantagens:**
- ✅ Funciona em qualquer dispositivo com navegador
- ✅ Não precisa Flutter SDK ou dependências extras
- ✅ Fácil de hospedar (GitHub Pages, Netlify, Vercel)
- ✅ Atualizações instantâneas (sem reinstalar)

**Como usar:**
```bash
./build_web.sh
cd build/web
python -m http.server 8000
# Acesse: http://localhost:8000
```

**Deploy:**
- GitHub Pages: Faça push da pasta `build/web`
- Netlify/Vercel: Conecte o repositório
- Servidor próprio: Copie `build/web` para `/var/www/html`

---

## 🪟 Build Windows

⚠️ **IMPORTANTE:** 
- Deve ser executado **no Windows** (PowerShell/CMD), **NÃO no WSL**
- Ou use WSL mas vai precisar das ferramentas Linux + Flutter

**No Windows:**
```powershell
# No PowerShell do Windows (não no WSL!)
cd caminho\para\o\projeto
uv run flet build windows
```

**Requisitos:**
- Windows 10/11
- Python 3.10+
- uv instalado
- Flutter SDK (será baixado automaticamente)

**Resultado:**
- Executável: `build/windows/app.exe`
- Tamanho: ~80-150 MB

---

## 🐧 Build Linux

**Requisitos do Sistema:**
```bash
sudo apt install clang++ cmake ninja-build libgtk-3-dev mesa-utils
```

**Build:**
```bash
./build_linux.sh
```

**Resultado:**
- Executável: `build/linux/app`
- Executar: `cd build/linux && ./app`

---

## 🤖 Build Android APK

⚠️ **Complexo!** Requer Android SDK completo.

**Requisitos:**
- Android SDK instalado
- Java JDK 11+
- Variável `ANDROID_HOME` configurada
- ~10-20 GB de espaço em disco

**Build:**
```bash
./build_android.sh
```

**Resultado:**
- APK: `build/apk/app.apk`
- Instalar: `adb install build/apk/app.apk`

---

## 🚀 Build Múltiplas Plataformas

```bash
./build.sh
# Escolha opção 5 (Todas as plataformas)
```

⚠️ Apenas faça isso se tiver **TODAS** as dependências instaladas.

---

## 💡 Qual escolher?

| Cenário | Recomendação |
|---------|--------------|
| **Distribuição rápida** | 🌐 WEB |
| **Uso interno/teste** | 🌐 WEB ou executar direto com Python |
| **App desktop profissional** | 🪟 Windows ou 🐧 Linux (na plataforma nativa) |
| **App mobile** | 🌐 WEB (Progressive Web App) |
| **Offline completo** | 🪟 Windows / 🐧 Linux / 🤖 Android |

---

## 🔧 Troubleshooting

### "Flutter SDK not found"
Normal! Será baixado automaticamente (~800 MB). Aguarde.

### "Build failed" no WSL
Use `build_web.sh` ou execute o build Windows no PowerShell do Windows.

### "Android SDK not found"
Instale o Android Studio primeiro, depois configure `ANDROID_HOME`.

### Muito devagar?
Use `build_web.sh` - é 10x mais rápido que builds nativos.

---

## 📊 Comparação

| Tipo | Tamanho | Tempo Build | Requisitos | Dificuldade |
|------|---------|-------------|------------|-------------|
| WEB | ~5 MB | 1-2 min | Nenhum extra | ⭐ Fácil |
| Windows | ~100 MB | 10-15 min | Flutter SDK | ⭐⭐⭐ Médio |
| Linux | ~80 MB | 10-15 min | clang, cmake, gtk | ⭐⭐⭐ Médio |
| Android | ~30 MB | 20-30 min | Android SDK | ⭐⭐⭐⭐⭐ Difícil |

---

## 🎓 Executar sem Build

**Para desenvolvimento ou uso pessoal:**
```bash
uv run python app.py
```

Mais rápido e não precisa fazer build!
