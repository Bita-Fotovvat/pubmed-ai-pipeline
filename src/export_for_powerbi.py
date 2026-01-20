import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

EXPORTS = [
    ("SELECT * FROM vw_articles_enriched;", "exports/articles_enriched.csv"),
    ("SELECT * FROM vw_category_counts;", "exports/category_counts.csv"),
    ("SELECT * FROM vw_top_keywords;", "exports/top_keywords.csv"),
    ("SELECT * FROM vw_recent_high_relevance;", "exports/recent_high_relevance.csv"),
    ("SELECT * FROM vw_pubs_by_year;", "exports/pubs_by_year.csv"),
    ("SELECT * FROM vw_category_over_time;", "exports/category_over_time.csv"),
]

def main():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set (check your .env file)")

    os.makedirs("exports", exist_ok=True)
    engine = create_engine(DATABASE_URL)

    for sql, path in EXPORTS:
        df = pd.read_sql(sql, engine)
        df.to_csv(path, index=False, encoding="utf-8")
        print(f"✅ Wrote {path} ({len(df)} rows)")

if __name__ == "__main__":
    main()
