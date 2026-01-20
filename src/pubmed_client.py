import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def esearch(query: str, retmax: int = 20) -> List[str]:
    """
    Search PubMed and return a list of PMIDs.
    If PubMed returns an unexpected response, print debug info.
    """
    url = f"{BASE}/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax,
        # good practice (optional but recommended)
        "tool": "pubmed-ai-pipeline",
        "email": "fotovvab@mcmaster.ca",
    }

    r = requests.get(url, params=params, timeout=30)

    # If PubMed returns HTML or a non-JSON error, this helps us see it:
    try:
        data = r.json()
    except Exception:
        print("❌ PubMed did not return JSON.")
        print("Status:", r.status_code)
        print("First 300 chars of response:\n", r.text[:300])
        raise

    # Debug if expected keys are missing
    if "esearchresult" not in data:
        print("❌ Missing 'esearchresult' in response.")
        print("Status:", r.status_code)
        print("Response JSON keys:", list(data.keys()))
        print("Full response JSON:", data)
        raise KeyError("esearchresult missing")

    es = data["esearchresult"]

    # PubMed sometimes returns errorlist/warnings
    if "errorlist" in es:
        print("⚠️ PubMed errorlist:", es["errorlist"])
    if "warninglist" in es:
        print("⚠️ PubMed warninglist:", es["warninglist"])

    pmids = es.get("idlist", [])
    if not isinstance(pmids, list):
        print("❌ 'idlist' exists but is not a list:", pmids)
        raise TypeError("idlist is not a list")

    return pmids


def esummary(pmids: List[str]) -> List[Dict[str, Any]]:
    if not pmids:
        return []

    url = f"{BASE}/esummary.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "json",
        "tool": "pubmed-ai-pipeline",
        "email": "example@example.com",
    }

    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()

    result = data.get("result", {})
    uids = result.get("uids", [])

    articles = []
    for uid in uids:
        item = result.get(uid, {})
        articles.append({
            "pmid": uid,
            "title": item.get("title"),
            "journal": item.get("fulljournalname"),
            "pubdate": item.get("pubdate"),
            "authors": [a.get("name") for a in item.get("authors", [])],
        })
    return articles
