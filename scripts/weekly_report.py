"""
Informe semanal de conversiones — convertidorwebp.com
Requiere variables de entorno:
  GA4_PROPERTY_ID   → el ID numérico de tu propiedad GA4 (ej. 123456789)
  GA4_CREDENTIALS   → contenido JSON de la service account (todo en una línea)
  EMAIL_TO          → destinatario (migueldelgadogarcia@gmail.com)
  SMTP_USER         → tu Gmail (migueldelgadogarcia@gmail.com)
  SMTP_PASSWORD     → contraseña de aplicación de Gmail (16 chars)
"""

import os, json, smtplib, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ── Configuración ──────────────────────────────────────────────────────────────
PROPERTY_ID   = os.environ["GA4_PROPERTY_ID"]
CREDENTIALS   = json.loads(os.environ["GA4_CREDENTIALS"])
EMAIL_TO      = os.environ["EMAIL_TO"]
SMTP_USER     = os.environ["SMTP_USER"]
SMTP_PASSWORD = os.environ["SMTP_PASSWORD"]

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]

PAGE_LABELS = {
    "es_home":  "🏠 Home ES",
    "es_jpg":   "📄 JPG a WebP (ES)",
    "es_png":   "📄 PNG a WebP (ES)",
    "es_jpeg":  "📄 JPEG a WebP (ES)",
    "en_home":  "🏠 Home EN",
    "en_jpg":   "📄 JPG to WebP (EN)",
    "en_png":   "📄 PNG to WebP (EN)",
    "en_jpeg":  "📄 JPEG to WebP (EN)",
}

# ── Fechas ─────────────────────────────────────────────────────────────────────
today     = datetime.date.today()
week_end  = today - datetime.timedelta(days=1)               # ayer
week_start = week_end - datetime.timedelta(days=6)           # hace 7 días
date_start = week_start.strftime("%Y-%m-%d")
date_end   = week_end.strftime("%Y-%m-%d")

# ── GA4 Data API ───────────────────────────────────────────────────────────────
creds   = service_account.Credentials.from_service_account_info(CREDENTIALS, scopes=SCOPES)
service = build("analyticsdata", "v1beta", credentials=creds)

response = service.properties().runReport(
    property=f"properties/{PROPERTY_ID}",
    body={
        "dateRanges": [{"startDate": date_start, "endDate": date_end}],
        "dimensions": [{"name": "customEvent:page_name"}],
        "metrics": [
            {"name": "eventCount"},
            {"name": "customEvent:image_count"},  # suma total de imágenes
        ],
        "dimensionFilter": {
            "filter": {
                "fieldName": "eventName",
                "stringFilter": {"matchType": "EXACT", "value": "image_convert"},
            }
        },
        "orderBys": [{"metric": {"metricName": "eventCount"}, "desc": True}],
    },
).execute()

# ── Procesar resultados ────────────────────────────────────────────────────────
rows = []
total_uses   = 0
total_images = 0

for row in response.get("rows", []):
    page_name  = row["dimensionValues"][0]["value"]
    uses       = int(row["metricValues"][0]["value"])
    img_total  = float(row["metricValues"][1]["value"] or 0)
    avg_images = round(img_total / uses, 1) if uses > 0 else 0
    label      = PAGE_LABELS.get(page_name, page_name)
    rows.append((label, uses, avg_images))
    total_uses   += uses
    total_images += img_total

global_avg = round(total_images / total_uses, 1) if total_uses > 0 else 0

# ── Construir HTML del email ───────────────────────────────────────────────────
rows_html = "\n".join(
    f"""<tr>
      <td style="padding:10px 16px;border-bottom:1px solid #f0f0f0;">{label}</td>
      <td style="padding:10px 16px;border-bottom:1px solid #f0f0f0;text-align:center;font-weight:600;">{uses}</td>
      <td style="padding:10px 16px;border-bottom:1px solid #f0f0f0;text-align:center;">{avg}</td>
    </tr>"""
    for label, uses, avg in rows
) or '<tr><td colspan="3" style="padding:16px;text-align:center;color:#999;">Sin datos esta semana</td></tr>'

html = f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f9fafb;margin:0;padding:24px;">
  <div style="max-width:560px;margin:0 auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.08);">

    <div style="background:#4f46e5;padding:28px 32px;">
      <h1 style="color:#fff;margin:0;font-size:1.3rem;">📊 Informe semanal</h1>
      <p style="color:#c7d2fe;margin:4px 0 0;font-size:.9rem;">
        {week_start.strftime("%-d %b")} – {week_end.strftime("%-d %b %Y")} · convertidorwebp.com
      </p>
    </div>

    <div style="padding:24px 32px;">
      <div style="display:flex;gap:16px;margin-bottom:28px;">
        <div style="flex:1;background:#f5f3ff;border-radius:8px;padding:16px;text-align:center;">
          <div style="font-size:2rem;font-weight:700;color:#4f46e5;">{total_uses}</div>
          <div style="font-size:.8rem;color:#6b7280;margin-top:4px;">conversiones totales</div>
        </div>
        <div style="flex:1;background:#f0fdf4;border-radius:8px;padding:16px;text-align:center;">
          <div style="font-size:2rem;font-weight:700;color:#16a34a;">{global_avg}</div>
          <div style="font-size:.8rem;color:#6b7280;margin-top:4px;">imágenes por uso (media)</div>
        </div>
      </div>

      <h2 style="font-size:.95rem;font-weight:600;color:#374151;margin:0 0 12px;">Por página</h2>
      <table style="width:100%;border-collapse:collapse;font-size:.88rem;">
        <thead>
          <tr style="background:#f9fafb;">
            <th style="padding:10px 16px;text-align:left;color:#6b7280;font-weight:600;border-bottom:2px solid #e5e7eb;">Página</th>
            <th style="padding:10px 16px;text-align:center;color:#6b7280;font-weight:600;border-bottom:2px solid #e5e7eb;">Usos</th>
            <th style="padding:10px 16px;text-align:center;color:#6b7280;font-weight:600;border-bottom:2px solid #e5e7eb;">Media imgs</th>
          </tr>
        </thead>
        <tbody>
          {rows_html}
        </tbody>
      </table>
    </div>

    <div style="padding:16px 32px 24px;text-align:center;">
      <a href="https://analytics.google.com" style="font-size:.8rem;color:#9ca3af;text-decoration:none;">
        Ver GA4 completo →
      </a>
    </div>
  </div>
</body>
</html>"""

# ── Enviar email ───────────────────────────────────────────────────────────────
msg = MIMEMultipart("alternative")
msg["Subject"] = f"📊 Informe semanal convertidorwebp.com ({week_start.strftime('%-d %b')}–{week_end.strftime('%-d %b')})"
msg["From"]    = SMTP_USER
msg["To"]      = EMAIL_TO
msg.attach(MIMEText(html, "html"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.sendmail(SMTP_USER, EMAIL_TO, msg.as_string())

print(f"✅ Informe enviado a {EMAIL_TO}  ({total_uses} conversiones, media {global_avg} imgs)")
