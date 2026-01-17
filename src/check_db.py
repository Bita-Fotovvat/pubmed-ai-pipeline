from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def main():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM pubmed_articles;")).scalar()
        print("Rows in pubmed_articles:", count)

        rows = conn.execute(text("""
            SELECT pmid, pubdate, left(title, 80) AS title
            FROM pubmed_articles
            ORDER BY pmid DESC
            LIMIT 5;
        """)).fetchall()

        print("\nTop 5 rows:")
        for r in rows:
            print(r)

if __name__ == "__main__":
    main()
