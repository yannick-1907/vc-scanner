"""
Kuratierte Liste der zu scannenden VCs.

Jeder Eintrag:
    name    -> Anzeigename
    website -> Karriere-/Website-Link (für die UI)
    ats     -> eines von: personio | greenhouse | lever | ashby | recruitee | workable
                          | join | getro | smartrecruiters | trakstar
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

    - SmartRecruiters: "<company>" oder "<company>|<Stichwort>". Mit Stichwort werden nur Stellen
                  behalten, deren Titel es enthaelt (GFC: "RocketInternet|Global Founders Capital").
    - Trakstar:   {slug}.hire.trakstar.com

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
    {
        "name": "Creandum",
        "website": "https://creandum.com/",
        "ats": "recruitee",
        "slug": "creandum",
    },
    {
        "name": "DN Capital",
        "website": "https://dncapital.hire.trakstar.com/",
        "ats": "trakstar",
        "slug": "dncapital",
    },
    {
        "name": "Global Founders Capital",
        "website": "https://jobs.smartrecruiters.com/RocketInternet",
        "ats": "smartrecruiters",
        "slug": "RocketInternet|Global Founders Capital",
    },
    {
        "name": "UVC Partners",
        "website": "https://talent.uvcpartners.com/companies/uvc-partners-2",
        "ats": "getro",
        "slug": "talent.uvcpartners.com/uvc-partners-2",
    },
    {
        "name": "Headline",
        "website": "https://join.com/companies/headline",
        "ats": "join",
        "slug": "headline",
    },
    {
        "name": "Atlantic Labs",
        "website": "https://join.com/companies/atlanticlabs",
        "ats": "join",
        "slug": "atlanticlabs",
    },
    {
        "name": "Antler",
        "website": "https://join.com/companies/antler",
        "ats": "join",
        "slug": "antler",
    },
    {
        "name": "btov / b2venture",
        "website": "https://join.com/companies/b2venture",
        "ats": "join",
        "slug": "b2venture",
    },
    {
        "name": "Visionaries Club",
        "website": "https://join.com/companies/visionariesclub",
        "ats": "join",
        "slug": "visionariesclub",
    },
    {
        "name": "Wellington Partners",
        "website": "https://join.com/companies/wellington-partners",
        "ats": "join",
        "slug": "wellington-partners",
    },
    {
        "name": "Vorwerk Ventures",
        "website": "https://join.com/companies/vorwerkventures",
        "ats": "join",
        "slug": "vorwerkventures",
    },
    {
        "name": "Senovo",
        "website": "https://join.com/companies/senovo",
        "ats": "join",
        "slug": "senovo",
    },
    {
        "name": "coparion",
        "website": "https://join.com/companies/coparion",
        "ats": "join",
        "slug": "coparion",
    },
    {
        "name": "Cusp Capital",
        "website": "https://join.com/companies/cuspcapital",
        "ats": "join",
        "slug": "cuspcapital",
    },
    {
        "name": "Extantia Capital",
        "website": "https://join.com/companies/extantia",
        "ats": "join",
        "slug": "extantia",
    },
    {
        "name": "JOIN Capital",
        "website": "https://join-capital.com/",
        "ats": "personio",
        "slug": "join-capital",
    },
    {
        "name": "General Catalyst",
        "website": "https://job-boards.greenhouse.io/generalcatalyst",
        "ats": "greenhouse",
        "slug": "generalcatalyst",
    },
    {
        "name": "BITKRAFT Ventures",
        "website": "https://boards.greenhouse.io/bitkraft",
        "ats": "greenhouse",
        "slug": "bitkraft",
    },
]
