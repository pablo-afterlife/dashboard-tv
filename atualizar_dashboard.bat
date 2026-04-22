@echo off
setlocal EnableDelayedExpansion

:: ─────────────────────────────────────────────────────────────
::  Caminho da pasta do projeto (sem barra no final)
:: ─────────────────────────────────────────────────────────────
set "PROJ=C:\Users\Consultor\OneDrive - Aquila\SITE AQUILA\teste123\dashboard_tv_slides_pacote\dashboard_tv_slides_pacote"

:: Caminho do Excel fonte
set "XLSX=C:\Users\Consultor\Aquila\ADM - EGA - General\Arquivos Referencias\Escola\Andamento - Projetos.xlsx"

:: Log file (fica dentro da pasta do projeto)
set "LOG=%PROJ%\log_atualizacao.txt"

:: ─────────────────────────────────────────────────────────────
::  Garante que git e python estejam no PATH do Agendador
:: ─────────────────────────────────────────────────────────────
set "PATH=%PATH%;C:\Program Files\Git\cmd;C:\Program Files\Git\bin"
set "PATH=%PATH%;C:\Users\Consultor\AppData\Local\Programs\Python\Python312"
set "PATH=%PATH%;C:\Users\Consultor\AppData\Local\Programs\Python\Python311"
set "PATH=%PATH%;C:\Python312;C:\Python311;C:\Python310"

echo. >> "%LOG%"
echo ============================================================ >> "%LOG%"
echo [%date% %time%] INICIO >> "%LOG%"

:: ─────────────────────────────────────────────────────────────
::  Entrar na pasta do projeto
:: ─────────────────────────────────────────────────────────────
cd /d "%PROJ%"
if errorlevel 1 (
    echo [%date% %time%] ERRO: nao foi possivel acessar a pasta do projeto >> "%LOG%"
    exit /b 1
)
echo [%date% %time%] Pasta OK: %PROJ% >> "%LOG%"

:: ─────────────────────────────────────────────────────────────
::  Garantir que estamos na branch main
:: ─────────────────────────────────────────────────────────────
git checkout main >> "%LOG%" 2>&1
if errorlevel 1 (
    echo [%date% %time%] AVISO: nao conseguiu fazer checkout da main (pode ja estar nela) >> "%LOG%"
)

:: Puxar atualizacoes remotas antes de commitar (evita conflito)
git pull origin main >> "%LOG%" 2>&1
if errorlevel 1 (
    echo [%date% %time%] AVISO: git pull falhou (sem internet ou sem atualizacoes) >> "%LOG%"
)

:: ─────────────────────────────────────────────────────────────
::  Verificar se o Excel existe
:: ─────────────────────────────────────────────────────────────
if not exist "%XLSX%" (
    echo [%date% %time%] ERRO: Excel nao encontrado em %XLSX% >> "%LOG%"
    exit /b 1
)
echo [%date% %time%] Excel encontrado >> "%LOG%"

:: ─────────────────────────────────────────────────────────────
::  Gerar o JSON
:: ─────────────────────────────────────────────────────────────
python gerar_dashboard_json.py "%XLSX%" filtrada dashboard_tv_data.json >> "%LOG%" 2>&1
if errorlevel 1 (
    echo [%date% %time%] ERRO: python falhou ao gerar o JSON >> "%LOG%"
    exit /b 1
)
echo [%date% %time%] JSON gerado com sucesso >> "%LOG%"

:: ─────────────────────────────────────────────────────────────
::  Commitar e enviar para o GitHub
:: ─────────────────────────────────────────────────────────────
git add dashboard_tv_data.json

:: Verificar se ha mudancas para commitar
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "dados: atualizar JSON %date% %time%" >> "%LOG%" 2>&1
    if errorlevel 1 (
        echo [%date% %time%] ERRO: git commit falhou >> "%LOG%"
        exit /b 1
    )
    echo [%date% %time%] Commit criado >> "%LOG%"

    git push origin main >> "%LOG%" 2>&1
    if errorlevel 1 (
        echo [%date% %time%] ERRO: git push falhou - verifique credenciais do git >> "%LOG%"
        exit /b 1
    )
    echo [%date% %time%] Push enviado para o GitHub >> "%LOG%"
) else (
    echo [%date% %time%] Nenhuma mudanca nos dados - nada a commitar >> "%LOG%"
)

echo [%date% %time%] CONCLUIDO com sucesso >> "%LOG%"
exit /b 0
