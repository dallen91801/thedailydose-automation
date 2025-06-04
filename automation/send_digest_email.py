import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from datetime import date

# === CONFIGURATION ===
USE_OUTLOOK = False  # Not in use, local SMTP relay only
LOCAL_SMTP_SERVER = "localhost"
LOCAL_SMTP_PORT = 25

# Email meta
SENDER = "news@thedailydose.live"
RECIPIENT = "dallen91801@gmail.com"
SUBJECT = "🧠 Your Daily Healthcare Digest"

# === FILE PATHS ===
today = date.today().isoformat()
html_path = Path(f"exports/daily_digest_{today}.html")

# === FILE VALIDATION ===
if not html_path.exists():
    print(f"❌ Missing HTML digest: {html_path}")
    exit(1)

# === LOAD HTML BODY ===
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# === COMPOSE EMAIL ===
msg = MIMEMultipart("alternative")
msg["From"] = SENDER
msg["To"] = RECIPIENT
msg["Subject"] = SUBJECT

# Attach fallback plain text + full HTML body
msg.attach(MIMEText("Your email client does not support HTML.\nVisit https://thedailydose.live", "plain"))
msg.attach(MIMEText(html_content, "html"))

# === SEND MAIL ===
try:
    with smtplib.SMTP(LOCAL_SMTP_SERVER, LOCAL_SMTP_PORT) as server:
        server.send_message(msg)
    print(f"✅ HTML digest sent to {RECIPIENT}")
except Exception as e:
    print(f"❌ Failed to send: {e}")
