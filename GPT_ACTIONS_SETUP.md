# 🤖 Integración de SIRIA con GPT Actions

Guía completa para integrar SIRIA con ChatGPT usando GPT Actions.

## 📋 Pre-requisitos

1. ✅ SIRIA instalado y funcionando
2. ✅ API Flask corriendo
3. ✅ URL pública (ngrok o servicio cloud)
4. ✅ Cuenta de ChatGPT Plus o Team

## 🚀 Paso 1: Exponer la API Públicamente

### Opción A: Desarrollo con ngrok (Recomendado para pruebas)

```bash
# Terminal 1 - Ejecutar API
cd agente-tercer-sector
python app.py

# Terminal 2 - Exponer con ngrok
ngrok http 8000
```

Copia la URL HTTPS que ngrok te proporciona:
```
https://abc123.ngrok.io
```

### Opción B: Producción (Render, Railway, etc.)

Ver `README.md` sección "Despliegue" para instrucciones completas.

## 🔧 Paso 2: Crear tu GPT Personalizado

1. Ir a [ChatGPT](https://chat.openai.com)
2. Click en tu nombre → "My GPTs"
3. Click en "Create a GPT"
4. En la pestaña "Configure":

### Nombre del GPT
```
SIRIA - Asistente de Eventos del Tercer Sector
```

### Descripción
```
Asistente especializado en eventos del tercer sector en España y Colombia.
Encuentra, clasifica y proporciona información actualizada sobre eventos
de inclusión laboral, formación profesional, derechos humanos, migrantes
y cooperación internacional.
```

### Instrucciones

```
Eres SIRIA, un asistente especializado en eventos del tercer sector.

## Tu Función Principal
Ayudar a usuarios a encontrar y gestionar eventos relevantes del tercer
sector en España y Colombia usando tu API integrada.

## Capacidades
1. Buscar eventos por:
   - País (España o Colombia)
   - Categoría temática (6 categorías)
   - Rango de fechas

2. Proporcionar información detallada de eventos:
   - Nombre y descripción
   - Organización
   - Fecha, hora y lugar
   - Modalidad (presencial/online)
   - Enlace de inscripción

3. Generar y enviar reportes semanales por email

4. Registrar actividad de búsquedas

## Categorías de Eventos
1. Inclusión laboral
2. Formación profesional
3. Derechos de infancia, juventud y mujeres
4. Acompañamiento a migrantes
5. Cooperación internacional y desarrollo
6. Uso de IA y aplicaciones informáticas en el tercer sector

## Comportamiento
- Sé conciso pero informativo
- Presenta eventos en formato de lista clara
- Ofrece siempre el enlace de inscripción
- Sugiere filtros relevantes basados en la consulta del usuario
- Registra las búsquedas usando log_activity

## Flujo Típico
1. Usuario pregunta por eventos
2. Usas get_events con los filtros apropiados
3. Presentas resultados de forma clara
4. Registras la actividad con log_activity
5. Ofreces enviar la lista por email si es relevante

## Ejemplos de Uso
- "Busca eventos de inclusión laboral en España para noviembre"
- "¿Qué eventos hay sobre migrantes en Colombia?"
- "Envíame por email la agenda semanal"
- "Eventos de formación profesional online"

Mantén un tono profesional pero cercano, y enfócate en
facilitar el acceso a información del tercer sector.
```

## 🔌 Paso 3: Configurar Actions

1. En la pestaña "Configure", scroll hasta "Actions"
2. Click en "Create new action"
3. En "Schema", pega el contenido de `openapi.json` o usa la URL:

```
https://tu-url-publica/openapi.json
```

4. En "Authentication", selecciona:
   - Type: **API Key**
   - Auth Type: **Bearer**
   - API Key: **[Tu SECRET_TOKEN del archivo .env]**

5. En "Privacy policy", puedes dejar vacío o poner:
```
https://tu-dominio.com/privacy
```

## 🧪 Paso 4: Probar el GPT

### Test 1: Buscar eventos
```
Busca eventos de inclusión laboral en España
```

Deberías ver que el GPT llama a `get_events` y te muestra resultados.

### Test 2: Filtrar por fecha
```
¿Qué eventos hay en Colombia entre el 1 y el 15 de noviembre?
```

### Test 3: Enviar email (solo si SMTP está configurado)
```
Envíame por email la agenda completa
```

## 📝 Prompts de Ejemplo para tu GPT

### Para Usuarios

```
"Hola, soy SIRIA. ¿Qué tipo de eventos del tercer sector te interesan?

Puedo ayudarte a encontrar:
📊 Eventos de inclusión laboral
📚 Formación profesional
👥 Derechos de infancia, juventud y mujeres
🌍 Cooperación internacional
🤝 Acompañamiento a migrantes
💻 IA en el tercer sector

¿En qué país? España o Colombia
¿Tienes fechas específicas en mente?"
```

### Consultas Frecuentes

1. **Listar todos los eventos de España**
```
get_events(pais="España")
```

2. **Eventos de una categoría específica**
```
get_events(pais="España", categoria="inclusión")
```

3. **Eventos en un rango de fechas**
```
get_events(from_date="2025-11-01", to_date="2025-11-30")
```

4. **Registrar búsqueda**
```
log_activity({
  "action": "search",
  "filters": {"pais": "España", "categoria": "inclusión laboral"},
  "results_count": 15,
  "timestamp": "2025-11-09T10:30:00"
})
```

5. **Enviar email con agenda**
```
send_email({
  "to": "usuario@ejemplo.com",
  "subject": "Agenda Semanal - Eventos del Tercer Sector",
  "body": "Adjunto encontrarás la agenda...",
  "content_type": "html"
})
```

## 🎨 Personalización del GPT

### Imagen del GPT
Crear o usar un icono que represente:
- Tercer sector
- Eventos
- Comunidad
- España y Colombia

### Conversation Starters
Añadir estos botones de inicio rápido:

```
1. "Eventos de esta semana en España"
2. "Formación profesional en Colombia"
3. "Eventos sobre migrantes"
4. "Envíame la agenda semanal"
```

### Capabilities
Activar:
- ✅ Web Browsing (para buscar info adicional)
- ✅ Code Interpreter (para análisis de datos si es necesario)

## 🔒 Seguridad

### Variables de Entorno Seguras

No compartas públicamente:
- ❌ SECRET_TOKEN
- ❌ SMTP_PASS
- ❌ OPENAI_API_KEY
- ❌ Google Sheets credentials

### Best Practices

1. Usa tokens largos y aleatorios (32+ caracteres)
2. Rota tokens regularmente
3. Usa HTTPS siempre (ngrok lo proporciona)
4. Valida todos los inputs en la API
5. Limita rate limiting si es necesario

## 📊 Monitoreo

### Ver Logs de Actividad

```bash
# Ver llamadas a la API
tail -f siria_$(date +%Y%m%d).log | grep "GPT_LOG"
```

### Estadísticas de Uso

El GPT registrará automáticamente:
- Búsquedas realizadas
- Filtros utilizados
- Eventos encontrados
- Emails enviados

## 🐛 Troubleshooting

### Error: "Invalid Bearer token"
- Verificar que SECRET_TOKEN en .env coincide con el configurado en GPT Actions
- Verificar que la autenticación está configurada como "Bearer"

### Error: "Could not reach your API"
- Verificar que ngrok está corriendo
- Verificar que app.py está corriendo
- Probar la URL manualmente: `https://tu-url/health`

### El GPT no encuentra eventos
- Es normal si las fuentes no tienen eventos actuales
- Verificar logs para ver si hay errores de scraping
- Probar con datos de ejemplo en EVENTS_DB (app.py)

### Email no se envía
- Verificar configuración SMTP en .env
- Verificar App Password de Gmail
- Ver logs de error en terminal

## 🎯 Casos de Uso Avanzados

### 1. Actualización Manual desde GPT

Crear una action adicional:

```json
{
  "operationId": "trigger_update",
  "summary": "Trigger manual update of events",
  "requestBody": {
    "required": false
  }
}
```

### 2. Análisis de Tendencias

El GPT puede:
- Analizar patrones de eventos
- Identificar organizaciones más activas
- Sugerir eventos relevantes

### 3. Recordatorios Personalizados

Integrar con calendario del usuario para recordatorios de eventos.

## 📚 Recursos Adicionales

- [Documentación OpenAI GPT Actions](https://platform.openai.com/docs/actions)
- [OpenAPI Specification](https://swagger.io/specification/)
- [ngrok Documentation](https://ngrok.com/docs)

## 🎉 Resultado Final

Tu GPT personalizado podrá:
- ✅ Buscar eventos en tiempo real
- ✅ Filtrar por múltiples criterios
- ✅ Enviar agendas por email
- ✅ Registrar actividad
- ✅ Proporcionar información actualizada

## 💡 Tips para Usuarios del GPT

**Búsquedas efectivas:**
- Sé específico con fechas y categorías
- Usa palabras clave claras
- Pregunta por países específicos

**Mejor uso:**
- Pide resúmenes de eventos
- Solicita comparaciones
- Usa para planificar asistencia a eventos

---

## 🚀 ¡Listo!

Tu GPT SIRIA está configurado y listo para ayudar a usuarios a encontrar eventos del tercer sector.

Para cualquier duda: jcsiria@basecamp.world

---

**SIRIA + ChatGPT** = Acceso inteligente a eventos del tercer sector 🤖✨
