"""
Kuratierte Liste der zu scannenden VCs.

Jeder Eintrag:
    name    -> Anzeigename
    website -> Karriere-/Website-Link (für die UI)
    ats     -> eines von: personio | greenhouse | lever | ashby | recruitee | workable
                          | join | getro | smartrecruiters | trakstar | breezy | careerpage
    slug    -> die firmenspezifische Kennung im jeweiligen ATS

Nur VCs mit auswertbarer Quelle stehen hier. VCs ohne auslesbaren Karrierefeed liegen in
scanner/vcs_not_scannable.py (vom Scanner ignoriert) und koennen bei Bedarf hierher verschoben
werden, sobald ein Feed gefunden ist. Ein VC kann mehrere Eintraege haben (mehrere Feeds),
der Name muss dann identisch sein.

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
    - Breezy HR:  {slug}.breezy.hr
    - careerpage: "<URL der Karriereseite>" oder "<URL>|<Ort>". Generischer Seiten-Scraper (Best effort)
                  fuer einfache HTML-Karriereseiten ohne Bewerbersystem. Der Ort ist der Fallback,
                  wenn die Seite keine deutsche Stadt nennt.

Bevorzugt den direkten ATS des VCs (Personio, Ashby ...) gegenüber Getro, wenn bekannt.

Neue VCs einfach unten anhängen. Falsche/leere Feeds liefern einfach 0 Stellen
und stören den Rest nicht. Steht im Actions-Log ("X Stellen vom Feed") dauerhaft 0,
stimmt entweder ats/slug nicht oder der VC hat gerade nichts offen.

Stand (19.09.2026): 156 VCs. Status je VC: Feed (Bewerbersystem, zuverlaessig) oder
Seitenpruefung (careerpage, best effort). Feeds wurden ueber den echten Kontonamen verifiziert.
Bei VCs mit 0 Stellen ist der Feed erreichbar, aber aktuell leer.
"""

