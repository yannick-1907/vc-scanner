"""
ATS-Adapter: Für jeden Bewerbungssystem-Typ (Personio, Greenhouse, Lever, Ashby,
Recruitee, Workable) gibt es eine Funktion, die die Karriere-Stellen eines VCs
als normalisierte Liste von Job-Dicts zurückgibt.

Ein normalisierter Job sieht so aus:
    {
        "id":        "<stabiler eindeutiger Schlüssel>",
        "title":     "Praktikant Investment (m/w/d)",
        "location":  "Berlin, Germany",
        "url":       "https://...",
        "department":"Investment",
        "raw":       {...}   # Original-Daten, optional
    }

Jeder Adapter fängt Netzwerk-/Parse-Fehler ab und gibt im Fehlerfall [] zurück,
damit ein defekter Feed den gesamten Scan nicht abbricht.
"""

from __future__ import annotations

import hashlib
import json
import re
from html import unescape as html_unescape
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
from typing import Callable

import requests

TIMEOUT = 20
HEADERS = {
    "User-Agent": "vc-scanner/1.0 (+https://github.com/)",
    "Accept": "application/json, text/xml, */*",
}


def _get(url: str) -> requests.Response:
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp


# --------------------------------------------------------------------------- #
# Personio  ->  https://{slug}.jobs.personio.de/xml
# --------------------------------------------------------------------------- #
def personio(slug: str) -> list[dict]:
    jobs: list[dict] = []
    for host in (f"https://{slug}.jobs.personio.de/xml", f"https://{slug}.jobs.personio.com/xml"):
        try:
            resp = _get(host)
        except requests.RequestException:
            continue
        try:
            root = ET.fromstring(resp.content)
        except ET.ParseError:
            continue

        for pos in root.iter("position"):
            def field(tag: str) -> str:
                el = pos.find(tag)
                return (el.text or "").strip() if el is not None and el.text else ""

            job_id = field("id")
            title = field("name")
            if not title:
                continue
            office = field("office")
            recruiting_category = field("recruitingCategory")
            # Personio-Bewerbungslink
            url = f"https://{slug}.jobs.personio.de/job/{job_id}" if job_id else host
            jobs.append(
                {
                    "id": f"personio:{slug}:{job_id or title}",
                    "title": title,
                    "location": office,
                    "url": url,
                    "department": recruiting_category or field("department"),
                }
            )
        if jobs:
            break
    return jobs


# --------------------------------------------------------------------------- #
# Greenhouse -> https://boards-api.greenhouse.io/v1/boards/{slug}/jobs
# --------------------------------------------------------------------------- #
def greenhouse(slug: str) -> list[dict]:
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=false"
    try:
        data = _get(url).json()
    except (requests.RequestException, ValueError):
        return []
    jobs = []
    for j in data.get("jobs", []):
        jobs.append(
            {
                "id": f"greenhouse:{slug}:{j.get('id')}",
                "title": (j.get("title") or "").strip(),
                "location": (j.get("location") or {}).get("name", ""),
                "url": j.get("absolute_url", ""),
                "department": ", ".join(d.get("name", "") for d in j.get("departments", [])),
            }
        )
    return jobs


# --------------------------------------------------------------------------- #
# Lever -> https://api.lever.co/v0/postings/{slug}?mode=json
# --------------------------------------------------------------------------- #
def lever(slug: str) -> list[dict]:
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
    try:
        data = _get(url).json()
    except (requests.RequestException, ValueError):
        return []
    jobs = []
    for j in data:
        cats = j.get("categories", {}) or {}
        jobs.append(
            {
                "id": f"lever:{slug}:{j.get('id')}",
                "title": (j.get("text") or "").strip(),
                "location": cats.get("location", ""),
                "url": j.get("hostedUrl", ""),
                "department": cats.get("team", "") or cats.get("department", ""),
            }
        )
    return jobs


