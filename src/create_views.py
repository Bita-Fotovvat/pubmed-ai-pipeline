from pathlib import Path
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")

def main():
    engine = create_engine(DATABASE_URL)
    sql = Path("sql/views.sql").read_text(encoding="utf-8")
    with engine.begin() as conn:
        conn.execute(text(sql))
    print("✅ Views created/updated successfully.")

if __name__ == "__main__":
    main()
