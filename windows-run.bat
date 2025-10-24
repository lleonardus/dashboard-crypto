@echo off
chcp 65001 >nul
title Iniciando Aplicação Streamlit
color 0A
cls

echo ===================================================
echo       🚀 INICIALIZANDO AMBIENTE STREAMLIT
echo ===================================================

REM Configurações
set VENV_NAME=venv
set REQUIREMENTS=requirements.txt
set APP_FILE=app.py

REM --------------------------------------------
REM Verifica se o Python está instalado
REM --------------------------------------------
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não está instalado ou não está no PATH.
    echo Instale o Python e tente novamente.
    pause
    exit /b
)

REM --------------------------------------------
REM Cria o ambiente virtual, se não existir
REM --------------------------------------------
if not exist "%VENV_NAME%" (
    echo [INFO] Criando ambiente virtual...
    python -m venv "%VENV_NAME%"
)

REM --------------------------------------------
REM Ativa o ambiente virtual
REM --------------------------------------------
call "%VENV_NAME%\Scripts\activate"

REM --------------------------------------------
REM Atualiza o pip
REM --------------------------------------------
echo [INFO] Atualizando o pip...
python -m pip install --upgrade pip >nul

REM --------------------------------------------
REM Instala dependências
REM --------------------------------------------
if exist "%REQUIREMENTS%" (
    echo [INFO] Instalando dependências...
    pip install -r "%REQUIREMENTS%"
) else (
    echo [AVISO] O arquivo "%REQUIREMENTS%" não foi encontrado. Pulando instalação.
)

REM --------------------------------------------
REM Executa o Streamlit
REM --------------------------------------------
echo.
echo ===================================================
echo       🟢 INICIANDO A APLICAÇÃO STREAMLIT
echo ===================================================
echo.

streamlit run "%APP_FILE%"

echo.
echo ===================================================
echo Execução encerrada. Pressione qualquer tecla para sair.
echo ===================================================
pause >nul