# --------------------------------------------------------------------------- #
# Ashby -> https://api.ashbyhq.com/posting-api/job-board/{slug}
# --------------------------------------------------------------------------- #
def ashby(slug: str) -> list[dict]:
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=false"
    try:
        data = _get(url).json()
    except (requests.RequestException, ValueError):
        return []
    jobs = []
    for j in data.get("jobs", []):
        jobs.append(
            {
                "id": f"ashby:{slug}:{j.get('id')}",
                "title": (j.get("title") or "").strip(),
                "location": j.get("location", ""),
                "url": j.get("jobUrl", "") or j.get("applyUrl", ""),
                "department": j.get("department", "") or j.get("team", ""),
            }
        )
    return jobs


# --------------------------------------------------------------------------- #
# Recruitee -> https://{slug}.recruitee.com/api/offers/
# --------------------------------------------------------------------------- #
def recruitee(slug: str) -> list[dict]:
    url = f"https://{slug}.recruitee.com/api/offers/"
    try:
        data = _get(url).json()
    except (requests.RequestException, ValueError):
        return []
    jobs = []
    for j in data.get("offers", []):
        jobs.append(
            {
                "id": f"recruitee:{slug}:{j.get('id')}",
                "title": (j.get("title") or "").strip(),
                "location": j.get("location", "") or j.get("city", ""),
                "url": j.get("careers_url", "") or j.get("url", ""),
                "department": j.get("department", ""),
            }
        )
    return jobs


# --------------------------------------------------------------------------- #
# Workable -> https://apply.workable.com/api/v3/accounts/{slug}/jobs
# --------------------------------------------------------------------------- #
def workable(slug: str) -> list[dict]:
    url = f"https://apply.workable.com/api/v3/accounts/{slug}/jobs"
    try:
        # Workable erwartet POST mit leerem Filter-Body
        resp = requests.post(url, json={}, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError):
        return []
    jobs = []
    for j in data.get("results", []):
        loc = j.get("location", {}) or {}
        jobs.append(
            {
                "id": f"workable:{slug}:{j.get('shortcode') or j.get('id')}",
                "title": (j.get("title") or "").strip(),
                "location": ", ".join(
                    filter(None, [loc.get("city", ""), loc.get("country", "")])
                ),
                "url": f"https://apply.workable.com/{slug}/j/{j.get('shortcode')}/"
                if j.get("shortcode")
                else "",
                "department": j.get("department", ""),
            }
        )
    return jobs


# --------------------------------------------------------------------------- #
# JOIN -> https://join.com/api/public/companies/{company_id}/jobs
#   slug = Firmenname aus der URL, z.B. "project-a" (join.com/companies/project-a)
# --------------------------------------------------------------------------- #
def join(slug: str) -> list[dict]:
    try:
        html = _get(f"https://join.com/companies/{slug}").text
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
        company_id = json.loads(m.group(1))["props"]["pageProps"]["initialState"]["company"]["id"]
    except (requests.RequestException, ValueError, KeyError, AttributeError):
        return []

    jobs: list[dict] = []
    page = 1
    while page <= 20:  # Sicherheitslimit
        url = (
            f"https://join.com/api/public/companies/{company_id}/jobs"
            f"?locale=de-de&page={page}&pageSize=5"
        )
        try:
            data = _get(url).json()
        except (requests.RequestException, ValueError):
            break
        for j in data.get("items", []):
            city = j.get("city") or {}
            country = j.get("country") or {}
            city_name = city.get("cityName", "") if isinstance(city, dict) else str(city)
            country_name = country.get("name", "") if isinstance(country, dict) else str(country)
            id_param = j.get("idParam") or j.get("id")
            jobs.append(
                {
                    "id": f"join:{slug}:{j.get('id')}",
                    "title": (j.get("title") or "").strip(),
                    "location": ", ".join(filter(None, [city_name, country_name])),
                    "url": f"https://join.com/companies/{slug}/{id_param}",
                    "department": (j.get("category") or {}).get("name", "")
                    if isinstance(j.get("category"), dict)
                    else "",
                }
            )
        if page >= (data.get("pagination") or {}).get("pageCount", 0):
            break
        page += 1
    return jobs


