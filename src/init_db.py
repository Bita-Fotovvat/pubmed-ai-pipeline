from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Put it in your .env file.")

def main():
    engine = create_engine(DATABASE_URL)

    schema_path = Path("sql/schema.sql")
    sql = schema_path.read_text(encoding="utf-8")

    with engine.begin() as conn:
        conn.execute(text(sql))

    print("✅ Database schema created/verified successfully.")

if __name__ == "__main__":
    main()
