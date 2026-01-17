from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def main():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM article_enrichment;")).scalar()
        print("Rows in article_enrichment:", count)

        rows = conn.execute(text("""
            SELECT e.pmid, e.topic_category, e.relevance_score, left(e.summary, 90)
            FROM article_enrichment e
            ORDER BY e.relevance_score DESC
            LIMIT 5;
        """)).fetchall()

        print("\nTop 5 enriched:")
        for r in rows:
            print(r)

if __name__ == "__main__":
    main()