# --------------------------------------------------------------------------- #
# Getro (Job-Boards von VCs, z.B. jobs.earlybird.com)
#   slug = "<board-host>/<company-slug>", z.B. "jobs.earlybird.com/earlybird-venture-capital"
#   Das Board enthaelt auch Portfolio-Stellen -> wir filtern ueber organization.id
#   auf die Stellen des VCs selbst.
# --------------------------------------------------------------------------- #
def getro(slug: str) -> list[dict]:
    host, _, company_slug = slug.partition("/")
    try:
        html = _get(f"https://{host}/companies/{company_slug}").text
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
        props = json.loads(m.group(1))["props"]["pageProps"]
        collection_id = props["network"]["id"]
        org_id = props["company"]["id"]
    except (requests.RequestException, ValueError, KeyError, AttributeError):
        return []

    api = f"https://api.getro.com/api/v2/collections/{collection_id}/search/jobs"
    jobs: list[dict] = []
    for page in range(20):  # Sicherheitslimit
        body = {"hitsPerPage": 20, "page": page, "query": "", "filters": {"organization.id": [org_id]}}
        try:
            resp = requests.post(
                api, json=body, headers={**HEADERS, "Accept": "application/json"}, timeout=TIMEOUT
            )
            resp.raise_for_status()
            hits = resp.json()["results"]["jobs"]
        except (requests.RequestException, ValueError, KeyError):
            break
        for j in hits:
            # Sicherheitsnetz: nur Stellen der VC-Organisation selbst
            if (j.get("organization") or {}).get("id") not in (None, org_id):
                continue
            jobs.append(
                {
                    "id": f"getro:{host}:{j.get('id') or j.get('url')}",
                    "title": (j.get("title") or "").strip(),
                    "location": ", ".join(j.get("searchable_locations") or []),
                    "url": j.get("url", ""),
                    "department": "",
                }
            )
        if len(hits) < 20:
            break
    return jobs


# --------------------------------------------------------------------------- #
# SmartRecruiters -> https://api.smartrecruiters.com/v1/companies/{company}/postings
#   slug = "<company>" oder "<company>|<Stichwort>". Mit Stichwort werden nur Stellen
#   behalten, deren Titel das Stichwort enthaelt (z.B. "RocketInternet|Global Founders Capital",
#   weil GFC seine Stellen ueber das Rocket-Internet-Konto ausschreibt).
# --------------------------------------------------------------------------- #
def smartrecruiters(slug: str) -> list[dict]:
    company, _, keyword = slug.partition("|")
    jobs: list[dict] = []
    offset = 0
    while offset < 500:  # Sicherheitslimit
        params = {"limit": 100, "offset": offset}
        if keyword:
            params["q"] = keyword
        try:
            data = requests.get(
                f"https://api.smartrecruiters.com/v1/companies/{company}/postings",
                params=params,
                headers=HEADERS,
                timeout=TIMEOUT,
            ).json()
        except (requests.RequestException, ValueError):
            break
        items = data.get("content", [])
        for j in items:
            title = (j.get("name") or "").strip()
            if keyword and keyword.lower() not in title.lower():
                continue
            loc = j.get("location") or {}
            jobs.append(
                {
                    "id": f"smartrecruiters:{company}:{j.get('id')}",
                    "title": title,
                    "location": ", ".join(
                        filter(None, [loc.get("city", ""), (loc.get("country") or "").upper()])
                    ),
                    "url": f"https://jobs.smartrecruiters.com/{company}/{j.get('id')}",
                    "department": "",
                }
            )
        offset += 100
        if len(items) < 100:
            break
    return jobs


# --------------------------------------------------------------------------- #
# Trakstar Hire -> https://{slug}.hire.trakstar.com/  (HTML-Liste)
# --------------------------------------------------------------------------- #
def trakstar(slug: str) -> list[dict]:
    base = f"https://{slug}.hire.trakstar.com"
    try:
        html = _get(base + "/").text
    except requests.RequestException:
        return []
    jobs: list[dict] = []
    for card in html.split('data-href="')[1:]:
        path = card.split('"', 1)[0]
        title = re.search(r'js-job-list-opening-name[^>]*title="([^"]*)"', card)
        loc = re.search(r'js-job-list-opening-loc[^>]*title="([^"]*)"', card)
        if not title or not path.startswith("/jobs/"):
            continue
        jobs.append(
            {
                "id": f"trakstar:{slug}:{path.strip('/').split('/')[-1]}",
                "title": html_unescape(title.group(1)).strip(),
                "location": html_unescape(loc.group(1)).strip() if loc else "",
                "url": base + path,
                "department": "",
            }
        )
    return jobs


