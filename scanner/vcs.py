"""
Kuratierte Liste der zu scannenden VCs.

Jeder Eintrag:
    name    -> Anzeigename
    website -> Karriere-/Website-Link (für die UI)
    ats     -> eines von: personio | greenhouse | lever | ashby | recruitee | workable
                          | join | getro
    slug    -> die firmenspezifische Kennung im jeweiligen ATS

So findest du den slug:
    - Personio:   URL der Karriereseite ist meist {slug}.jobs.personio.de
    - Greenhouse: boards.greenhouse.io/{slug}  oder im Bewerbungslink
    - Lever:      jobs.lever.co/{slug}
    - Ashby:      jobs.ashbyhq.com/{slug}
    - Recruitee:  {slug}.recruitee.com
    - Workable:   apply.workable.com/{slug}
    - JOIN:       join.com/companies/{slug}
    - Getro:      "<board-host>/<company-slug>", z.B. "jobs.earlybird.com/earlybird-venture-capital".
                  Das Board listet auch Portfolio-Stellen; der Adapter filtert auf die
                  Stellen des VCs selbst. Den company-slug findest du in der URL
                  <board-host>/companies/<company-slug>.

Bevorzugt den direkten ATS des VCs (Personio, Ashby ...) gegenüber Getro, wenn bekannt.

Neue VCs einfach unten anhängen. Falsche/leere Feeds liefern einfach 0 Stellen
und stören den Rest nicht. Steht im Actions-Log ("X Stellen vom Feed") dauerhaft 0,
stimmt entweder ats/slug nicht oder der VC hat gerade nichts offen.

Stand der Prüfung (18.09.2026): Personio/Ashby/Recruitee/Getro liefern echte Daten.
Der JOIN-Adapter erreicht die API, war aber bisher nur gegen leere Boards testbar
(Project A, Picus haben aktuell keine offenen Stellen), die Feldnamen sind daher
noch nicht an einer echten Stelle bestätigt.
"""

VCS: list[dict] = [
    {
        "name": "Earlybird",
        "website": "https://earlybird.com/",
        "ats": "personio",
        "slug": "earlybirdvc-gmbh",
    },
    {
        "name": "HV Capital",
        "website": "https://hvcapital.com/",
        "ats": "ashby",
        "slug": "hv",
    },
    {
        "name": "Lakestar",
        "website": "https://lakestar.com/",
        "ats": "personio",
        "slug": "lakestar",
    },
    {
        "name": "Point Nine",
        "website": "https://www.pointnine.com/",
        "ats": "recruitee",
        "slug": "pointnine",
    },
    {
        "name": "Speedinvest",
        "website": "https://careers.speedinvest.com/companies/speedinvest",
        "ats": "getro",
        "slug": "careers.speedinvest.com/speedinvest",
    },
    {
        "name": "Cherry Ventures",
        "website": "https://talent.cherry.vc/companies/cherry-ventures",
        "ats": "getro",
        "slug": "talent.cherry.vc/cherry-ventures",
    },
    {
        "name": "Project A Ventures",
        "website": "https://join.com/companies/project-a",
        "ats": "join",
        "slug": "project-a",
    },
    {
        "name": "Picus Capital",
        "website": "https://join.com/companies/picuscap",
        "ats": "join",
        "slug": "picuscap",
    },
    {
        "name": "High-Tech Gründerfonds (HTGF)",
        "website": "https://www.htgf.de/de/karriere/",
        "ats": "personio",
        "slug": "htgf",
    },
]
