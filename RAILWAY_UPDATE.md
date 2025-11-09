# 🚂 Actualizar Despliegue en Railway

Guía para actualizar tu despliegue existente de SIRIA en Railway con todas las nuevas funcionalidades.

## 📦 Paso 1: Subir el Código Actualizado a Git

```bash
# 1. Asegúrate de estar en el directorio correcto
cd C:\Users\iutre\IdeaProjects\SIRIA\agente-tercer-sector

# 2. Añadir todos los archivos nuevos
git add .

# 3. Hacer commit con descripción
git commit -m "Update SIRIA: Complete system with scrapers, classifiers, schedulers and full automation"

# 4. Subir a GitHub (Railway detectará automáticamente el cambio)
git push origin main
```

## 🔄 Paso 2: Railway Desplegará Automáticamente

Railway detectará el push y comenzará a redesplegar automáticamente. Esto tomará 2-3 minutos.

Puedes ver el progreso en:
- https://railway.app → Tu proyecto → Deployments

## ⚙️ Paso 3: Configurar Variables de Entorno en Railway

**IMPORTANTE**: Necesitas configurar estas variables de entorno en Railway:

### Variables Obligatorias:

1. Ve a tu proyecto en Railway
2. Click en tu servicio
3. Click en "Variables"
4. Añade las siguientes variables:

```env
SECRET_TOKEN=tu_token_secreto_largo_y_aleatorio

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASS=tu_app_password_de_gmail
SMTP_USE_TLS=true
DEFAULT_FROM=tu_email@gmail.com

PORT=8000
```

### Variables Opcionales (Recomendadas):

```env
# Para clasificación mejorada con IA
OPENAI_API_KEY=sk-tu-api-key-aqui

# Para Eventbrite
EVENTBRITE_API_KEY=tu_eventbrite_api_key

# Para Google Sheets (si lo usarás)
GOOGLE_SHEETS_SPREADSHEET_ID=tu_spreadsheet_id
```

**Nota sobre Google Sheets**: Las credenciales JSON no se pueden subir como variable de entorno simple. Opciones:
- Usar Railway Volumes para almacenar `credentials.json`
- O no usar Google Sheets en Railway (solo usar generación de Excel local)

## 🧪 Paso 4: Verificar que Funciona

### 4.1 Obtener tu URL de Railway

1. En Railway, click en tu servicio
2. Ve a Settings
3. En "Domains", deberías ver tu URL (ej: `https://agente-tercer-sector-production.up.railway.app`)

### 4.2 Probar los Endpoints

**Health Check (público):**
```
https://TU-URL.railway.app/health
```

Deberías ver:
```json
{
  "status": "ok",
  "time": "2025-11-09T..."
}
```

**OpenAPI Schema (público):**
```
https://TU-URL.railway.app/openapi.json
```

**Get Events (requiere Bearer token):**
```bash
curl -H "Authorization: Bearer TU_SECRET_TOKEN" \
  "https://TU-URL.railway.app/get_events?pais=España"
```

## 🤖 Paso 5: Actualizar GPT Actions

Si ya tenías un GPT configurado:

1. Ve a tu GPT en ChatGPT
2. Click en "Edit GPT"
3. Ve a "Configure" → "Actions"
4. Actualiza la URL del servidor en el schema:
   ```json
   "servers": [
     {
       "url": "https://TU-NUEVA-URL.railway.app"
     }
   ]
   ```
5. Guarda

O simplemente apunta a:
```
https://TU-URL.railway.app/openapi.json
```

Y Railway actualizará automáticamente el schema.

## 🆕 Nuevas Funcionalidades Disponibles

Tu API ahora incluye:

### 1. Sistema Completo de Scraping
- 22+ organizaciones (España y Colombia)
- Eventbrite
- Ejecución paralela

### 2. Clasificación Inteligente
- 6 categorías temáticas
- IA con OpenAI (si configuras API key)
- Clasificación por reglas como fallback