# --------------------------------------------------------------------------- #
# Breezy HR -> https://{slug}.breezy.hr/json
# --------------------------------------------------------------------------- #
def breezy(slug: str) -> list[dict]:
    try:
        data = _get(f"https://{slug}.breezy.hr/json").json()
    except (requests.RequestException, ValueError):
        return []
    jobs = []
    for j in data if isinstance(data, list) else []:
        loc = j.get("location") or {}
        jobs.append(
            {
                "id": f"breezy:{slug}:{j.get('id')}",
                "title": (j.get("name") or "").strip(),
                "location": loc.get("name", "") if isinstance(loc, dict) else str(loc),
                "url": j.get("url", ""),
                "department": j.get("department", "") if isinstance(j.get("department"), str) else "",
            }
        )
    return jobs


# --------------------------------------------------------------------------- #
# Karriereseite (generisch) -> beliebige statische HTML-Karriereseite eines VCs
#   slug = URL der Karriereseite. Best effort: Es werden Links gesucht, die wie eine
#   Stellenanzeige aussehen (Titel mit Einstiegs-Stichwort UND Stellen-Merkmal wie
#   "(m/w/d)" oder ein Job-Pfad). Ort: erste deutsche Stadt im Link-Text bzw. auf der Seite.
# --------------------------------------------------------------------------- #
_ENTRY = re.compile(
    r"(?<![a-zäöüß])(praktik\w*|intern(?:ship)?s?|werkstudent\w*|working student|analyst\w*|"
    r"associate|trainee|junior|absolvent\w*|graduate|fellow\w*|visiting)(?![a-zäöüß])",
    re.I,
)
_GENDER = re.compile(r"\((?:\s*[mwfdxgn]\s*[/|*:]\s*){1,3}[mwfdxgn]\s*\)|all genders|\(gn\)|\(m/w/\*\)", re.I)
_JOBPATH = re.compile(r"/(jobs?|stelle[n]?|position[s]?|opening[s]?|vacanc\w*|karriere|careers?|apply|bewerb\w*)(/|$|\?|-)", re.I)
_STOP_TITLES = {"analyst", "analysts", "analysten", "praktikum", "internship", "internships", "intern",
                "interns", "associate", "associates", "graduate", "junior", "trainee"}
_CITIES = ["berlin", "münchen", "munich", "hamburg", "frankfurt", "köln", "cologne", "düsseldorf",
           "stuttgart", "bonn", "leipzig", "hannover", "karlsruhe", "heidelberg", "mannheim", "nürnberg",
           "dresden", "potsdam", "heilbronn"]


class _AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.anchors: list[tuple[str, str]] = []
        self.text: list[str] = []
        self._cur: list[str] | None = None
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._skip += 1
        if tag == "a":
            self._cur = [dict(attrs).get("href") or "", ""]

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self._skip = max(0, self._skip - 1)
        if tag == "a" and self._cur is not None:
            self.anchors.append((self._cur[0], self._cur[1]))
            self._cur = None

    def handle_data(self, data):
        if self._skip:
            return
        self.text.append(data)
        if self._cur is not None:
            self._cur[1] += data


def _clean_title(t: str) -> str:
    t = " ".join(html_unescape(t).split())
    t = re.sub(r"^\d{1,2}\s*/\s*\d{1,2}\s*/\s*\d{2,4}\s*", "", t)          # Datum am Anfang
    t = re.sub(r"^(job opening|open position|stellenanzeige|new)\s*[:\-–]?\s*", "", t, flags=re.I)
    return t.strip(" -–|")


