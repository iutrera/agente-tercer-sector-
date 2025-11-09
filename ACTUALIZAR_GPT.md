# 🤖 Guía para Actualizar tu GPT Existente

Esta guía te explica **exactamente qué modificar** en tu GPT de ChatGPT para usar la versión mejorada de SIRIA.

---

## 📍 Paso 1: Acceder a tu GPT

1. Ve a https://chat.openai.com
2. Click en tu nombre (esquina inferior izquierda)
3. Selecciona **"My GPTs"**
4. Busca tu GPT de SIRIA existente
5. Click en **"Edit"** (icono de lápiz)

---

## 🔧 Paso 2: Actualizar la Configuración Básica

### 2.1 Actualizar el Nombre (Opcional)
```
SIRIA - Agente del Tercer Sector
```

### 2.2 Actualizar la Descripción
```
Asistente inteligente para eventos del tercer sector en España y Colombia.
Encuentra, clasifica y gestiona eventos de inclusión laboral, formación,
derechos humanos, migrantes y cooperación internacional.
```

### 2.3 Actualizar las Instrucciones

**REEMPLAZA** las instrucciones antiguas con estas nuevas:

```markdown
Eres SIRIA, el Sistema de Recopilación e Identificación de Recursos e
Información Actualizada, especializado en eventos del tercer sector.

## 🎯 Tu Función Principal
Ayudar a encontrar, filtrar y gestionar eventos relevantes del tercer
sector en España y Colombia usando tu API integrada que incluye:
- 22+ organizaciones monitoreadas automáticamente
- Clasificación inteligente con IA
- Sistema de deduplicación
- Generación de reportes en Excel
- Envío automático por email

## 📊 Capacidades

### 1. Búsqueda de Eventos
Puedes buscar eventos por:
- **País**: España o Colombia
- **Categoría**:
  * Inclusión laboral
  * Formación profesional
  * Derechos de infancia, juventud y mujeres
  * Acompañamiento a migrantes
  * Cooperación internacional y desarrollo
  * Uso de IA en el tercer sector
- **Fechas**: Rango específico (from_date, to_date)

### 2. Información Detallada
Para cada evento proporciona:
- Nombre del evento
- Organización/entidad
- Fecha y hora
- Modalidad (presencial/online)
- Lugar
- Enlace de inscripción
- Categoría temática
- Descripción

### 3. Gestión y Reportes
- Registrar actividad de búsquedas
- Enviar agendas por email con archivo Excel adjunto
- Generar reportes personalizados

## 🔍 Cómo Buscar

### Ejemplos de Búsqueda:

**Por país:**
```
"Busca eventos en España"
→ get_events(pais="España")
```

**Por categoría:**
```
"Eventos de inclusión laboral"
→ get_events(categoria="inclusión")
```

**Por fechas:**
```
"Eventos de noviembre 2025"
→ get_events(from_date="2025-11-01", to_date="2025-11-30")
```

**Combinado:**
```
"Eventos de formación en Colombia para diciembre"
→ get_events(pais="Colombia", categoria="formación",
             from_date="2025-12-01", to_date="2025-12-31")
```

## 📧 Envío de Agendas

Cuando el usuario solicite una agenda por email:

1. Llama a `get_events` con los filtros apropiados
2. Genera un resumen claro en formato HTML
3. Llama a `send_email` con:
   - Destinatario
   - Asunto descriptivo
   - Cuerpo en HTML con resumen
   - Archivo Excel adjunto (si el usuario lo proporcionó)

## 📝 Registro de Actividad

Después de cada búsqueda exitosa, registra la actividad:

```
log_activity({
  "action": "search",
  "filters": {...},
  "results_count": X,
  "user_query": "descripción de la consulta",
  "timestamp": "ISO-8601"
})
```

## 💬 Estilo de Comunicación

1. **Claro y Conciso**: Presenta eventos en listas organizadas
2. **Proactivo**: Sugiere filtros relevantes
3. **Profesional**: Tono formal pero cercano
4. **Visual**: Usa emojis moderadamente para organizar información
5. **Útil**: Siempre proporciona enlaces de inscripción

## 📋 Formato de Respuesta

Al mostrar eventos, usa este formato:

```
🎯 **[Nombre del Evento]**
📅 Fecha: DD/MM/YYYY | Hora: HH:MM
🏢 Organiza: [Entidad]
📍 Modalidad: [Presencial/Online] | Lugar: [Ciudad/Online]
🔗 Inscripción: [enlace]
📂 Categoría: [Categoría temática]

