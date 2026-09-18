"""
Kuratierte Liste der zu scannenden VCs.

Jeder Eintrag:
    name    -> Anzeigename
    website -> Karriere-/Website-Link (für die UI)
    ats     -> eines von: personio | greenhouse | lever | ashby | recruitee | workable
    slug    -> die firmenspezifische Kennung im jeweiligen ATS

So findest du den slug:
    - Personio:   URL der Karriereseite ist meist {slug}.jobs.personio.de
    - Greenhouse: boards.greenhouse.io/{slug}  oder im Bewerbungslink
    - Lever:      jobs.lever.co/{slug}
    - Ashby:      jobs.ashbyhq.com/{slug}
    - Recruitee:  {slug}.recruitee.com
    - Workable:   apply.workable.com/{slug}

Neue VCs einfach unten anhängen. Falsche/leere Feeds liefern einfach 0 Stellen
und stören den Rest nicht.

HINWEIS: Die slugs unten werden beim ersten Deploy verifiziert/korrigiert.
Prüfe den Actions-Log ("X Stellen vom Feed") — steht dort dauerhaft 0, stimmt
vermutlich ats/slug nicht.
"""

VCS: list[dict] = [
    # --- Startliste (Testphase, wird gemeinsam erweitert) --------------------
    {
        "name": "Project A Ventures",
        "website": "https://www.project-a.com/careers",
        "ats": "greenhouse",
        "slug": "projecta",
    },
    {
        "name": "Cherry Ventures",
        "website": "https://www.cherry.vc/careers",
        "ats": "greenhouse",
        "slug": "cherryventures",
    },
    {
        "name": "Point Nine",
        "website": "https://www.pointnine.com/careers",
        "ats": "ashby",
        "slug": "pointnine",
    },
    {
        "name": "HV Capital",
        "website": "https://www.hvcapital.com/careers",
        "ats": "personio",
        "slug": "hvcapital",
    },
    {
        "name": "Picus Capital",
        "website": "https://www.picuscap.com/careers",
        "ats": "personio",
        "slug": "picuscapital",
    },
    {
        "name": "UVC Partners",
        "website": "https://www.uvcpartners.com/careers",
        "ats": "personio",
        "slug": "uvcpartners",
    },
    {
        "name": "High-Tech Gründerfonds (HTGF)",
        "website": "https://www.htgf.de/de/karriere/",
        "ats": "personio",
        "slug": "htgf",
    },
    {
        "name": "Speedinvest",
        "website": "https://www.speedinvest.com/careers",
        "ats": "greenhouse",
        "slug": "speedinvest",
    },
]
