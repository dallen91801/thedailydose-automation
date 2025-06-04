import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from datetime import date

# === CONFIGURATION ===
SMTP_SERVER = "localhost"
SMTP_PORT = 25

SENDER = "news@thedailydose.live"
RECIPIENT = "dallen91801@gmail.com"
SUBJECT = "🧠 Your Daily Healthcare Digest"

# === FILE PATHS ===
today = date.today().isoformat()
html_path = Path(f"exports/daily_digest_{today}.html")

# === VALIDATION ===
if not html_path.exists():
    print(f"❌ Missing HTML digest: {html_path}")
    exit(1)

# === READ CONTENT ===
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# === BUILD EMAIL ===
msg = MIMEMultipart("alternative")
msg["From"] = SENDER
msg["To"] = RECIPIENT
msg["Subject"] = SUBJECT

plain_fallback = "Your email client does not support HTML. Visit https://thedailydose.live"
msg.attach(MIMEText(plain_fallback, "plain"))
msg.attach(MIMEText(html_content, "html"))

# === SEND ===
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.send_message(msg)
    print(f"✅ HTML digest sent to {RECIPIENT}")
except Exception as e:
    print(f"❌ Failed to send: {e}")