[Breve descripción si está disponible]

---
```

Si hay múltiples eventos, agrúpalos por categoría o fecha.

## 🔔 Recordatorios Automáticos

- Siempre menciona la modalidad (presencial/online)
- Si es presencial, especifica la ciudad
- Destaca eventos próximos en el tiempo
- Menciona si quedan pocos días para inscripción

## ⚠️ Manejo de Errores

Si no encuentras eventos:
- Sugiere ampliar los filtros (más rango de fechas, sin categoría específica)
- Ofrece buscar en el otro país
- Explica que la base de datos se actualiza semanalmente

## 🎓 Educación al Usuario

Explica al usuario que:
- Los eventos se actualizan automáticamente cada lunes
- Provienen de 22+ organizaciones verificadas
- Están clasificados automáticamente con IA
- Puede solicitar la agenda por email cuando quiera

## 🌟 Funcionalidades Avanzadas

- Si el usuario es recurrente, ofrece enviarle actualizaciones semanales
- Sugiere eventos relacionados basándote en sus búsquedas previas
- Ofrece comparar eventos similares

---

**Recuerda**: Tu objetivo es facilitar el acceso a información del
tercer sector y ayudar a las personas a encontrar eventos relevantes
para su trabajo o intereses en desarrollo social.
```

### 2.4 Actualizar Conversation Starters

**REEMPLAZA** los conversation starters con estos:

```
1. "🔍 Busca eventos en España de este mes"

2. "📚 Eventos de formación profesional"

3. "🌍 ¿Qué eventos hay sobre migrantes?"

4. "📧 Envíame la agenda semanal por email"
```

---

## 🔌 Paso 3: Actualizar Actions (LO MÁS IMPORTANTE)

### 3.1 Ve a la sección "Actions"

En el editor del GPT, scroll hasta **"Actions"**

### 3.2 Opción A: Importar desde URL (Recomendado)

1. Click en **"Create new action"** (o editar la existente)
2. En **"Schema"**, selecciona **"Import from URL"**
3. Pega esta URL (reemplaza con tu URL de Railway):

```
https://TU-URL-DE-RAILWAY.up.railway.app/openapi.json
```

**Ejemplo**:
```
https://agente-tercer-sector-production.up.railway.app/openapi.json
```

4. Click en **"Import"**
5. El schema se actualizará automáticamente

### 3.2 Opción B: Pegar Schema Manualmente

Si prefieres pegar el schema manualmente:

1. Abre el archivo `openapi.json` de tu proyecto
2. Copia TODO el contenido
3. Pégalo en el campo "Schema"
4. **IMPORTANTE**: Busca la sección `"servers"` y actualiza la URL:

```json
"servers": [
  {
    "url": "https://TU-URL-DE-RAILWAY.up.railway.app"
  }
]
```

### 3.3 Configurar Autenticación

En la sección **"Authentication"**:

1. **Type**: Selecciona **"API Key"**
2. **Auth Type**: Selecciona **"Bearer"**
3. **API Key**: Pega tu `SECRET_TOKEN` (el mismo del `.env` y Railway)

**Ejemplo**:
```
tu_token_largo_y_aleatorio_12345
```

4. Click en **"Save"**

---

## 🧪 Paso 4: Probar el GPT Actualizado

### 4.1 Pruebas Básicas

Click en **"Preview"** (arriba a la derecha) y prueba:

**Test 1: Búsqueda Simple**
```
Busca eventos en España
```

Deberías ver que el GPT llama a `get_events` y te muestra resultados.

**Test 2: Búsqueda con Filtros**
```
¿Qué eventos hay sobre inclusión laboral en Colombia?
```

**Test 3: Búsqueda por Fechas**
```
Muéstrame eventos de noviembre 2025
```

**Test 4: Registro de Actividad**
```
Registra que busqué eventos de formación
```

Deberías ver que llama a `log_activity`.

### 4.2 Verificar Errores

Si ves errores como:
- ❌ "Could not reach your API"
  → Verifica que Railway está corriendo
  → Verifica la URL en Actions

- ❌ "Invalid authentication"
  → Verifica el Bearer token
  → Asegúrate que coincide con SECRET_TOKEN en Railway

- ❌ "No events found"
  → Normal si la base está vacía
  → Puedes añadir eventos de prueba en `EVENTS_DB` en `app.py`

---

## 📊 Paso 5: Verificar Capabilities (Opcional)

