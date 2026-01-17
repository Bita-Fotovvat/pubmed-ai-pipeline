import requests
from typing import Dict, List
import xml.etree.ElementTree as ET

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def fetch_abstracts(pmids: List[int], email: str = "example@example.com") -> Dict[int, str]:
    """
    Fetch abstracts for a list of PMIDs using efetch (XML).
    Returns {pmid: abstract_text}.
    """
    if not pmids:
        return {}

    url = f"{BASE}/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(str(p) for p in pmids),
        "retmode": "xml",
        "tool": "pubmed-ai-pipeline",
        "email": email,
    }

    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()

    root = ET.fromstring(r.text)
    abstracts = {}

    # Walk through PubmedArticle nodes
    for article in root.findall(".//PubmedArticle"):
        pmid_el = article.find(".//PMID")
        if pmid_el is None:
            continue
        pmid = int(pmid_el.text)

        # AbstractText can appear multiple times (labeled sections)
        abstract_parts = []
        for abs_el in article.findall(".//Abstract/AbstractText"):
            label = abs_el.attrib.get("Label")
            txt = (abs_el.text or "").strip()
            if not txt:
                continue
            if label:
                abstract_parts.append(f"{label}: {txt}")
            else:
                abstract_parts.append(txt)

        abstracts[pmid] = "\n".join(abstract_parts).strip()

    return abstracts