def careerpage(slug: str) -> list[dict]:
    """slug = "<URL>" oder "<URL>|<Ort>". Der Ort dient als Fallback, wenn Titel/Seite keine
    deutsche Stadt nennen (fuer VCs, die bekanntermassen in Deutschland sitzen)."""
    from urllib.parse import urljoin, urlparse

    slug, _, default_loc = slug.partition("|")
    resp = None
    for _ in range(2):
        try:
            resp = _get(slug)
            break
        except requests.RequestException:
            continue
    if resp is None or "html" not in resp.headers.get("content-type", "html").lower():
        return []
    parser = _AnchorParser()
    try:
        parser.feed(resp.text)
    except Exception:
        return []
    page_text = " ".join(" ".join(parser.text).split()).lower()
    page_city = next((c for c in _CITIES if re.search(rf"(?<![a-zäöü]){c}(?![a-zäöü])", page_text)), "")
    page_path = urlparse(resp.url).path.rstrip("/")
    page_city = page_city.title() if page_city else default_loc

    jobs: dict[str, dict] = {}
    for href, raw in parser.anchors:
        title = _clean_title(raw)
        if not (8 <= len(title) <= 140) or not _ENTRY.search(title):
            continue
        if title.lower() in _STOP_TITLES or len(title.split()) < 2:
            continue
        if re.match(r"^(studenten|schüler|absolventen|students)\b", title, re.I):
            continue  # Kategorie-Links wie "Studenten & Absolventen", keine Stellen
        target = urljoin(resp.url, href)
        path = urlparse(target).path.rstrip("/")
        jobby = bool(_GENDER.search(title)) or (
            bool(_JOBPATH.search(path)) and path != page_path and len(path) > len(page_path)
        )
        if not jobby or href.startswith(("mailto:", "tel:", "#", "javascript:")):
            continue
        city = next((c.title() for c in _CITIES if c in title.lower()), page_city)
        job_id = "careerpage:" + hashlib.md5(f"{target}|{title}".encode()).hexdigest()[:12]
        jobs[job_id] = {
            "id": job_id,
            "title": title,
            "location": city,
            "url": target,
            "department": "",
        }
    # Zweiter Durchgang: Manche Seiten (z.B. Wix) legen Stellen als JSON-Daten im HTML ab statt als
    # Links. Gesucht werden Objekte mit "title" (+ optional "location"/"url") und Geschlechtsmarker.
    raw = resp.text.replace("\\/", "/")
    for m in re.finditer(r'"title":"([^"]{6,160})"', raw):
        title = _clean_title(m.group(1).replace("\\n", " ").replace("\\u0026", "&"))
        if not (8 <= len(title) <= 140) or not _ENTRY.search(title) or not _GENDER.search(title):
            continue
        if len(title.split()) < 2:
            continue
        seg = raw[max(0, m.start() - 900): m.end() + 200]
        loc = re.findall(r'"location":"([^"]*)"', seg)
        url = re.findall(r'"url":"(https?://[^"]*)"', seg)
        target = url[-1] if url else resp.url
        if title.islower():
            title = " ".join(w if w.startswith("(") else w.capitalize() for w in title.split())
        location = loc[-1].title() if loc and loc[-1] else page_city
        job_id = "careerpage:" + hashlib.md5(f"{target}|{title}".encode()).hexdigest()[:12]
        jobs.setdefault(
            job_id,
            {"id": job_id, "title": title, "location": location, "url": target, "department": ""},
        )
    return list(jobs.values())


# Registry: ATS-Name -> Adapter-Funktion
ADAPTERS: dict[str, Callable[[str], list[dict]]] = {
    "personio": personio,
    "greenhouse": greenhouse,
    "lever": lever,
    "ashby": ashby,
    "recruitee": recruitee,
    "workable": workable,
    "join": join,
    "getro": getro,
    "smartrecruiters": smartrecruiters,
    "trakstar": trakstar,
    "breezy": breezy,
    "careerpage": careerpage,
}


def fetch_jobs(ats: str, slug: str) -> list[dict]:
    """Ruft den passenden Adapter auf. Unbekanntes ATS -> []."""
    adapter = ADAPTERS.get(ats)
    if adapter is None:
        return []
    return adapter(slug)