VCS: list[dict] = [
    {
        "name": "1745 Ventures",
        "website": "https://www.1745ventures.com/careers",
        "ats": "careerpage",
        "slug": "https://www.1745ventures.com/careers|Deutschland",
    },
    {
        "name": "2150",
        "website": "https://2150.getro.com/jobs",
        "ats": "getro",
        "slug": "2150.getro.com/2150",
    },
    {
        "name": "3VC Partners",
        "website": "https://three.vc",
        "ats": "recruitee",
        "slug": "3vc",
    },
    {
        "name": "Ada Ventures",
        "website": "https://www.adaventures.com/talent-network",
        "ats": "careerpage",
        "slug": "https://www.adaventures.com/talent-network",
    },
    {
        "name": "AENU",
        "website": "https://www.aenu.com/careers",
        "ats": "join",
        "slug": "aenu",
    },
    {
        "name": "Allianz X",
        "website": "https://allianzx.com/jobs",
        "ats": "careerpage",
        "slug": "https://allianzx.com/jobs",
    },
    {
        "name": "Alstin Capital",
        "website": "https://alstin.capital/careers",
        "ats": "join",
        "slug": "alstin",
    },
    {
        "name": "Amino Capital",
        "website": "https://www.aminocapital.com/careers",
        "ats": "careerpage",
        "slug": "https://www.aminocapital.com/careers|Deutschland",
    },
    {
        "name": "Ananda Impact Ventures",
        "website": "https://ananda.vc",
        "ats": "recruitee",
        "slug": "anandaventuresgmbh",
    },
    {
        "name": "Antler",
        "website": "https://www.antler.co/careers",
        "ats": "join",
        "slug": "antler",
    },
    {
        "name": "Atlantic Labs",
        "website": "https://atlanticlabs.com/careers",
        "ats": "join",
        "slug": "atlanticlabs",
    },
    {
        "name": "Atlantis Ventures",
        "website": "https://www.atlantis-ventures.com/careers",
        "ats": "join",
        "slug": "atlantis-ventures",
    },
    {
        "name": "Avala Capital",
        "website": "https://avalacapital.com/",
        "ats": "join",
        "slug": "avalacapital",
    },
    {
        "name": "Backed VC",
        "website": "https://talent.backed.vc/jobs",
        "ats": "getro",
        "slug": "talent.backed.vc/backed-vc-2",
    },
    {
        "name": "Bain Capital Ventures",
        "website": "https://jobs.baincapitalventures.com/jobs",
        "ats": "careerpage",
        "slug": "https://jobs.baincapitalventures.com/jobs",
    },
    {
        "name": "Balderton Capital",
        "website": "https://careers.balderton.com/jobs",
        "ats": "careerpage",
        "slug": "https://careers.balderton.com/jobs",
    },
    {
        "name": "Battery Ventures",
        "website": "https://battery.com",
        "ats": "join",
        "slug": "battery",
    },
    {
        "name": "Bayern Kapital",
        "website": "https://bayernkapital.de/bayern-kapital/karriere/",
        "ats": "careerpage",
        "slug": "https://bayernkapital.de/bayern-kapital/karriere/|Deutschland",
    },
    {
        "name": "BITKRAFT Ventures",
        "website": "https://bitkraft.vc/careers",
        "ats": "greenhouse",
        "slug": "bitkraft",
    },
    {
        "name": "BitStone Capital",
        "website": "https://www.bitstone.capital/karriere/",
        "ats": "careerpage",
        "slug": "https://www.bitstone.capital/karriere/",
    },
    {
        "name": "Blossom Capital",
        "website": "https://www.blossomcap.com/talent",
        "ats": "careerpage",
        "slug": "https://www.blossomcap.com/talent",
    },
    {
        "name": "BlueYard Capital",
        "website": "https://blueyard.com",
        "ats": "join",
        "slug": "blueyard",
    },
    {
        "name": "Blumberg Capital",
        "website": "https://blumbergcapital.com/careers",
        "ats": "workable",
        "slug": "blumberg-capital",
    },
    {
        "name": "Bonventure",
        "website": "https://www.bonventure.de/careers",
        "ats": "join",
        "slug": "bonventure",
    },
    {
        "name": "Brandenburg Kapital",
        "website": "https://www.brandenburg-kapital.de/de/bk/karriere.html",
        "ats": "careerpage",
        "slug": "https://www.brandenburg-kapital.de/de/bk/karriere.html|Deutschland",
    },
    {
        "name": "Breakthrough Energy Ventures",
        "website": "https://www.breakthroughenergy.org/careers",
        "ats": "careerpage",
        "slug": "https://www.breakthroughenergy.org/careers",
    },
    {
        "name": "Brose Ventures",
        "website": "https://www.brose.com/de-en/career/",
        "ats": "careerpage",
        "slug": "https://www.brose.com/de-en/career/|Deutschland",
    },
    {
        "name": "btov / b2venture",
        "website": "https://www.b2venture.vc",
        "ats": "join",
        "slug": "b2venture",
    },
    {
        "name": "Börse Stuttgart Digital Ventures",
        "website": "https://www.bsdigital.com/karriere",
        "ats": "careerpage",
        "slug": "https://www.bsdigital.com/karriere|Deutschland",
    },
    {
        "name": "Capmont Technology",
        "website": "https://careers.cmont.com/companies/capmont-technology#content",
        "ats": "getro",
        "slug": "careers.cmont.com/capmont-technology",
    },
    {
        "name": "capnamic Ventures",
        "website": "https://capnamic.com/jobs",
        "ats": "careerpage",
        "slug": "https://capnamic.com/jobs|Köln",
    },
    {
        "name": "Cathay Innovation",
        "website": "https://cathayinnovation.com",
        "ats": "join",
        "slug": "cathayinnovation",
    },
    {
        "name": "Cherry Ventures",
        "website": "https://cherry.vc",
        "ats": "getro",
        "slug": "talent.cherry.vc/cherry-ventures",
    },
    {
        "name": "Cherry Ventures",
        "website": "https://cherry.vc",
        "ats": "workable",
        "slug": "cherry-ventures",
    },
    {
        "name": "coparion",
        "website": "https://join.com/companies/coparion",
        "ats": "join",
        "slug": "coparion",
    },
    {
        "name": "Creandum",
        "website": "https://creandum.com",
        "ats": "workable",
        "slug": "creandum",
    },
    {
        "name": "Creathor Ventures",
        "website": "https://www.creathor.com/careers",
        "ats": "careerpage",
        "slug": "https://www.creathor.com/careers",
    },
    {
        "name": "Cusp Capital",
        "website": "https://cuspcapital.com",
        "ats": "join",
        "slug": "cuspcapital",
    },
    {
        "name": "D11Z Ventures",
        "website": "https://d11z.com/jobs",
        "ats": "join",
        "slug": "d11z",
    },
    {
        "name": "DeepTech & Climate Fonds",
        "website": "https://dtcf.de/careers",
        "ats": "personio",
        "slug": "dtcf",
    },
    {
        "name": "Deutsche Telekom Capital Partners",
        "website": "https://www.dtcp.capital/careers",
        "ats": "breezy",
        "slug": "dtcp",
    },
    {
        "name": "DN Capital",
        "website": "https://dncapital.com",
        "ats": "trakstar",
        "slug": "dncapital",
    },
    {
        "name": "DST Global",
        "website": "https://dst.global/careers",
        "ats": "careerpage",
        "slug": "https://dst.global/careers",
    },
    {
        "name": "Earlybird",
        "website": "https://earlybird.com",
        "ats": "personio",
        "slug": "earlybirdvc-gmbh",
    },
    {
        "name": "Elaia",
        "website": "https://elaia.com/careers",
        "ats": "careerpage",
        "slug": "https://elaia.com/careers",
    },
    {
        "name": "Energy Impact Partners",
        "website": "https://www.energyimpactpartners.com/careers",
        "ats": "join",
        "slug": "energyimpactpartners",
    },
    {
        "name": "EQT Ventures",
        "website": "https://eqtgroup.com",
        "ats": "join",
        "slug": "eqtventures",
    },
    {
        "name": "EquityPitcher",
        "website": "https://jobs.equitypitcher.com/jobs",
        "ats": "careerpage",
        "slug": "https://jobs.equitypitcher.com/jobs|Deutschland",
    },
    {
        "name": "Eurazeo",
        "website": "https://www.eurazeo.com/en/talents",
        "ats": "careerpage",
        "slug": "https://www.eurazeo.com/en/talents",
    },
    {
        "name": "European Investment Fund (EIF)",
        "website": "https://www.eif.org/work-with-us/careers",
        "ats": "careerpage",
        "slug": "https://www.eif.org/work-with-us/careers",
    },
    {
        "name": "EWOR",
        "website": "https://www.ewor.com",
        "ats": "join",
        "slug": "ewor",
    },
    {
        "name": "Extantia Capital",
        "website": "https://join.com/companies/extantia",
        "ats": "join",
        "slug": "extantia",
    },
    {
        "name": "Fabric Ventures",
        "website": "https://careers.fabric.vc/jobs",
        "ats": "careerpage",
        "slug": "https://careers.fabric.vc/jobs",
    },
    {
        "name": "FinTech Collective",
        "website": "https://fintechcollective.com/careers",
        "ats": "careerpage",
        "slug": "https://fintechcollective.com/careers",
    },
    {
        "name": "First Momentum",
        "website": "https://jobs.firstmomentum.vc/jobs",
        "ats": "getro",
        "slug": "jobs.firstmomentum.vc/first-momentum-ventures-2",
    },
    {
        "name": "First Round Capital",
        "website": "https://www.firstround.com",
        "ats": "ashby",
        "slug": "firstround",
    },
    {
        "name": "Forbion",
        "website": "https://forbion.com/about-us/careers/",
        "ats": "careerpage",
        "slug": "https://forbion.com/about-us/careers/",
    },
    {
        "name": "Found Fair",
        "website": "https://foundfair.de/career/",
        "ats": "careerpage",
        "slug": "https://foundfair.de/career/|Deutschland",
    },
    {
        "name": "Foundamental",
        "website": "https://www.foundamental.com",
        "ats": "join",
        "slug": "foundamental",
    },
    {
        "name": "Founderful",
        "website": "https://jobs.founderful.com/jobs",
        "ats": "careerpage",
        "slug": "https://jobs.founderful.com/jobs",
    },
    {
        "name": "Freigeist Capital",
        "website": "https://freigeist.com/career/",
        "ats": "careerpage",
        "slug": "https://freigeist.com/career/",
    },
    {
        "name": "Freiraum VC",
        "website": "https://www.freiraum.vc/",
        "ats": "join",
        "slug": "freiraum",
    },
    {
        "name": "Futury Capital",
        "website": "https://futurycapital.vc/#home",
        "ats": "join",
        "slug": "futurycapital",
    },
    {
        "name": "General Atlantic",
        "website": "https://www.generalatlantic.com/careers",
        "ats": "greenhouse",
        "slug": "generalatlantic",
    },
    {
        "name": "General Catalyst",
        "website": "https://www.generalcatalyst.com",
        "ats": "greenhouse",
        "slug": "generalcatalyst",
    },
    {
        "name": "Global Founders Capital",
        "website": "https://www.globalfounders.vc",
        "ats": "smartrecruiters",
        "slug": "RocketInternet|Global Founders Capital",
    },
    {
        "name": "Green Generation Fund",
        "website": "https://www.ggf.vc/",
        "ats": "careerpage",
        "slug": "https://www.ggf.vc/|Deutschland",
    },
    {
        "name": "Greycroft",
        "website": "https://jobs.greycroft.com/companies",
        "ats": "getro",
        "slug": "jobs.greycroft.com/greycroft-2",
    },
    {
        "name": "GV",
        "website": "https://jobs.gv.com/jobs",
        "ats": "careerpage",
        "slug": "https://jobs.gv.com/jobs",
    },
    {
        "name": "Headline",
        "website": "https://headline.com",
        "ats": "join",
        "slug": "headline",
    },
    {
        "name": "High-Tech Gründerfonds (HTGF)",
        "website": "https://www.htgf.de/careers",
        "ats": "personio",
        "slug": "htgf",
    },
    {
        "name": "Highland Europe",
        "website": "https://careers.highlandeurope.com/jobs",
        "ats": "careerpage",
        "slug": "https://careers.highlandeurope.com/jobs",
    },
    {
        "name": "Hoxton Ventures",
        "website": "https://jobs.hoxtonventures.com/jobs",
        "ats": "careerpage",
        "slug": "https://jobs.hoxtonventures.com/jobs",
    },
    {
        "name": "HV Capital",
        "website": "https://hvcapital.com/careers",
        "ats": "ashby",
        "slug": "hv",
    },
    {
        "name": "IBB Ventures",
        "website": "https://www.ibbventures.de/en/jobs",
        "ats": "careerpage",
        "slug": "https://www.ibbventures.de/en/jobs|Deutschland",
    },
    {
        "name": "ICONIQ Capital",
        "website": "https://www.iconiq.com/careers",
        "ats": "careerpage",
        "slug": "https://www.iconiq.com/careers",
    },
    {
        "name": "IFB Innovationsstarter Hamburg",
        "website": "https://www.ifbhh.de/die-ifb-hamburg/karriere",
        "ats": "careerpage",
        "slug": "https://www.ifbhh.de/die-ifb-hamburg/karriere|Deutschland",
    },
    {
        "name": "Index Ventures",
        "website": "https://www.indexventures.com:443",
        "ats": "lever",
        "slug": "indexventures",
    },
    {
        "name": "Innovationsfonds Schleswig-Holstein",
        "website": "https://wtsh.de/de/karriere",
        "ats": "careerpage",
        "slug": "https://wtsh.de/de/karriere|Deutschland",
    },
    {
        "name": "Inovia Capital",
        "website": "https://careers.inovia.vc/jobs",
        "ats": "getro",
        "slug": "careers.inovia.vc/inovia-capital-2",
    },
    {
        "name": "Insight Partners",
        "website": "https://www.insightpartners.com/jobs",
        "ats": "smartrecruiters",
        "slug": "InsightPartners",
    },
    {
        "name": "Inventure",
        "website": "https://www.inventure.vc/portfolio",
        "ats": "careerpage",
        "slug": "https://www.inventure.vc/portfolio",
    },
    {
        "name": "Invisible Hand Ventures",
        "website": "https://www.i-hand.de/",
        "ats": "join",
        "slug": "invisiblehand",
    },
    {
        "name": "JOIN Capital",
        "website": "https://join-capital.com/",
        "ats": "personio",
        "slug": "join-capital",
    },
    {
        "name": "K5 Advisors",
        "website": "https://k5.io/",
        "ats": "careerpage",
        "slug": "https://k5.io/|Deutschland",
    },
    {
        "name": "KfW Capital",
        "website": "https://www.kfw-capital.de/Karriere/",
        "ats": "careerpage",
        "slug": "https://www.kfw-capital.de/Karriere/|Deutschland",
    },
    {
        "name": "Kiko Ventures",
        "website": "https://kiko.vc",
        "ats": "join",
        "slug": "kiko",
    },
    {
        "name": "Kompas VC",
        "website": "https://www.kompas.vc/careers",
        "ats": "careerpage",
        "slug": "https://www.kompas.vc/careers",
    },
    {
        "name": "Lakestar",
        "website": "https://www.lakestar.com",
        "ats": "personio",
        "slug": "lakestar",
    },
    {
        "name": "Latitude",
        "website": "https://jobs.phoenixcourt.vc/jobs",
        "ats": "careerpage",
        "slug": "https://jobs.phoenixcourt.vc/jobs",
    },
    {
        "name": "Left Lane Capital",
        "website": "https://jobs.leftlanecap.com/companies",
        "ats": "getro",
        "slug": "jobs.leftlanecap.com/left-lane-capital",
    },
    {
        "name": "Lifeline Ventures",
        "website": "https://www.lifelineventures.com/careers/",
        "ats": "careerpage",
        "slug": "https://www.lifelineventures.com/careers/",
    },
    {
        "name": "Lightrock",
        "website": "https://careers.lightrock.com/jobs",
        "ats": "careerpage",
        "slug": "https://careers.lightrock.com/jobs",
    },
    {
        "name": "Lightspeed Venture Partners",
        "website": "https://jobs.lsvp.com/jobs",
        "ats": "careerpage",
        "slug": "https://jobs.lsvp.com/jobs",
    },
    {
        "name": "LocalGlobe",
        "website": "https://jobs.phoenixcourt.vc/jobs",
        "ats": "careerpage",
        "slug": "https://jobs.phoenixcourt.vc/jobs",
    },
    {
        "name": "Lunar Ventures",
        "website": "https://www.lunar.vc/careers",
        "ats": "careerpage",
        "slug": "https://www.lunar.vc/careers",
    },
    {
        "name": "Mangrove Capital Partners",
        "website": "https://www.mangrove.vc/about/careers",
        "ats": "careerpage",
        "slug": "https://www.mangrove.vc/about/careers",
    },
    {
        "name": "Media Ventures",
        "website": "https://x.com/joinspotted",
        "ats": "careerpage",
        "slug": "https://x.com/joinspotted|Deutschland",
    },
    {
        "name": "Merantix Capital",
        "website": "https://careers.merantix-aicampus.com/companies?filter=eyJvcmdhbml6YXRpb24udG9waWNzLmNvbW11bml0aWVzIjpbIk1lcmFudGl4IFBvcnRmb2xpb3MiXX0%3D",
        "ats": "getro",
        "slug": "careers.merantix-aicampus.com/merantix-capital",
    },
    {
        "name": "Merck Ventures",
        "website": "https://merckventures.com/careers",
        "ats": "careerpage",
        "slug": "https://merckventures.com/careers",
    },
    {
        "name": "MIG Capital",
        "website": "https://www.mig.ag/",
        "ats": "join",
        "slug": "mig",
    },
    {
        "name": "Mountain Partners",
        "website": "https://mountain-partners.ch/careers",
        "ats": "join",
        "slug": "mountain",
    },
    {
        "name": "MS&AD Ventures",
        "website": "https://msad.vc/portfolio/join-digital",
        "ats": "careerpage",
        "slug": "https://msad.vc/portfolio/join-digital|Deutschland",
    },
    {
        "name": "Nauta Capital",
        "website": "https://www.nautacapital.com/careers",
        "ats": "join",
        "slug": "nautacapital",
    },
    {
        "name": "Next47",
        "website": "https://www.n47.com",
        "ats": "greenhouse",
        "slug": "next47",
    },
    {
        "name": "Northzone",
        "website": "https://northzone.com",
        "ats": "personio",
        "slug": "northzone",
    },
    {
        "name": "Norwest",
        "website": "https://www.norwest.com/portfolio-success/talent-and-network-development/",
        "ats": "careerpage",
        "slug": "https://www.norwest.com/portfolio-success/talent-and-network-development/",
    },
    {
        "name": "Notion Capital",
        "website": "https://jobs.notioncapital.com/jobs",
        "ats": "careerpage",
        "slug": "https://jobs.notioncapital.com/jobs",
    },
    {
        "name": "Octopus Ventures",
        "website": "https://octopusgroup.com/careers/listings/?search=&department=octopus-ventures",
        "ats": "careerpage",
        "slug": "https://octopusgroup.com/careers/listings/?search=&department=octopus-ventures",
    },
    {
        "name": "Partech",
        "website": "https://partechpartners.com",
        "ats": "join",
        "slug": "partechpartners",
    },
    {
        "name": "Peak",
        "website": "https://jobs.peak.capital/jobs",
        "ats": "getro",
        "slug": "jobs.peak.capital/peak-2-e3d8adee-675f-4e64-8a30-91bce686f8d7",
    },
    {
        "name": "Picus Capital",
        "website": "https://www.picuscap.com/career",
        "ats": "join",
        "slug": "picuscap",
    },
    {
        "name": "Planet A Ventures",
        "website": "https://planeta.vc/careers",
        "ats": "careerpage",
        "slug": "https://planeta.vc/careers",
    },
    {
        "name": "Point Nine",
        "website": "https://www.pointnine.com",
        "ats": "recruitee",
        "slug": "pointnine",
    },
    {
        "name": "Project A Ventures",
        "website": "https://www.project-a.vc/careers",
        "ats": "join",
        "slug": "project-a",
    },
    {
        "name": "Project A Ventures",
        "website": "https://www.project-a.vc/careers",
        "ats": "workable",
        "slug": "project-a",
    },
    {
        "name": "Promus Ventures",
        "website": "https://jobs.promusventures.com/jobs",
        "ats": "careerpage",
        "slug": "https://jobs.promusventures.com/jobs|Deutschland",
    },
    {
        "name": "Quadia Ventures",
        "website": "https://quadia.ch/2019/05/06/joint-quadia-and-degroof-petercam-fund-invests-in-opes-solutions-and-les-coteaux-nantais/",
        "ats": "careerpage",
        "slug": "https://quadia.ch/2019/05/06/joint-quadia-and-degroof-petercam-fund-invests-in-opes-solutions-and-les-coteaux-nantais/|Deutschland",
    },
    {
        "name": "Realyze Ventures",
        "website": "https://realyzeventures.com/jobs",
        "ats": "join",
        "slug": "realyzeventures",
    },
    {
        "name": "Redalpine",
        "website": "https://www.redalpine.com/career",
        "ats": "careerpage",
        "slug": "https://www.redalpine.com/career",
    },
    {
        "name": "Redstone",
        "website": "https://redstone.vc/careers",
        "ats": "personio",
        "slug": "redstone-digital-gmbh",
    },
    {
        "name": "Richmond View Ventures",
        "website": "https://rvv.tv/jobs",
        "ats": "join",
        "slug": "richmondviewventures",
    },
    {
        "name": "Rocket Internet",
        "website": "https://rocket-internet.com/careers",
        "ats": "careerpage",
        "slug": "https://rocket-internet.com/careers",
    },
    {
        "name": "Seed + Speed Ventures",
        "website": "https://www.seedandspeed.com",
        "ats": "join",
        "slug": "seedandspeed",
    },
    {
        "name": "Senovo",
        "website": "https://join.com/companies/senovo",
        "ats": "join",
        "slug": "senovo",
    },
    {
        "name": "Sequoia Capital",
        "website": "https://jobs.sequoiacap.com/jobs",
        "ats": "careerpage",
        "slug": "https://jobs.sequoiacap.com/jobs",
    },
    {
        "name": "Seventure Partners",
        "website": "https://www.seventure.fr/envoyer-une-candidature/",
        "ats": "careerpage",
        "slug": "https://www.seventure.fr/envoyer-une-candidature/|Deutschland",
    },
    {
        "name": "Smart Infrastructure Ventures",
        "website": "https://siventures.de/careers",
        "ats": "join",
        "slug": "smartinfrastructure",
    },
    {
        "name": "Sofina",
        "website": "https://www.sofinagroup.com/en/careers",
        "ats": "careerpage",
        "slug": "https://www.sofinagroup.com/en/careers",
    },
    {
        "name": "SoftBank Vision Fund",
        "website": "https://visionfund.com/work-with-us",
        "ats": "careerpage",
        "slug": "https://visionfund.com/work-with-us",
    },
    {
        "name": "Speedinvest",
        "website": "https://www.speedinvest.com",
        "ats": "getro",
        "slug": "careers.speedinvest.com/speedinvest",
    },
    {
        "name": "SURPLUS Equity Partners",
        "website": "https://www.alpx-group.com/careers",
        "ats": "careerpage",
        "slug": "https://www.alpx-group.com/careers|Deutschland",
    },
    {
        "name": "Swisscom Ventures",
        "website": "https://www.swisscom.ch/careers/",
        "ats": "careerpage",
        "slug": "https://www.swisscom.ch/careers/",
    },
    {
        "name": "TAKKT Beteiligungen",
        "website": "https://www.takkt.de/karriere",
        "ats": "careerpage",
        "slug": "https://www.takkt.de/karriere|Deutschland",
    },
    {
        "name": "Trill Impact",
        "website": "https://www.trillimpact.com/career",
        "ats": "careerpage",
        "slug": "https://www.trillimpact.com/career|Deutschland",
    },
    {
        "name": "TS Ventures",
        "website": "https://www.tsventures.io/careers",
        "ats": "join",
        "slug": "tsventures",
    },
    {
        "name": "UVC Partners",
        "website": "https://www.uvcpartners.com/jobs",
        "ats": "getro",
        "slug": "talent.uvcpartners.com/uvc-partners-2",
    },
    {
        "name": "Venionaire Capital",
        "website": "https://www.venionaire.com/about-alt/careers/?s=",
        "ats": "careerpage",
        "slug": "https://www.venionaire.com/about-alt/careers/?s=",
    },
    {
        "name": "Venture Stars",
        "website": "https://www.venture-stars.com/",
        "ats": "join",
        "slug": "venture-stars",
    },
    {
        "name": "Verve Ventures",
        "website": "https://www.verve.vc/join?utm_source=verve&utm_medium=nav&utm_campaign=main&utm_term=join&utm_content=text",
        "ats": "careerpage",
        "slug": "https://www.verve.vc/join?utm_source=verve&utm_medium=nav&utm_campaign=main&utm_term=join&utm_content=text",
    },
    {
        "name": "Visionaries Club",
        "website": "https://join.com/companies/visionariesclub",
        "ats": "join",
        "slug": "visionariesclub",
    },
    {
        "name": "Vorwerk Ventures",
        "website": "https://vorwerkventures.com",
        "ats": "join",
        "slug": "vorwerkventures",
    },
    {
        "name": "Wellington Partners",
        "website": "https://wellington-partners.com",
        "ats": "join",
        "slug": "wellington-partners",
    },
    {
        "name": "Wenvest Capital",
        "website": "https://www.wenvest.capital/",
        "ats": "join",
        "slug": "wenvest",
    },
    {
        "name": "World Fund",
        "website": "https://www.worldfund.vc/career",
        "ats": "careerpage",
        "slug": "https://www.worldfund.vc/career",
    },
    {
        "name": "XAnge",
        "website": "https://www.xange.vc",
        "ats": "join",
        "slug": "xange",
    },
    {
        "name": "Y Combinator",
        "website": "https://www.ycombinator.com/jobs",
        "ats": "careerpage",
        "slug": "https://www.ycombinator.com/jobs",
    },
    {
        "name": "Ysios Capital",
        "website": "https://ysioscapital.com/join-us/",
        "ats": "careerpage",
        "slug": "https://ysioscapital.com/join-us/",
    },
    {
        "name": "YZR Capital",
        "website": "https://yzr-capital.com/careers",
        "ats": "join",
        "slug": "yzr",
    },
    {
        "name": "LEA Partners",
        "website": "https://leapartners.jobs.personio.com/",
        "ats": "personio",
        "slug": "leapartners",
    },
    {
        "name": "T.Capital",
        "website": "https://t-capital.breezy.hr/",
        "ats": "breezy",
        "slug": "t-capital",
    },
    {
        "name": "xdeck",
        "website": "https://join.com/companies/xdeck",
        "ats": "join",
        "slug": "xdeck",
    },
    {
        "name": "DvH Ventures (Dieter von Holtzbrinck Ventures)",
        "website": "https://dvhventures.de/jobs/",
        "ats": "careerpage",
        "slug": "https://dvhventures.de/jobs/|Deutschland",
    },
]
