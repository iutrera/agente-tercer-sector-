@echo off
echo ====================================
echo API de Gestion de Eventos
echo ====================================
echo.

cd %~dp0

if not exist "venv\" (
    echo Creando entorno virtual...
    python -m venv venv
    echo.
)

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Instalando/Actualizando dependencias...
pip install -r requirements.txt --quiet

echo.
echo ====================================
echo Iniciando servidor Flask...
echo ====================================
echo.
echo El servidor estara disponible en:
echo http://localhost:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python app.py
