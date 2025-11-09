# 🚀 Guía de Inicio Rápido - SIRIA

Esta guía te ayudará a tener SIRIA funcionando en menos de 10 minutos.

## ⚡ Instalación Rápida

### 1. Instalar dependencias

```bash
cd agente-tercer-sector

# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
copy .env.example .env
```

**Editar `.env` con tus credenciales mínimas:**

```env
SECRET_TOKEN=mi_token_secreto_12345

# Configuración de email (usar Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASS=tu_app_password_de_gmail
SMTP_USE_TLS=true
DEFAULT_FROM=tu_email@gmail.com
```

> **Nota**: Para Gmail, necesitas crear una "contraseña de aplicación" en tu cuenta de Google:
> 1. Ir a Cuenta de Google → Seguridad
> 2. Activar verificación en 2 pasos
> 3. Generar contraseña de aplicación
> 4. Usar esa contraseña en `SMTP_PASS`

### 3. Probar el sistema

```bash
# Probar scraping básico (solo 3 organizaciones)
python siria_main.py test
```

Esto debería:
- Scrapear eventos de 3 organizaciones
- Clasificarlos automáticamente
- Generar un archivo Excel en `./output/test_output.xlsx`

## 🎯 Primeros Pasos

### Ejecutar scraping completo

```bash
python siria_main.py scrape
```

Esto scrapeará todas las organizaciones configuradas (15+ españolas, 7+ colombianas).

### Ejecutar actualización completa

```bash
# Sin enviar email
python siria_main.py update --no-email

# Con envío de email
python siria_main.py update
```

Esto ejecutará el flujo completo:
1. Scraping de todas las fuentes
2. Clasificación con IA
3. Deduplicación
4. Generación de Excel
5. Envío por email (si no se usa --no-email)

### Iniciar la API

```bash
python app.py
```

La API estará disponible en `http://localhost:8000`

Probar:
- `http://localhost:8000/health` (sin autenticación)
- `http://localhost:8000/get_events` (requiere Bearer token)

### Iniciar scheduler para actualizaciones semanales

```bash
python siria_main.py schedule
```

Esto ejecutará automáticamente la actualización completa todos los lunes a las 09:00.

## 📊 Resultados

### Archivos generados

Los archivos Excel se generan en `./output/`:

- `agenda_eventos_tercer_sector_YYYY-MM-DD.xlsx` - Agenda completa
- `resumen_eventos_YYYY-MM-DD.xlsx` - Reporte con estadísticas

### Logs

Los logs se guardan como:
- `siria_YYYYMMDD.log` - Log principal
- `siria_weekly_update.log` - Log de actualizaciones
- `siria_scheduler.log` - Log del scheduler

## 🔧 Configuración Opcional

### OpenAI (para clasificación mejorada)

Añadir a `.env`:
```env
OPENAI_API_KEY=sk-tu-api-key-aqui
```

Sin esto, el sistema usará clasificación basada en reglas (funciona bien).

### Google Sheets (para almacenamiento en la nube)

1. Crear proyecto en Google Cloud Console
2. Habilitar Google Sheets API
3. Descargar credenciales JSON
4. Añadir a `.env`:
```env
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=tu_id_de_hoja
```

### Eventbrite (opcional)

```env
EVENTBRITE_API_KEY=tu_api_key
```

## 🐛 Solución de Problemas

### Error: "No module named 'scrapers'"

```bash
# Asegúrate de estar en el directorio correcto
cd agente-tercer-sector
python siria_main.py test
```

### Error: "Google API libraries not available"

No es crítico. El sistema funciona sin Google Sheets.

Para instalar:
```bash
pip install google-api-python-client google-auth
```

### Error en envío de email

Verificar:
1. App password de Gmail configurado correctamente
2. Verificación en 2 pasos activada en Google
3. Variables SMTP correctas en `.env`

### No se encuentran eventos

Es normal en el primer test. Los scrapers genéricos necesitan ajuste de selectores según la estructura actual de cada sitio web.

## 📝 Próximos Pasos

1. **Revisar eventos scrapeados**: Abrir Excel generado en `./output/`
2. **Ajustar selectores**: Si algunos scrapers no funcionan, editar archivos en `scrapers/`
3. **Añadir organizaciones**: Editar `generic_scraper.py` o `colombia_organizations.py`
4. **Configurar GPT Actions**: Usar `openapi.json` para integrar con ChatGPT
5. **Desplegar en producción**: Ver README.md sección "Despliegue"

## 🎓 Comandos Útiles

```bash
# Ver ayuda
python siria_main.py --help

# Scrapear organización específica
python siria_main.py scrape --org "Fundación ONCE"

# Modo test (rápido)
python siria_main.py test

# Actualización completa sin email
python siria_main.py update --no-email

# Ver logs en tiempo real (Linux/Mac)
tail -f siria_$(date +%Y%m%d).log

# Ver logs en tiempo real (Windows PowerShell)
Get-Content siria_$(Get-Date -Format "yyyyMMdd").log -Wait
```

## 💡 Tips

- **Primera ejecución**: Usa `test` para verificar que todo funciona
- **Desarrollo**: Usa `scrape` para probar scrapers individuales
- **Producción**: Usa `schedule` para actualizaciones automáticas
- **Debugging**: Revisa los logs en tiempo real

## 🆘 Necesitas Ayuda?

1. Revisar logs: `siria_YYYYMMDD.log`
2. Ver README completo: `README.md`
3. Contacto: jcsiria@basecamp.world

---

¡Listo! Ya tienes SIRIA funcionando 🎉
