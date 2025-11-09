# SIRIA - Sistema de Recopilación e Identificación de Recursos e Información Actualizada

Sistema de inteligencia artificial para explorar, identificar, compilar y actualizar semanalmente un listado de eventos relevantes del tercer sector en España y Colombia.

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Arquitectura](#arquitectura)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Módulos](#módulos)
- [Despliegue](#despliegue)
- [Mantenimiento](#mantenimiento)

## 🎯 Descripción

SIRIA es un sistema completo que automatiza la recopilación y clasificación de eventos del tercer sector enfocados en:

- Inclusión laboral
- Formación profesional
- Derechos de infancia, juventud y mujeres
- Acompañamiento a migrantes
- Cooperación internacional y desarrollo
- Uso de IA y aplicaciones informáticas en el tercer sector

## ✨ Características

### Funcionalidades Principales

1. **Scraping Multi-Fuente**
   - Scraping de 15+ organizaciones españolas (Fundación ONCE, Save the Children, Entreculturas, etc.)
   - Scraping de 7+ organizaciones colombianas
   - Integración con Eventbrite
   - Sistema de reintentos automáticos

2. **Clasificación Inteligente**
   - Clasificación con IA usando OpenAI GPT-4
   - Clasificación basada en reglas como fallback
   - 6 categorías temáticas predefinidas

3. **Deduplicación Avanzada**
   - Deduplicación por ID único (hash)
   - Detección de similitud semántica
   - Fusión de información de eventos duplicados

4. **Almacenamiento y Exportación**
   - Almacenamiento en Google Sheets
   - Generación de Excel con formato profesional
   - Reportes resumen con estadísticas

5. **Automatización**
   - Actualizaciones semanales automáticas (lunes 09:00)
   - Envío automático por email
   - Sistema de logging y monitoreo

## 🏗️ Arquitectura

```
agente-tercer-sector/
├── app.py                      # API Flask principal
├── siria_main.py              # Punto de entrada del sistema
├── scrapers/
│   ├── base_scraper.py        # Clase base para scrapers
│   ├── fundacion_once_scraper.py
│   ├── save_the_children_scraper.py
│   ├── generic_scraper.py     # Scraper configurable
│   ├── eventbrite_scraper.py
│   ├── colombia_organizations.py
│   └── scraper_orchestrator.py # Coordinador de scrapers
├── classifiers/
│   └── event_classifier.py    # Clasificador con IA
├── database/
│   └── google_sheets_manager.py # Gestión de Google Sheets
├── utils/
│   ├── deduplication.py       # Sistema de deduplicación
│   └── excel_generator.py     # Generador de Excel
├── schedulers/
│   ├── weekly_updater.py      # Actualización semanal
│   └── scheduler.py           # Programador de tareas
├── output/                    # Archivos Excel generados
├── requirements.txt
├── .env
└── README.md
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.8+
- pip
- Cuenta de Google Cloud (para Google Sheets API)
- OpenAI API Key (opcional, para clasificación con IA)
- Eventbrite API Key (opcional)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
cd agente-tercer-sector
```

2. **Crear entorno virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Instalar Playwright (para scraping dinámico)**
```bash
playwright install
```

5. **Configurar variables de entorno**
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Editar `.env` con tus credenciales.

## ⚙️ Configuración

### Variables de Entorno (.env)

```env
# Autenticación API
SECRET_TOKEN=tu_token_secreto_aqui

# SMTP para envío de emails
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASS=tu_app_password
SMTP_USE_TLS=true
DEFAULT_FROM=tu_email@gmail.com

# OpenAI (opcional)
OPENAI_API_KEY=sk-...

# Google Sheets (opcional)
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=tu_spreadsheet_id

# Eventbrite (opcional)
EVENTBRITE_API_KEY=tu_eventbrite_api_key

# Puerto del servidor
PORT=8000
```

### Configuración de Google Sheets

1. Ir a [Google Cloud Console](https://console.cloud.google.com)
2. Crear un proyecto nuevo
3. Habilitar Google Sheets API
4. Crear credenciales de cuenta de servicio
5. Descargar el archivo JSON y guardarlo como `credentials.json`
6. Compartir tu hoja de cálculo con el email de la cuenta de servicio

## 📖 Uso

### Comandos Principales

```bash
# Ejecutar scraping básico
python siria_main.py scrape

# Ejecutar scraping de una organización específica
python siria_main.py scrape --org "Fundación ONCE"

# Ejecutar actualización completa
python siria_main.py update

# Ejecutar actualización sin enviar email
python siria_main.py update --no-email

# Iniciar scheduler para actualizaciones semanales
python siria_main.py schedule

# Modo de prueba (scraping limitado)
python siria_main.py test
```

### Ejecutar API Flask

```bash
python app.py
```

La API estará disponible en `http://localhost:8000`

### Ejecutar con ngrok (para testing con GPT)

```bash
# Terminal 1 - Ejecutar API
python app.py

# Terminal 2 - Exponer con ngrok
ngrok http 8000
```

## 🔌 API Endpoints

### Endpoints Públicos

- `GET /health` - Verificar estado del servicio
- `GET /openapi.json` - Esquema OpenAPI

### Endpoints Protegidos (requieren Bearer token)

- `GET /get_events` - Obtener eventos con filtros
  - Parámetros: `from_date`, `to_date`, `pais`, `categoria`

- `POST /log_activity` - Registrar actividad
  - Body: JSON con datos de actividad

- `POST /send_email` - Enviar email con adjunto
  - Body: `to`, `subject`, `body`, `content_type`, `attachment_base64`, `filename`

### Ejemplo de Uso

```bash
# Obtener eventos
curl -H "Authorization: Bearer TU_TOKEN" \
  "http://localhost:8000/get_events?pais=España&from_date=2025-11-01"

# Enviar email
curl -X POST -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "destinatario@ejemplo.com",
    "subject": "Agenda Semanal",
    "body": "Adjunto encontrarás la agenda actualizada",
    "attachment_base64": "...",
    "filename": "agenda_eventos.xlsx"
  }' \
  http://localhost:8000/send_email
```

## 🔧 Módulos

### Scrapers

- **BaseScraper**: Clase base con funcionalidad común
- **FundacionOnceScraper**: Scraper específico para Fundación ONCE
- **SaveTheChildrenScraper**: Scraper para Save the Children
- **GenericScraper**: Scraper configurable para múltiples organizaciones
- **EventbriteScraper**: Integración con API de Eventbrite
- **ScraperOrchestrator**: Coordina ejecución paralela de scrapers

### Clasificador

- **EventClassifier**: Clasifica eventos usando IA (OpenAI) o reglas

### Utilidades

- **EventDeduplicator**: Sistema de deduplicación por hash y similitud
- **ExcelGenerator**: Genera archivos Excel con formato profesional

### Base de Datos

- **GoogleSheetsManager**: CRUD para Google Sheets

### Schedulers

- **WeeklyUpdater**: Orquesta proceso completo de actualización
- **Scheduler**: Programa ejecución semanal automática

## 🌐 Despliegue

### Opciones de Despliegue

#### 1. Render (Recomendado)

1. Crear cuenta en [Render](https://render.com)
2. Crear nuevo Web Service
3. Conectar repositorio
4. Configurar:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. Añadir variables de entorno
6. Deploy

#### 2. Railway

1. Crear cuenta en [Railway](https://railway.app)
2. New Project → Deploy from GitHub
3. Añadir variables de entorno
4. Deploy

#### 3. Heroku

```bash
# Instalar Heroku CLI
heroku login
heroku create tu-app-name
git push heroku main
```

#### 4. VPS (Linux)

```bash
# Instalar supervisor para mantener proceso activo
sudo apt-get install supervisor

# Configurar supervisor
sudo nano /etc/supervisor/conf.d/siria.conf
```

## 🔍 Mantenimiento

### Logs

Los logs se guardan en:
- `siria_YYYYMMDD.log` - Log diario del sistema
- `siria_weekly_update.log` - Log de actualizaciones semanales
- `siria_scheduler.log` - Log del scheduler

### Monitoreo

Verificar el estado:
```bash
# Ver últimos logs
tail -f siria_$(date +%Y%m%d).log

# Verificar eventos scrapeados
python siria_main.py test
```

### Actualización de Scrapers

Si una organización cambia su sitio web:

1. Editar el archivo del scraper correspondiente
2. Actualizar selectores CSS/XPath
3. Probar con: `python siria_main.py scrape --org "Nombre Organización"`

### Añadir Nuevas Organizaciones

1. Editar `scrapers/generic_scraper.py` (para España) o `scrapers/colombia_organizations.py` (para Colombia)
2. Añadir nueva configuración al array `SPANISH_ORGANIZATIONS` o `COLOMBIAN_ORGANIZATIONS`
3. Especificar selectores CSS apropiados

## 📊 Estadísticas

El sistema genera estadísticas automáticas:
- Total de eventos por categoría
- Eventos por país
- Eventos por modalidad (presencial/online)
- Eventos por organización

## 🤝 Contribuciones

Para añadir nuevas funcionalidades:

1. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
2. Hacer cambios y commit
3. Push y crear Pull Request

## 📄 Licencia

MIT License

## 👥 Contacto

Para soporte o consultas: jcsiria@basecamp.world

---

**SIRIA** - Automatizando la recopilación de eventos del tercer sector 🤖✨
