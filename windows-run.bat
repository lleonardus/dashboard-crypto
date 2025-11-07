@echo off
set VENV_NAME=venv
set APP_FILE=app.py
set VENV_PYTHON="%VENV_NAME%\Scripts\python"
chcp 65001 >nul

echo ===========================================
echo   🚀 INICIANDO APLICACAO STREAMLIT 
echo ===========================================

REM 1. Verifica se o Python global esta acessivel de forma silenciosa.
REM Este bloco pode gerar o erro 'ho' visualmente, mas permite a execucao.
python -c "" >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado no PATH global.
    pause
    exit /b
)

REM 2. Cria o ambiente virtual se ele nao existir
if not exist "%VENV_NAME%" (
    echo [INFO] Criando ambiente virtual '%VENV_NAME%'...
    python -m venv "%VENV_NAME%"
)

REM 3. Instala dependencias usando o Python do VENV
REM A chamada direta (python -m) garante que Streamlit seja encontrado
echo [INFO] Instalando/Verificando dependencias...
if exist "requirements.txt" (
    %VENV_PYTHON% -m pip install --upgrade pip >nul
    %VENV_PYTHON% -m pip install -r requirements.txt
) else (
    echo [AVISO] requirements.txt nao encontrado. Pulando instalacao.
)

REM 4. Executa o Streamlit de forma robusta
echo.
echo [INFO] Iniciando Streamlit...
REM Chamando o Streamlit via modulo Python do VENV
%VENV_PYTHON% -m streamlit run "%APP_FILE%"

echo.
echo ===========================================
echo   Execucao encerrada.
echo ===========================================
pause >nul