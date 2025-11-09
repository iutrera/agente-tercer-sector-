# API de Gestión de Eventos del Tercer Sector

API RESTful para la gestión de eventos de organizaciones del tercer sector, ONGs y asociaciones sin ánimo de lucro. Diseñada para integrarse con GPT Actions de OpenAI.

## Características

- Gestión completa de eventos (CRUD)
- Filtrado de eventos por tipo, estado y organización
- Control de participantes
- Estadísticas agregadas
- Documentación OpenAPI 3.1.0
- Compatible con GPT Actions

## Requisitos

- Python 3.7+
- pip
- virtualenv (opcional pero recomendado)

## Instalación

1. Clonar o descargar el proyecto

2. Crear y activar entorno virtual:
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y configurar las variables necesarias
```

## Uso

### Ejecutar el servidor

```bash
# Asegúrate de estar en el entorno virtual
python app.py
```

El servidor se ejecutará en `http://localhost:5000`

### Verificar el estado del servicio

```bash
curl http://localhost:5000/health
```

## Endpoints Disponibles

### Health Check
- `GET /health` - Verificar estado del servicio

### Eventos
- `GET /api/eventos` - Listar todos los eventos (con filtros opcionales)
- `POST /api/eventos` - Crear un nuevo evento
- `GET /api/eventos/{id}` - Obtener detalles de un evento
- `PUT /api/eventos/{id}` - Actualizar un evento
- `DELETE /api/eventos/{id}` - Eliminar un evento

### Participantes
- `POST /api/eventos/{id}/participantes` - Agregar participantes a un evento

### Estadísticas
- `GET /api/estadisticas` - Obtener estadísticas generales

## Ejemplos de Uso

### Crear un evento

```bash
curl -X POST http://localhost:5000/api/eventos \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Taller de Alfabetización Digital",
    "descripcion": "Taller gratuito para personas mayores",
    "fecha": "2024-03-15T10:00:00Z",
    "ubicacion": "Centro Comunitario",
    "organizacion": "Fundación Digital",
    "tipo_evento": "taller"
  }'
```

### Listar eventos

```bash
# Todos los eventos
curl http://localhost:5000/api/eventos

# Filtrar por tipo
curl "http://localhost:5000/api/eventos?tipo_evento=taller"

# Filtrar por estado
curl "http://localhost:5000/api/eventos?estado=programado"
```

### Agregar participantes

```bash
curl -X POST http://localhost:5000/api/eventos/1/participantes \
  -H "Content-Type: application/json" \
  -d '{"cantidad": 5}'
```

## Integración con GPT Actions

1. Accede a tu GPT en ChatGPT
2. Ve a "Configure" > "Actions"
3. Haz clic en "Create new action"
4. Importa el archivo `openapi.json` proporcionado
5. Configura la URL del servidor (debe ser accesible públicamente)
6. Guarda los cambios

### Opciones de Despliegue para GPT Actions

Para que tu GPT pueda acceder a la API, necesitas desplegarla en un servidor accesible públicamente. Algunas opciones:

#### Opción 1: ngrok (desarrollo/pruebas)
```bash
# Instalar ngrok: https://ngrok.com/
ngrok http 5000
```

#### Opción 2: Servicios Cloud Gratuitos
- **Render**: https://render.com
- **Railway**: https://railway.app
- **Fly.io**: https://fly.io
- **PythonAnywhere**: https://pythonanywhere.com

## Estructura del Proyecto

```
agente-tercer-sector/
├── app.py              # Aplicación Flask principal
├── openapi.json        # Especificación OpenAPI
├── requirements.txt    # Dependencias Python
├── .env.example        # Ejemplo de variables de entorno
├── .env                # Variables de entorno (no versionar)
└── README.md           # Este archivo
```

## Modelo de Datos

### Evento
```json
{
  "id": 1,
  "titulo": "string",
  "descripcion": "string",
  "fecha": "2024-03-15T10:00:00Z",
  "ubicacion": "string",
  "organizacion": "string",
  "tipo_evento": "string",
  "estado": "programado|en_curso|finalizado|cancelado",
  "participantes": 0,
  "creado_en": "2024-02-01T08:30:00Z"
}
```

## Próximos Pasos

1. **Base de datos persistente**: Actualmente usa almacenamiento en memoria. Para producción, integrar con PostgreSQL, MySQL o MongoDB.

2. **Autenticación**: Implementar autenticación JWT o OAuth2 para proteger los endpoints.

3. **Validación avanzada**: Agregar validación más robusta con bibliotecas como Marshmallow o Pydantic.

4. **Paginación**: Implementar paginación para endpoints que retornan listas.

5. **Tests**: Agregar tests unitarios y de integración.

6. **Logging**: Implementar sistema de logging más robusto.

7. **CORS**: Configurar CORS adecuadamente para permitir acceso desde dominios específicos.

## Contribuir

Este es un proyecto de ejemplo. Siéntete libre de adaptarlo a tus necesidades específicas.

## Licencia

MIT License
