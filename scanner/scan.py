"""
Haupt-Scanner.

Ablauf:
  1. Lade die bisher gesehenen Jobs aus data/jobs.json (Zustand).
  2. Frage für jeden VC dessen ATS-Feed ab.
  3. Filtere auf Deutschland + Praktikum/Einstieg.
  4. Vergleiche mit dem gespeicherten Zustand -> alles Neue.
  5. Sende für jede neue Stelle eine Telegram-Nachricht.
  6. Schreibe die aktualisierte, angereicherte Liste zurück nach data/jobs.json.

Läuft ohne Argumente:  python scanner/scan.py
Erststart (kein Spam):  SCANNER_SEED=1 python scanner/scan.py
    -> markiert alle aktuell offenen Stellen als "bekannt", ohne zu benachrichtigen.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ermögliche `python scanner/scan.py` UND `python -m scanner.scan`
sys.path.insert(0, str(Path(__file__).resolve().parent))

import ats  # noqa: E402
import filters  # noqa: E402
import notify  # noqa: E402
from vcs import VCS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "jobs.json"
SEED_MODE = os.environ.get("SCANNER_SEED", "").strip() in ("1", "true", "yes")


def load_state() -> dict:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"updated_at": None, "jobs": []}


def save_state(state: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def scan() -> None:
    state = load_state()
    known = {j["id"]: j for j in state.get("jobs", [])}
    now = datetime.now(timezone.utc).isoformat()

    current: dict[str, dict] = {}
    new_jobs: list[dict] = []
    errors: list[str] = []

    for vc in VCS:
        name = vc["name"]
        try:
            raw_jobs = ats.fetch_jobs(vc["ats"], vc["slug"])
        except Exception as e:  # defensiv: ein VC darf den Lauf nicht killen
            errors.append(f"{name}: {e}")
            continue

        if not raw_jobs:
            # Kein Ergebnis kann "aktuell keine Stellen" ODER ein kaputter Feed sein.
            print(f"[scan] {name}: 0 Stellen vom Feed")
            continue

        matched = 0
        for job in raw_jobs:
            if not filters.keep(job):
                continue
            matched += 1
            job = {
                **job,
                "vc": name,
                "vc_website": vc.get("website", ""),
            }
            current[job["id"]] = job
            if job["id"] not in known:
                job["first_seen"] = now
                new_jobs.append(job)
            else:
                # Erstsichtungs-Datum erhalten
                job["first_seen"] = known[job["id"]].get("first_seen", now)
        print(f"[scan] {name}: {len(raw_jobs)} Stellen, {matched} passend")

    # Merge: aktuell offene passende Stellen sind der neue Zustand.
    merged = list(current.values())
    merged.sort(key=lambda j: j.get("first_seen", ""), reverse=True)

    state = {
        "updated_at": now,
        "count": len(merged),
        # Alle gescannten VCs, damit die Webseite auch VCs ohne offene Stelle anzeigen kann.
        "vcs": [{"name": vc["name"], "website": vc.get("website", "")} for vc in VCS],
        "jobs": merged,
        "errors": errors,
    }
    save_state(state)

    if SEED_MODE:
        print(f"[seed] {len(merged)} Stellen als bekannt markiert, keine Benachrichtigung.")
        return

    print(f"[scan] {len(new_jobs)} NEUE Stelle(n) gefunden.")
    for job in new_jobs:
        print(f"   + {job['vc']}: {job['title']} ({job.get('location','')})")
        notify.notify_new_job(job)

    if new_jobs and len(new_jobs) > 1:
        # Optionale Sammel-Info, falls mehrere auf einmal reinkommen
        pass


if __name__ == "__main__":
    scan()
