# 📦 Dependencias Externas de SIRIA

Documentación completa de todas las dependencias, servicios y plataformas utilizadas en el proyecto.

---

## 🐍 Dependencias de Python

### Framework Web
- **Flask==3.0.3** - Framework web para la API REST
- **python-dotenv==1.0.1** - Gestión de variables de entorno

### Web Scraping
- **requests==2.31.0** - Librería HTTP para hacer peticiones web
- **beautifulsoup4==4.12.3** - Parser HTML/XML para scraping
- **lxml==5.1.0** - Parser rápido para BeautifulSoup
- **playwright==1.41.0** - Automatización de navegador (JavaScript rendering)
- **selenium==4.18.0** - Alternativa para scraping dinámico
- **webdriver-manager==4.0.1** - Gestión automática de drivers de navegador

### Procesamiento de Datos
- **pandas==2.2.0** - Manipulación y análisis de datos
- **openpyxl==3.1.2** - Lectura/escritura de archivos Excel (.xlsx)
- **xlsxwriter==3.2.0** - Creación de archivos Excel con formato

### Inteligencia Artificial
- **openai==1.12.0** - Cliente oficial de OpenAI para clasificación con GPT

### Integración con Google
- **google-api-python-client==2.118.0** - Cliente para Google APIs
- **google-auth-httplib2==0.2.0** - Autenticación HTTP para Google
- **google-auth-oauthlib==1.2.0** - OAuth para Google APIs

### Programación de Tareas
- **schedule==1.2.1** - Scheduler simple para tareas periódicas

### Gestión de Errores y Retry
- **retry==0.9.2** - Decoradores para reintentos
- **tenacity==8.2.3** - Sistema avanzado de reintentos con estrategias

---

## ☁️ Servicios en la Nube

### 1. **GitHub**
- **Uso**: Repositorio de código fuente
- **URL**: https://github.com/iutrera/agente-tercer-sector-
- **Plan**: Free (repositorio público/privado)
- **Funcionalidades usadas**:
  - Control de versiones (Git)
  - Almacenamiento de código
  - Issues y project management
  - GitHub Actions (potencial CI/CD)

**Configuración necesaria**:
```bash
git remote add origin https://github.com/iutrera/agente-tercer-sector-.git
git push origin main
```

### 2. **Railway**
- **Uso**: Hosting y deployment de la aplicación
- **URL**: https://railway.app
- **Plan**: Starter ($5 crédito gratis/mes)
- **Funcionalidades usadas**:
  - Deployment automático desde GitHub
  - Variables de entorno
  - Logs en tiempo real
  - Métricas de uso (CPU, RAM, Network)
  - Dominios públicos

**Configuración en Railway**:
```env
# Variables de entorno configuradas en Railway
SECRET_TOKEN=***
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=***
SMTP_PASS=***
PORT=8000
```

**Archivos de configuración**:
- `Procfile` - Define comando de inicio: `web: python app.py`
- `railway.json` - Configuración específica de Railway
- `requirements.txt` - Dependencias Python para instalación

### 3. **OpenAI API**
- **Uso**: Clasificación inteligente de eventos con GPT-4o-mini
- **URL**: https://platform.openai.com
- **Plan**: Pay-as-you-go
- **Modelo usado**: `gpt-4o-mini` (económico y eficiente)
- **Costo estimado**: ~$0.001 por evento clasificado

**Configuración**:
```env
OPENAI_API_KEY=sk-proj-...
```

**Endpoint usado**:
```python
client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...]
)
```

### 4. **Google Cloud Platform**
- **Uso**: Google Sheets API para almacenamiento de eventos
- **URL**: https://console.cloud.google.com
- **Plan**: Free (uso dentro de cuotas gratuitas)
- **APIs habilitadas**:
  - Google Sheets API v4

**Configuración necesaria**:
1. Crear proyecto en Google Cloud Console
2. Habilitar Google Sheets API
3. Crear cuenta de servicio
4. Descargar credenciales JSON
5. Compartir Sheet con email de la cuenta de servicio

**Credenciales**:
```env
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=1abc...xyz
```

### 5. **Gmail SMTP**
- **Uso**: Envío de emails con adjuntos (agendas semanales)
- **URL**: smtp.gmail.com
- **Plan**: Free (parte de cuenta Gmail)
- **Puerto**: 587 (TLS)