### 3. Deduplicación
- Elimina eventos duplicados automáticamente

### 4. Generación de Excel
- Formato profesional
- Múltiples hojas
- Estadísticas

### 5. Envío de Emails
- Con adjuntos
- HTML y texto plano

## 📊 Comandos Disponibles (si usas Railway CLI)

Si instalas Railway CLI, puedes ejecutar comandos directamente:

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Linkear tu proyecto
railway link

# Ver logs en tiempo real
railway logs

# Ejecutar comando en Railway
railway run python siria_main.py test

# Ver variables de entorno
railway variables
```

## 🔧 Troubleshooting

### Error: "Module not found"
- Verificar que `requirements.txt` está actualizado
- Railway reinstalará dependencias automáticamente

### Error: "Port already in use"
- Railway asigna el puerto automáticamente vía variable `PORT`
- El código ya está configurado para usar `os.getenv('PORT', 8000)`

### Error: "SMTP connection failed"
- Verificar que las variables SMTP están correctamente configuradas
- Verificar App Password de Gmail
- Verificar que SMTP_USE_TLS=true

### El scraping no encuentra eventos
- Es normal, los scrapers genéricos necesitan ajustes según cada sitio
- Los selectores CSS pueden cambiar
- Funciona mejor con OpenAI API key para clasificación

### Timeout en Railway
- Railway free tier tiene límite de 500 horas/mes
- El scraping completo puede tomar varios minutos
- Considera usar `siria_main.py test` para pruebas rápidas

## 📈 Monitoreo en Railway

Railway proporciona:

1. **Logs en Tiempo Real**
   - Ve a tu servicio → Logs
   - Puedes ver todo el output de Python

2. **Métricas**
   - CPU usage
   - Memory usage
   - Network activity

3. **Deployments**
   - Historial de despliegues
   - Rollback si es necesario

## 🔐 Seguridad

### Best Practices en Railway:

1. ✅ Nunca subir `.env` a git
2. ✅ Usar variables de entorno de Railway
3. ✅ Rotar `SECRET_TOKEN` regularmente
4. ✅ Usar App Passwords, no contraseñas reales
5. ✅ Limitar acceso a endpoints sensibles

### Variables de Entorno Sensibles:

NO compartir públicamente:
- `SECRET_TOKEN`
- `SMTP_PASS`
- `OPENAI_API_KEY`
- Credenciales de Google

## 💰 Costos de Railway

**Plan Gratuito:**
- $5 de crédito/mes
- 500 horas de ejecución
- 512 MB RAM
- 1 GB disco

**Si necesitas más:**
- Railway Hobby: $5/mes
- Railway Pro: $20/mes

Para SIRIA, el plan gratuito debería ser suficiente para:
- API corriendo 24/7
- Actualizaciones semanales
- Testing regular

## 📞 Soporte

Si tienes problemas:

1. Revisar logs en Railway
2. Verificar variables de entorno
3. Probar endpoints manualmente
4. Revisar documentación: `README.md`, `QUICKSTART.md`

## ✅ Checklist de Actualización

- [ ] Código pusheado a GitHub
- [ ] Railway desplegó automáticamente (ver Deployments)
- [ ] Variables de entorno configuradas
- [ ] `/health` responde correctamente
- [ ] `/get_events` funciona con Bearer token
- [ ] GPT Actions actualizado (si aplica)
- [ ] Email test enviado (si configuraste SMTP)

---

## 🎉 ¡Listo!

Tu despliegue de SIRIA en Railway está actualizado con todas las nuevas funcionalidades.

**URL de tu API**: `https://TU-URL.railway.app`

**Próximos pasos:**
- Probar todos los endpoints
- Configurar GPT Actions
- Ejecutar primera actualización semanal

Para cualquier duda: jcsiria@basecamp.world

---

**SIRIA** - Desplegado y listo en Railway 🚂✨
