@echo off
REM ======================================================
REM Script para gerar o executável do Sistema de Estoque
REM ======================================================

echo.
echo ========================================
echo  Gerando Executavel - Sistema de Estoque
echo ========================================
echo.

REM Verificar se PyInstaller está instalado
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [ERRO] PyInstaller não está instalado!
    echo Instalando PyInstaller...
    python -m pip install pyinstaller
)

REM Limpar builds anteriores
echo.
echo [1/3] Limpando arquivos antigos...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo [✓] Limpeza concluída

REM Gerar o executável
echo.
echo [2/3] Gerando executável (isto pode levar alguns minutos)...
pyinstaller build.spec
if errorlevel 1 (
    echo [X] Erro ao gerar o executável!
    pause
    exit /b 1
)
echo [✓] Executável gerado com sucesso!

REM Resultado
echo.
echo ========================================
echo  SUCESSO!
echo ========================================
echo.
echo O arquivo "Sistema_Estoque.exe" foi criado em:
echo   dist\Sistema_Estoque.exe
echo.
echo Voce pode:
echo   1. Copiar esta pasta para o PC da cliente
echo   2. Dar dois cliques no Sistema_Estoque.exe
echo   3. O sistema vai rodar normalmente!
echo.
pause
