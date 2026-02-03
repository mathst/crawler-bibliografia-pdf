# Script de build automatizado para Windows
# Instala tudo que precisa e faz o build

Write-Host "🪟 BUILD AUTOMATIZADO - WINDOWS" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Função para verificar se comando existe
function Test-Command {
    param($Command)
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            return $true
        }
    }
    catch {
        return $false
    }
}

# 1. Verificar/Instalar Python
Write-Host "🐍 Verificando Python..." -ForegroundColor Yellow
if (Test-Command python) {
    $pythonVersion = python --version
    Write-Host "   ✅ Python já instalado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "   ❌ Python não encontrado!" -ForegroundColor Red
    Write-Host "   📥 Baixando Python 3.11..." -ForegroundColor Yellow
    
    $pythonUrl = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    $pythonInstaller = "$env:TEMP\python-installer.exe"
    
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
    
    Write-Host "   🔧 Instalando Python (aguarde)..." -ForegroundColor Yellow
    Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
    
    Remove-Item $pythonInstaller
    
    # Atualizar ambiente
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Host "   ✅ Python instalado!" -ForegroundColor Green
}

Write-Host ""

# 2. Verificar/Instalar uv
Write-Host "📦 Verificando uv..." -ForegroundColor Yellow
if (Test-Command uv) {
    $uvVersion = uv --version
    Write-Host "   ✅ uv já instalado: $uvVersion" -ForegroundColor Green
} else {
    Write-Host "   ❌ uv não encontrado!" -ForegroundColor Red
    Write-Host "   📥 Instalando uv..." -ForegroundColor Yellow
    
    try {
        Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
        
        # Atualizar ambiente
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        Write-Host "   ✅ uv instalado!" -ForegroundColor Green
    }
    catch {
        Write-Host "   ⚠️  Instalação automática falhou. Instalando via pip..." -ForegroundColor Yellow
        python -m pip install uv
        Write-Host "   ✅ uv instalado via pip!" -ForegroundColor Green
    }
}

Write-Host ""

# 3. Instalar dependências do projeto
Write-Host "📚 Instalando dependências do projeto..." -ForegroundColor Yellow
uv sync
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Dependências instaladas!" -ForegroundColor Green
} else {
    Write-Host "   ❌ Erro ao instalar dependências" -ForegroundColor Red
    exit 1
}

Write-Host ""

# 4. Fazer o build
Write-Host "🏗️  Iniciando build do executável..." -ForegroundColor Yellow
Write-Host "   ⏳ Isso pode demorar 10-20 minutos na primeira vez..." -ForegroundColor Cyan
Write-Host "   (Flutter SDK será baixado automaticamente)" -ForegroundColor Cyan
Write-Host ""

uv run flet build windows

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "✅ BUILD CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📂 Executável criado em: build\windows\" -ForegroundColor Cyan
    Write-Host ""
    
    # Listar arquivos gerados
    if (Test-Path "build\windows") {
        Write-Host "📄 Arquivos gerados:" -ForegroundColor Yellow
        Get-ChildItem "build\windows" -Recurse -Include *.exe | ForEach-Object {
            $size = [math]::Round($_.Length / 1MB, 2)
            Write-Host "   • $($_.Name) ($size MB)" -ForegroundColor White
        }
    }
    
    Write-Host ""
    Write-Host "🎉 Pronto para distribuir!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ ERRO AO CRIAR EXECUTÁVEL" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Possíveis soluções:" -ForegroundColor Yellow
    Write-Host "   1. Verifique sua conexão com internet" -ForegroundColor White
    Write-Host "   2. Execute como Administrador" -ForegroundColor White
    Write-Host "   3. Desative antivírus temporariamente" -ForegroundColor White
    Write-Host "   4. Tente: uv run python app.py (para testar sem build)" -ForegroundColor White
    exit 1
}
