@echo off
echo Instalando dependências para o Classificador de Estresse Acadêmico...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não foi encontrado. Por favor, instale Python 3.8 ou superior.
    pause
    exit /b 1
)

REM Instalar dependências
echo Instalando dependências do requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERRO: Falha na instalação das dependências.
    pause
    exit /b 1
)

echo.
echo Dependências instaladas com sucesso!
echo.

REM Executar aplicação
echo Iniciando aplicação Flask...
echo.
echo Abra o navegador e acesse: http://localhost:5000
echo.
echo Para parar a aplicação, pressione Ctrl+C
echo.

python app.py

pause