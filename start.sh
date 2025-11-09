#!/bin/bash

echo "===================================="
echo "API de Gestion de Eventos"
echo "===================================="
echo ""

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    echo ""
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando/Actualizando dependencias..."
pip install -r requirements.txt --quiet

echo ""
echo "===================================="
echo "Iniciando servidor Flask..."
echo "===================================="
echo ""
echo "El servidor estara disponible en:"
echo "http://localhost:5000"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

python app.py
