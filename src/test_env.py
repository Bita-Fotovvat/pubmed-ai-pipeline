import sys
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

print("Python executable:", sys.executable)
print("DATABASE_URL:", os.getenv("DATABASE_URL"))

conn = psycopg2.connect(
    dbname="pubmed_ai",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5433"
)


print("✅ Connected to PostgreSQL successfully!")
conn.close()