**Configuración necesaria**:
1. Activar verificación en 2 pasos en Google
2. Generar "Contraseña de aplicación"
3. Usar esa contraseña en SMTP_PASS

**Variables de configuración**:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASS=xxxx xxxx xxxx xxxx  # App Password
SMTP_USE_TLS=true
DEFAULT_FROM=tu_email@gmail.com
```

### 6. **Eventbrite API** (Opcional)
- **Uso**: Scraping de eventos de Eventbrite
- **URL**: https://www.eventbrite.com/platform
- **Plan**: Free (con límites de rate)
- **Documentación**: https://www.eventbrite.com/platform/api

**Configuración**:
```env
EVENTBRITE_API_KEY=tu_eventbrite_private_token
```

**Endpoints usados**:
- `/v3/events/search/` - Búsqueda de eventos

---

## 🌐 APIs y Servicios Web Scrapeados

### Organizaciones Españolas (15+)
1. **Fundación ONCE** - https://www.fundaciononce.es
2. **Save the Children España** - https://www.savethechildren.es
3. **Fundación La Caixa** - https://fundacionlacaixa.org
4. **Entreculturas** - https://www.entreculturas.org
5. **Fundación Telefónica** - https://www.fundaciontelefonica.com
6. **CEAR** - https://www.cear.es
7. **Ayuda en Acción** - https://ayudaenaccion.org
8. **ACNUR** - https://www.acnur.org
9. **Fundación Tomillo** - (configurable)
10. Y más...

### Organizaciones Colombianas (7+)
1. **Fundación Corona** - https://www.fundacioncorona.org
2. **Fundación Plan Colombia** - https://plan.org.co
3. **Aldeas Infantiles SOS Colombia** - https://www.aldeasinfantiles.org.co
4. **ACNUR Colombia** - https://www.acnur.org/colombia
5. **Save the Children Colombia** - https://www.savethechildren.org.co
6. **Fundación WWB Colombia** - https://www.fundacionwwbcolombia.org
7. Y más...

**Nota**: Estas organizaciones NO requieren API key, se accede mediante scraping web público.

---

## 🔧 Herramientas de Desarrollo

### 1. **ngrok** (Para testing local)
- **Uso**: Exponer localhost a internet para testing de GPT Actions
- **URL**: https://ngrok.com
- **Plan**: Free (con limitaciones)
- **Comando**: `ngrok http 8000`

### 2. **Python 3.8+**
- **Requerido**: Python 3.8 o superior
- **Recomendado**: Python 3.10 o 3.11
- **Verificar**: `python --version`

### 3. **Git**
- **Uso**: Control de versiones
- **Recomendado**: Git 2.30+
- **Verificar**: `git --version`

### 4. **pip**
- **Uso**: Gestor de paquetes Python
- **Recomendado**: pip 23.0+
- **Verificar**: `pip --version`

---

## 🤖 Integraciones con IA

### 1. **ChatGPT / GPT Actions**
- **Uso**: Interfaz conversacional para acceder a SIRIA
- **URL**: https://chat.openai.com
- **Plan requerido**: ChatGPT Plus o Team
- **Protocolo**: OpenAPI 3.1.0 specification

**Archivo de integración**:
- `openapi.json` - Especificación completa de la API
- `openapi-para-chatgpt.json` - Versión optimizada para GPT

**Autenticación**:
- Tipo: Bearer Token
- Header: `Authorization: Bearer SECRET_TOKEN`

---

## 📊 Dependencias por Módulo

### Módulo de Scraping (`scrapers/`)
```
requests
beautifulsoup4
lxml
playwright (opcional)
selenium (opcional)
tenacity (reintentos)
```

### Módulo de Clasificación (`classifiers/`)
```
openai
```

### Módulo de Base de Datos (`database/`)
```
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
```

### Módulo de Utilidades (`utils/`)
```
pandas
openpyxl
xlsxwriter
```

### Módulo de Schedulers (`schedulers/`)
```
schedule
requests (para llamar API)
```

### API (`app.py`)
```
Flask
python-dotenv
```

---

## 💰 Costos Estimados Mensuales

### Escenario: Uso Normal
- **Railway**: $0 - $5/mes (plan gratuito suficiente)
- **OpenAI API**: ~$2-5/mes (clasificación de ~1000 eventos/mes)
- **Google Cloud**: $0 (dentro de cuota gratuita)
- **Gmail SMTP**: $0 (gratis)
- **GitHub**: $0 (repositorio público/privado gratis)
- **Eventbrite API**: $0 (plan gratuito)

**Total estimado**: $2-10/mes

### Escenario: Uso Intensivo
- **Railway**: $5-20/mes (Hobby/Pro plan)
- **OpenAI API**: $10-20/mes (más eventos, más uso)
- **Google Cloud**: $0-5/mes (si excede cuota)

**Total estimado**: $15-45/mes

---

## 🔐 Gestión de Credenciales

### Variables de Entorno Requeridas

**Archivo local**: `.env`
```env
# API Security
SECRET_TOKEN=token_largo_y_aleatorio

