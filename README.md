# 🎯 VC Scanner

Findet automatisch **Praktika & Einstiegsstellen bei Venture-Capital-Fonds in
Deutschland** – direkt von den Karriereseiten der VCs (nicht deren Portfolio-Firmen).

- 🌐 **Webseite** (Emergers-Stil) mit allen offenen Stellen
- 🤖 **Telegram-Push** bei jeder neuen Stelle
- ⚙️ Läuft **komplett kostenlos** auf GitHub Actions + GitHub Pages – kein Server

---

## So funktioniert es

```
GitHub Actions (Cron alle 3h)
  → fragt den Karriere-Feed jedes VCs ab (Personio, Greenhouse, Lever, Ashby …)
  → filtert: nur Deutschland + nur Praktikum/Einstieg
  → vergleicht mit data/jobs.json (letzter Stand)
  → neue Stelle?  → Telegram-Nachricht
  → schreibt & committet data/jobs.json
GitHub Pages  → zeigt index.html, das data/jobs.json lädt
```

Weil jeder VC **direkt** an seiner eigenen Karriereseite abgefragt wird, tauchen
Portfolio-Stellen prinzipbedingt nie auf.

---

## Einrichtung (einmalig, ~10 Min)

### 1. Repo anlegen
Diesen Ordner in ein neues **GitHub-Repository** pushen (z. B. `vc-scanner`).

```bash
cd vc-scanner
git init && git add . && git commit -m "init vc-scanner"
git branch -M main
git remote add origin https://github.com/<DEIN-USER>/vc-scanner.git
git push -u origin main
```

### 2. Telegram-Bot erstellen
1. In Telegram **@BotFather** öffnen → `/newbot` → Namen vergeben → du bekommst einen **Token** (`123456:ABC...`).
2. Deine **Chat-ID** herausfinden: Schreibe deinem neuen Bot eine beliebige Nachricht,
   öffne dann im Browser:
   `https://api.telegram.org/bot<DEIN-TOKEN>/getUpdates`
   und suche `"chat":{"id":123456789,...}` → das ist deine Chat-ID.

### 3. Secrets in GitHub hinterlegen
Repo → **Settings → Secrets and variables → Actions → New repository secret**:
| Name | Wert |
|------|------|
| `TELEGRAM_BOT_TOKEN` | dein Bot-Token |
| `TELEGRAM_CHAT_ID` | deine Chat-ID |

### 4. GitHub Pages aktivieren
Repo → **Settings → Pages** → *Source: Deploy from a branch* → Branch `main`, Ordner `/ (root)` → Save.
Die Seite ist dann unter `https://<DEIN-USER>.github.io/vc-scanner/` erreichbar.

### 5. Ersten Lauf starten (ohne Benachrichtigungs-Spam)
Damit du nicht sofort 30 Nachrichten für bereits offene Stellen bekommst, einmal im
**Seed-Modus** laufen lassen: Repo → **Actions → VC Scan → Run workflow**.
> Für den allerersten Lauf empfiehlt sich lokal: `SCANNER_SEED=1 python scanner/scan.py`
> und das Ergebnis committen. Danach benachrichtigt jeder Lauf nur noch *neue* Stellen.

Fertig. Ab jetzt läuft alles automatisch alle 3 Stunden.

---

## Lokal testen

```bash
pip install -r requirements.txt
python scanner/scan.py            # scannt + zeigt neue Stellen (Telegram nur wenn Secrets gesetzt)
SCANNER_SEED=1 python scanner/scan.py   # markiert alles als bekannt, ohne Benachrichtigung
```
Ohne gesetzte Telegram-Variablen werden Nachrichten nur in der Konsole ausgegeben.

Webseite lokal ansehen:
```bash
python -m http.server 8000   # dann http://localhost:8000 öffnen
```

---

## VCs hinzufügen / anpassen

Alle VCs stehen in [`scanner/vcs.py`](scanner/vcs.py). Ein neuer Eintrag:

```python
{
    "name": "Earlybird",
    "website": "https://earlybird.com/careers",
    "ats": "personio",       # personio | greenhouse | lever | ashby | recruitee | workable
    "slug": "earlybird",     # die Kennung im jeweiligen ATS
},
```

**Slug finden:** Öffne die Karriereseite des VCs und schau in die URL des Bewerbungssystems:
- `xyz.jobs.personio.de` → `ats: personio`, `slug: xyz`
- `boards.greenhouse.io/xyz` → `ats: greenhouse`, `slug: xyz`
- `jobs.lever.co/xyz` → `ats: lever`, `slug: xyz`
- `jobs.ashbyhq.com/xyz` → `ats: ashby`, `slug: xyz`
- `xyz.recruitee.com` → `ats: recruitee`, `slug: xyz`
- `apply.workable.com/xyz` → `ats: workable`, `slug: xyz`

Steht im Actions-Log dauerhaft `0 Stellen vom Feed`, stimmt vermutlich `ats`/`slug` nicht,
oder der VC nutzt ein System ohne offenen Feed (dann eigenen Adapter in `scanner/ats.py` ergänzen).

## Filter anpassen

Die Keyword-Listen für Standort (Deutschland) und Level (Praktikum/Einstieg) stehen
in [`scanner/filters.py`](scanner/filters.py) und lassen sich leicht erweitern.

---

## Projektstruktur

```
vc-scanner/
├── index.html                 # Webseite (Emergers-Stil)
├── data/jobs.json             # Datenstand (von der Action gepflegt)
├── scanner/
│   ├── scan.py                # Hauptlauf
│   ├── vcs.py                 # Liste der VCs   ← hier VCs hinzufügen
│   ├── ats.py                 # Feed-Adapter je ATS
│   ├── filters.py             # Deutschland- & Level-Filter
│   └── notify.py              # Telegram
├── .github/workflows/scan.yml # Cron alle 3h
└── requirements.txt
```