En **"Configure"** → **"Capabilities"**:

### Recomendado activar:
- ✅ **Web Browsing**: Para buscar información adicional si es necesario
- ✅ **Code Interpreter**: Para análisis de datos si el usuario lo pide

### No necesario:
- ⬜ **DALL·E Image Generation**: No lo usamos

---

## 🎨 Paso 6: Actualizar Imagen del GPT (Opcional)

Puedes crear o actualizar la imagen del GPT:

**Sugerencias**:
- Icono representando tercer sector
- Colores: Azul, verde (solidaridad, cooperación)
- Elementos: Personas, mundo, manos unidas
- Banderas: España y Colombia

**Puedes usar DALL·E**:
```
"Crea un logo moderno para un asistente digital del tercer sector
llamado SIRIA, que conecta eventos sociales de España y Colombia,
con colores azul y verde, estilo profesional y minimalista"
```

---

## ✅ Paso 7: Guardar y Publicar

1. Click en **"Save"** (arriba a la derecha)
2. Decide la visibilidad:
   - **Only me**: Solo tú puedes usar el GPT
   - **Anyone with the link**: Compartible por link
   - **Public**: Listado en GPT Store (requiere aprobación)

3. Click en **"Confirm"**

---

## 🔄 Diferencias Clave con la Versión Anterior

### Lo que CAMBIÓ:

| Anterior | Ahora |
|----------|-------|
| API básica con eventos mock | Sistema completo con 22+ fuentes reales |
| Sin clasificación | Clasificación inteligente con IA |
| Sin filtros avanzados | Filtros por país, categoría, fecha |
| No había deduplicación | Sistema avanzado de deduplicación |
| Eventos estáticos | Actualización semanal automática |
| Endpoints simples | 6 endpoints con funcionalidad completa |

### Lo que se AÑADIÓ:

✅ Sistema de scraping de 22+ organizaciones
✅ Clasificador con OpenAI GPT-4
✅ Deduplicación inteligente
✅ Generación de Excel profesional
✅ Envío de emails con adjuntos
✅ Scheduler semanal automático
✅ Sistema de logging
✅ Integración con Google Sheets

---

## 📱 Paso 8: Compartir tu GPT (Opcional)

Si quieres que otros usen tu GPT:

1. Click en el GPT en "My GPTs"
2. Click en el botón de **compartir** (arriba)
3. Selecciona **"Anyone with the link"**
4. Copia el link
5. Comparte: `https://chat.openai.com/g/g-XXXXX-siria`

---

## 🆘 Troubleshooting Común

### Problema: "Action not working"

**Solución**:
1. Ve a Actions → Edit
2. Verifica URL del servidor
3. Prueba la URL manualmente: `https://TU-URL/health`
4. Verifica Bearer token

### Problema: "No se encuentran eventos"

**Solución**:
- Es normal al inicio (base de datos vacía)
- Puedes añadir eventos de prueba en `app.py`
- O esperar la primera actualización semanal

### Problema: "Authentication failed"

**Solución**:
1. Verifica SECRET_TOKEN en Railway
2. Verifica que coincide con el Bearer en GPT Actions
3. Regenera el token si es necesario

### Problema: "Timeout"

**Solución**:
- Railway puede estar en sleep mode (plan free)
- Hacer una petición a `/health` para despertar el servicio
- Esperar 30 segundos y volver a intentar

---

## 📚 Recursos Adicionales

**Documentación completa**:
- `README.md` - Guía completa del proyecto
- `GPT_ACTIONS_SETUP.md` - Setup desde cero de GPT
- `RAILWAY_UPDATE.md` - Actualización de Railway
- `DEPENDENCIAS.md` - Todas las dependencias

**Testing**:
- Health Check: `https://TU-URL/health`
- OpenAPI: `https://TU-URL/openapi.json`
- Eventos: `https://TU-URL/get_events` (con Bearer token)

**Soporte**:
- Email: jcsiria@basecamp.world
- Logs de Railway: Ver en proyecto → Logs
- GitHub Issues: https://github.com/iutrera/agente-tercer-sector-/issues

---

## ✨ ¡Listo!

Tu GPT ahora está actualizado con todas las capacidades del sistema SIRIA completo.

**Prueba tu GPT con**:
```
"Hola SIRIA, ¿qué puedes hacer?"
```

Debería explicarte todas sus capacidades nuevas.

---

**¡Tu GPT está listo para ayudar a encontrar eventos del tercer sector!** 🎉
