import json
from pathlib import Path
from pubmed_client import esearch, esummary


def main():
    # Change this query to your research topic any time
    # gut microbiota AND anxiety
    query = '("gut microbiota" AND (anxiety)) AND ("2015"[dp] : "3000"[dp])'


    # 1) Get PMIDs
    pmids = esearch(query=query, retmax=20)
    print(f"Found {len(pmids)} PMIDs")

    # 2) Get summary metadata
    articles = esummary(pmids)
    print(f"Fetched {len(articles)} article summaries")

    # 3) Save output
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)

    out_path = out_dir / "pubmed_results.json"
    out_path.write_text(json.dumps(articles, indent=2), encoding="utf-8")

    print(f"Saved results to: {out_path.resolve()}")

    # 4) Print first 3 (quick check)
    for a in articles[:3]:
        print("-" * 60)
        print("PMID:", a["pmid"])
        print("Title:", a["title"])
        print("Journal:", a["journal"])
        print("Date:", a["pubdate"])
        print("Authors:", ", ".join(a["authors"][:5]))


if __name__ == "__main__":
    main()
