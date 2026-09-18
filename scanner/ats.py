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

import json
import re
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
}


def fetch_jobs(ats: str, slug: str) -> list[dict]:
    """Ruft den passenden Adapter auf. Unbekanntes ATS -> []."""
    adapter = ADAPTERS.get(ats)
    if adapter is None:
        return []
    return adapter(slug)
