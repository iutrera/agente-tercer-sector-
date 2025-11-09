from flask import Flask, request, jsonify
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

# Base de datos simulada (en memoria)
eventos = []
contador_eventos = 1

# Modelos de datos (estructura de ejemplo)
"""
Evento:
{
    "id": int,
    "titulo": str,
    "descripcion": str,
    "fecha": str (ISO format),
    "ubicacion": str,
    "organizacion": str,
    "tipo_evento": str,
    "estado": str,
    "participantes": int,
    "creado_en": str (ISO format)
}
"""

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificación de salud del servicio"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/api/eventos', methods=['GET'])
def listar_eventos():
    """
    Lista todos los eventos disponibles
    Parámetros de query opcionales:
    - tipo_evento: filtrar por tipo
    - estado: filtrar por estado
    - organizacion: filtrar por organización
    """
    tipo_evento = request.args.get('tipo_evento')
    estado = request.args.get('estado')
    organizacion = request.args.get('organizacion')

    eventos_filtrados = eventos.copy()

    if tipo_evento:
        eventos_filtrados = [e for e in eventos_filtrados if e.get('tipo_evento') == tipo_evento]
    if estado:
        eventos_filtrados = [e for e in eventos_filtrados if e.get('estado') == estado]
    if organizacion:
        eventos_filtrados = [e for e in eventos_filtrados if e.get('organizacion') == organizacion]

    return jsonify({
        "eventos": eventos_filtrados,
        "total": len(eventos_filtrados)
    }), 200

@app.route('/api/eventos/<int:evento_id>', methods=['GET'])
def obtener_evento(evento_id):
    """Obtiene los detalles de un evento específico"""
    evento = next((e for e in eventos if e['id'] == evento_id), None)

    if not evento:
        return jsonify({"error": "Evento no encontrado"}), 404

    return jsonify(evento), 200

@app.route('/api/eventos', methods=['POST'])
def crear_evento():
    """
    Crea un nuevo evento
    Body esperado:
    {
        "titulo": "string",
        "descripcion": "string",
        "fecha": "string (ISO format)",
        "ubicacion": "string",
        "organizacion": "string",
        "tipo_evento": "string",
        "participantes": int (opcional, default: 0)
    }
    """
    global contador_eventos

    data = request.get_json()

    # Validaciones básicas
    campos_requeridos = ['titulo', 'descripcion', 'fecha', 'ubicacion', 'organizacion', 'tipo_evento']
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({"error": f"Campo requerido faltante: {campo}"}), 400

    # Validar formato de fecha
    try:
        datetime.fromisoformat(data['fecha'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Use formato ISO 8601"}), 400

    # Crear nuevo evento
    nuevo_evento = {
        "id": contador_eventos,
        "titulo": data['titulo'],
        "descripcion": data['descripcion'],
        "fecha": data['fecha'],
        "ubicacion": data['ubicacion'],
        "organizacion": data['organizacion'],
        "tipo_evento": data['tipo_evento'],
        "estado": "programado",
        "participantes": data.get('participantes', 0),
        "creado_en": datetime.now().isoformat()
    }

    eventos.append(nuevo_evento)
    contador_eventos += 1

    return jsonify(nuevo_evento), 201

@app.route('/api/eventos/<int:evento_id>', methods=['PUT'])
def actualizar_evento(evento_id):
    """
    Actualiza un evento existente
    Body: mismos campos que crear_evento (todos opcionales)
    """
    evento = next((e for e in eventos if e['id'] == evento_id), None)

    if not evento:
        return jsonify({"error": "Evento no encontrado"}), 404

    data = request.get_json()

    # Actualizar campos proporcionados
    campos_actualizables = ['titulo', 'descripcion', 'fecha', 'ubicacion', 'organizacion', 'tipo_evento', 'estado', 'participantes']

    for campo in campos_actualizables:
        if campo in data:
            # Validar fecha si se está actualizando
            if campo == 'fecha':
                try:
                    datetime.fromisoformat(data['fecha'].replace('Z', '+00:00'))
                except ValueError:
                    return jsonify({"error": "Formato de fecha inválido. Use formato ISO 8601"}), 400
            evento[campo] = data[campo]

    return jsonify(evento), 200

@app.route('/api/eventos/<int:evento_id>', methods=['DELETE'])
def eliminar_evento(evento_id):
    """Elimina un evento"""
    global eventos

    evento = next((e for e in eventos if e['id'] == evento_id), None)

    if not evento:
        return jsonify({"error": "Evento no encontrado"}), 404

    eventos = [e for e in eventos if e['id'] != evento_id]

    return jsonify({"mensaje": "Evento eliminado exitosamente"}), 200

@app.route('/api/eventos/<int:evento_id>/participantes', methods=['POST'])
def agregar_participante(evento_id):
    """
    Incrementa el contador de participantes de un evento
    Body: { "cantidad": int } (opcional, default: 1)
    """
    evento = next((e for e in eventos if e['id'] == evento_id), None)

    if not evento:
        return jsonify({"error": "Evento no encontrado"}), 404

    data = request.get_json() or {}
    cantidad = data.get('cantidad', 1)

    if not isinstance(cantidad, int) or cantidad < 1:
        return jsonify({"error": "Cantidad debe ser un entero positivo"}), 400

    evento['participantes'] = evento.get('participantes', 0) + cantidad

    return jsonify(evento), 200

@app.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """
    Obtiene estadísticas generales de eventos
    """
    total_eventos = len(eventos)
    total_participantes = sum(e.get('participantes', 0) for e in eventos)

    eventos_por_tipo = {}
    eventos_por_estado = {}

    for evento in eventos:
        tipo = evento.get('tipo_evento', 'Sin tipo')
        estado = evento.get('estado', 'Sin estado')

        eventos_por_tipo[tipo] = eventos_por_tipo.get(tipo, 0) + 1
        eventos_por_estado[estado] = eventos_por_estado.get(estado, 0) + 1

    return jsonify({
        "total_eventos": total_eventos,
        "total_participantes": total_participantes,
        "eventos_por_tipo": eventos_por_tipo,
        "eventos_por_estado": eventos_por_estado
    }), 200

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
