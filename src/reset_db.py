import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def main():
    load_dotenv()  # <-- loads .env from project root

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set (check your .env file)")

    engine = create_engine(database_url)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE pubmed_articles CASCADE;"))

    print("✅ Database reset complete (TRUNCATE pubmed_articles CASCADE).")

if __name__ == "__main__":
    main()
