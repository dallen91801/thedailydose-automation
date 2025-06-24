from markdown2 import markdown
from datetime import date

today = date.today().isoformat()
with open(f"exports/daily_digest_{today}.md", "r") as f:
    md = f.read()

html = markdown(md)

with open(f"exports/daily_digest_{today}.html", "w") as f:
    f.write(f"<html><body>{html}</body></html>")
