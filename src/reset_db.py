from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set")

engine = create_engine(DATABASE_URL)

with engine.begin() as conn:
    conn.execute(text("TRUNCATE article_enrichment CASCADE;"))
    conn.execute(text("TRUNCATE pubmed_articles CASCADE;"))

print("✅ Database cleared successfully.")