# Email (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASS=app_password_16_caracteres
SMTP_USE_TLS=true
DEFAULT_FROM=tu_email@gmail.com

# OpenAI (opcional pero recomendado)
OPENAI_API_KEY=sk-proj-...

# Google Sheets (opcional)
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=1abc...xyz

# Eventbrite (opcional)
EVENTBRITE_API_KEY=tu_private_token

# Server
PORT=8000
```

**Railway**: Configurar las mismas variables en Settings → Variables

### Archivos de Credenciales

**NO subir a Git** (ya incluidos en `.gitignore`):
- `.env`
- `credentials.json`
- `service-account.json`
- `google-credentials.json`

---

## 🔄 Flujo de Dependencias

```
Usuario → ChatGPT GPT Actions
              ↓
         Railway (Hosting)
              ↓
      Flask API (app.py)
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
Scrapers          Classifiers
(requests +        (OpenAI API)
BeautifulSoup)            ↓
    ↓                   ↓
    └─────────┬─────────┘
              ↓
        Deduplication
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
Google Sheets      Excel Generator
(almacenamiento)   (pandas + openpyxl)
                         ↓
                   Gmail SMTP
                   (envío email)
```

---

## 📚 Documentación de Dependencias

### Links Oficiales

**Python Libraries**:
- Flask: https://flask.palletsprojects.com
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
- Pandas: https://pandas.pydata.org
- OpenAI Python: https://github.com/openai/openai-python
- Schedule: https://schedule.readthedocs.io

**Cloud Services**:
- Railway: https://docs.railway.app
- Google Sheets API: https://developers.google.com/sheets/api
- OpenAI API: https://platform.openai.com/docs
- Eventbrite API: https://www.eventbrite.com/platform/api

**Tools**:
- ngrok: https://ngrok.com/docs
- Git: https://git-scm.com/doc

---

## ⚠️ Limitaciones y Cuotas

### Railway (Plan Free)
- 500 horas de ejecución/mes
- $5 crédito/mes
- 512 MB RAM
- 1 GB almacenamiento

### OpenAI API
- Rate limits según plan
- ~60,000 tokens/min (Tier 1)
- Costo por token usado

### Google Sheets API
- 60 requests/min por usuario
- 100 requests/min por proyecto

### Gmail SMTP
- 500 emails/día (cuenta gratuita)
- 2,000 emails/día (Google Workspace)

### Eventbrite API
- 1,000 requests/día (sin autenticación)
- 2,000 requests/día (con OAuth)

---

## 🔧 Instalación de Dependencias

### Producción (Railway)
```bash
# Automático desde requirements.txt
pip install -r requirements.txt
```

### Desarrollo Local
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar Playwright browsers (opcional)
playwright install
```

---

## 📝 Actualización de Dependencias

### Verificar versiones actuales
```bash
pip list --outdated
```

### Actualizar todas las dependencias
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

### Actualizar una dependencia específica
```bash
pip install --upgrade openai
pip freeze | grep openai >> requirements.txt
```

---

## 🆘 Soporte y Documentación

### Python Packages
- PyPI: https://pypi.org
- Buscar paquetes: `pip search <nombre>`

### Issues y Bugs
- Reportar en GitHub: https://github.com/iutrera/agente-tercer-sector-/issues

### Contacto
- Email: jcsiria@basecamp.world

---

**Última actualización**: Noviembre 2025
**Versión de documento**: 1.0
