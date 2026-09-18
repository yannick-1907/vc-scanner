"""
Telegram-Benachrichtigung. Nutzt die Bot-API direkt via HTTPS (keine Extra-Libs).

Konfiguration über Umgebungsvariablen (in GitHub als Secrets hinterlegt):
    TELEGRAM_BOT_TOKEN  -> Token von @BotFather
    TELEGRAM_CHAT_ID    -> deine Chat-ID (siehe README)

Ist eine der Variablen leer, werden Nachrichten nur geloggt statt gesendet
(praktisch für lokale Tests ohne Bot).
"""

from __future__ import annotations

import html
import os

import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()


def _enabled() -> bool:
    return bool(BOT_TOKEN and CHAT_ID)


def send(text: str) -> None:
    if not _enabled():
        print("[telegram] deaktiviert (kein Token/Chat-ID) — Nachricht:\n" + text)
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        resp = requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": False,
            },
            timeout=20,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[telegram] Senden fehlgeschlagen: {e}")


def notify_new_job(job: dict) -> None:
    """Formatiert und sendet eine Benachrichtigung für eine neue Stelle."""
    title = html.escape(job.get("title", "Neue Stelle"))
    vc = html.escape(job.get("vc", ""))
    location = html.escape(job.get("location", "") or "—")
    url = job.get("url", "")
    dept = html.escape(job.get("department", "") or "")

    lines = [
        "🚀 <b>Neue VC-Stelle</b>",
        "",
        f"🏢 <b>{vc}</b>",
        f"💼 {title}",
        f"📍 {location}",
    ]
    if dept:
        lines.append(f"🗂️ {dept}")
    if url:
        lines.append("")
        lines.append(f'🔗 <a href="{html.escape(url)}">Zur Stelle</a>')
    send("\n".join(lines))
