import json
from pathlib import Path
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Put it in your .env file.")

def main():
    json_path = Path("data/pubmed_results.json")
    if not json_path.exists():
        raise FileNotFoundError("data/pubmed_results.json not found. Run Step 3 first.")

    articles = json.loads(json_path.read_text(encoding="utf-8"))
    print(f"Loaded {len(articles)} articles from JSON.")

    engine = create_engine(DATABASE_URL)

    upsert_sql = text("""
        INSERT INTO pubmed_articles (pmid, title, journal, pubdate, authors)
        VALUES (:pmid, :title, :journal, :pubdate, CAST(:authors AS jsonb))
        ON CONFLICT (pmid) DO UPDATE SET
          title = EXCLUDED.title,
          journal = EXCLUDED.journal,
          pubdate = EXCLUDED.pubdate,
          authors = EXCLUDED.authors,
          fetched_at = NOW();
    """)

    with engine.begin() as conn:
        for a in articles:
            conn.execute(
                upsert_sql,
                {
                    "pmid": int(a["pmid"]),
                    "title": a.get("title"),
                    "journal": a.get("journal"),
                    "pubdate": a.get("pubdate"),
                    "authors": json.dumps(a.get("authors", [])),
                }
            )

    print("✅ Inserted/updated articles in Postgres successfully.")

if __name__ == "__main__":
    main()
