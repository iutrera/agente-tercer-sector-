import os
import base64
import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify, send_file, abort
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SECRET_TOKEN = os.getenv("SECRET_TOKEN", "")
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
DEFAULT_FROM = os.getenv("DEFAULT_FROM", SMTP_USER)

app = Flask(__name__)

# --- Seguridad básica: exigir Authorization: Bearer <SECRET_TOKEN> ---
PUBLIC_PATHS = {"/health", "/openapi.json"}

@app.before_request
def check_auth():
    if request.path in PUBLIC_PATHS:
        return
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        abort(401, description="Missing Bearer token")
    token = auth.split(" ", 1)[1].strip()
    if token != SECRET_TOKEN:
        abort(401, description="Invalid token")

# --- Salud ---
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat() + "Z"})

# --- Servir el esquema OpenAPI para registrar la Acción en el GPT ---
@app.route("/openapi.json", methods=["GET"])
def openapi_schema():
    return send_file("openapi.json", mimetype="application/json")

# --- Datos de ejemplo: eventos (en producción, esto vendrá de tu BD/Sheets) ---
EVENTS_DB = [
    {
        "nombre": "Foro de Inclusión Laboral 2025",
        "entidad": "Fundación ONCE",
        "fecha": "2025-11-04",
        "hora": "10:00",
        "modalidad": "Presencial",
        "lugar": "Madrid",
        "enlace": "https://fundaciononce.es/foro",
        "pais": "España",
        "categoria": "Inclusión laboral"
    },
    {
        "nombre": "Webinar: Formación Profesional para Migrantes",
        "entidad": "Entreculturas",
        "fecha": "2025-11-12",
        "hora": "16:00",
        "modalidad": "Online",
        "lugar": "",
        "enlace": "https://entreculturas.org/webinar",
        "pais": "España",
        "categoria": "Acompañamiento a migrantes"
    },
    {
        "nombre": "Seminario de Cooperación Internacional",
        "entidad": "Fundación La Caixa",
        "fecha": "2025-11-20",
        "hora": "09:30",
        "modalidad": "Presencial",
        "lugar": "Barcelona",
        "enlace": "https://fundacionlacaixa.org/seminario",
        "pais": "España",
        "categoria": "Cooperación internacional y desarrollo"
    }
]

# --- GET /get_events: devuelve la lista de eventos (filtros opcionales) ---
@app.route("/get_events", methods=["GET"])
def get_events():
    """
    Parámetros opcionales:
      - from_date (YYYY-MM-DD)
      - to_date   (YYYY-MM-DD)
      - pais      (España|Colombia)
      - categoria (texto libre)
    """
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    pais = request.args.get("pais")
    categoria = request.args.get("categoria")

    def in_range(e):
        try:
            d = datetime.strptime(e.get("fecha", ""), "%Y-%m-%d").date()
        except Exception:
            return False
        if from_date:
            try:
                if d < datetime.strptime(from_date, "%Y-%m-%d").date():
                    return False
            except Exception:
                pass
        if to_date:
            try:
                if d > datetime.strptime(to_date, "%Y-%m-%d").date():
                    return False
            except Exception:
                pass
        return True

    results = [e for e in EVENTS_DB if in_range(e)]
    if pais:
        results = [e for e in results if e.get("pais", "").lower() == pais.lower()]
    if categoria:
        results = [e for e in results if categoria.lower() in e.get("categoria", "").lower()]

    return jsonify(results)

# --- POST /log_activity: registrar logs que envíe el GPT ---
@app.route("/log_activity", methods=["POST"])
def log_activity():
    data = request.json or {}
    print(f"[{datetime.now().isoformat()}] GPT_LOG: {data}")
    return jsonify({"status": "ok"})

# --- POST /send_email: enviar correo con (opcional) adjunto base64 ---
@app.route("/send_email", methods=["POST"])
def send_email():
    """
    JSON esperado:
    {
      "to": "destinatario@dominio.com",
      "subject": "Asunto",
      "body": "Texto del mensaje (puede ser HTML si pones content_type='html')",
      "content_type": "plain" | "html",  (opcional, por defecto 'plain')
      "attachment_base64": "....",       (opcional)
      "filename": "agenda_eventos.xlsx"  (opcional, requerido si hay adjunto)
    }
    """
    payload = request.json or {}
    to = payload.get("to")
    subject = payload.get("subject", "")
    body = payload.get("body", "")
    content_type = (payload.get("content_type") or "plain").lower()
    attachment_b64 = payload.get("attachment_base64")
    filename = payload.get("filename")

    if not to:
        abort(400, description="Missing 'to'")
    if not DEFAULT_FROM:
        abort(500, description="DEFAULT_FROM not configured")

    msg = EmailMessage()
    msg["From"] = DEFAULT_FROM
    msg["To"] = to
    msg["Subject"] = subject

    if content_type == "html":
        msg.add_alternative(body, subtype="html")
    else:
        msg.set_content(body)

    if attachment_b64:
        if not filename:
            abort(400, description="Missing 'filename' for attachment")
        try:
            data = base64.b64decode(attachment_b64)
        except Exception as ex:
            abort(400, description=f"Invalid base64: {ex}")
        msg.add_attachment(data, maintype="application", subtype="octet-stream", filename=filename)

    try:
        if SMTP_USE_TLS:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        if SMTP_USER and SMTP_PASS:
            server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
    except Exception as ex:
        abort(500, description=f"SMTP error: {ex}")

    return jsonify({"status": "sent"})

if __name__ == "__main__":
    # Ejecuta en 0.0.0.0 para que ngrok lo pueda ver
    port = int(os.getenv('PORT', 8000))
    app.run(host="0.0.0.0", port=port)
