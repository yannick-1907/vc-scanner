"""
Filter: Behalte nur (a) Deutschland-Standorte und (b) Praktikums-/Einstiegsstellen.

Beide Filter arbeiten rein textbasiert auf Titel + Standort, damit sie ATS-übergreifend
funktionieren. Die Keyword-Listen sind bewusst leicht anpassbar.
"""

from __future__ import annotations

import re

# --------------------------------------------------------------------------- #
# (a) Standort: Deutschland
# --------------------------------------------------------------------------- #
# Deutsche Städte mit VC-Präsenz + Länderbezeichnungen. "Remote" wird optional
# akzeptiert (siehe ALLOW_REMOTE), da viele Remote-Stellen DACH meinen.
GERMANY_TERMS = [
    "germany", "deutschland", "german",
    "berlin", "munich", "münchen", "muenchen", "hamburg", "frankfurt",
    "cologne", "köln", "koeln", "düsseldorf", "duesseldorf", "dusseldorf",
    "stuttgart", "bonn", "leipzig", "hannover", "hanover", "karlsruhe",
    "heidelberg", "mannheim", "nuremberg", "nürnberg", "nuernberg",
    "dresden", "essen", "dortmund",
]
ALLOW_REMOTE = True  # Remote-Stellen mit aufnehmen (oft DACH-weit)
REMOTE_TERMS = ["remote", "hybrid"]

# --------------------------------------------------------------------------- #
# (b) Stellen-Level: Praktikum + Einstieg nach dem Studium
# --------------------------------------------------------------------------- #
# Positive Signale im Titel.
ENTRY_TERMS = [
    # Praktikum
    "praktikum", "praktikant", "praktikantin", "praktikanten", "intern", "internship", "interns",
    # Werkstudent
    "werkstudent", "werkstudentin", "werkstudenten", "working student", "student assistant",
    # Absolvent / Einstieg
    "absolvent", "absolventen", "absolventin", "graduate", "new grad", "entry level", "entry-level",
    "berufseinsteiger", "trainee", "junior", "einsteiger", "einstieg",
    # VC-typische Einstiegsrollen
    "analyst", "investment analyst", "associate", "associate intern", "fellow", "fellowship",
    "venture fellow", "campus",
]

# Negative Signale: schließen Senior-/Führungsrollen aus, auch wenn z.B.
# "Associate" oder "Analyst" im Titel steht.
SENIOR_TERMS = [
    "senior", "lead", "principal", "head of", "director", "vp ", "vice president",
    "partner", "chief", "manager", "managing", "expert", "staff",
    "(sr", "sr.", "ii", "iii",
]


def _norm(s: str) -> str:
    return (s or "").lower()


def _contains_any(text: str, terms: list[str]) -> bool:
    """Ganzwort-Treffer: "intern" trifft nicht "international", "essen" nicht "essential"."""
    return any(re.search(rf"(?<![a-zäöüß]){re.escape(t.strip())}(?![a-zäöüß])", text) for t in terms)


def is_germany(job: dict) -> bool:
    loc = _norm(job.get("location", ""))
    # Manche ATS packen den Ort in den Titel/Department -> mitprüfen.
    haystack = f"{loc} {_norm(job.get('title',''))} {_norm(job.get('department',''))}"
    if _contains_any(haystack, GERMANY_TERMS):
        return True
    if ALLOW_REMOTE and _contains_any(loc, REMOTE_TERMS):
        return True
    return False


def is_entry_level(job: dict) -> bool:
    title = _norm(job.get("title", ""))
    if not title:
        return False
    # Senior-Ausschluss zuerst
    if _contains_any(f" {title} ", SENIOR_TERMS):
        # Ausnahme: "Junior ... Senior..." kommt praktisch nicht vor; wenn doch
        # ein Praktikum/Intern explizit drinsteht, trotzdem behalten.
        if not _contains_any(title, ["praktikum", "praktikant", "intern", "internship", "werkstudent", "working student"]):
            return False
    return _contains_any(title, ENTRY_TERMS)


def keep(job: dict) -> bool:
    """True, wenn der Job in Deutschland ist UND Praktikum/Einstieg."""
    return is_germany(job) and is_entry_level(job)
