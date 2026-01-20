import os
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError


def main(timeout_seconds: int = 40, interval_seconds: float = 1.5) -> None:
    """
    Wait until Postgres is ready to accept connections.

    This is required when Postgres runs in Docker and Python runs locally.
    """
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set (check your .env file).")

    engine = create_engine(database_url)

    print("⏳ Waiting for Postgres to be ready...")

    start_time = time.time()
    last_error = None

    while (time.time() - start_time) < timeout_seconds:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1;"))
            print("✅ Postgres is ready.")
            return
        except OperationalError as e:
            last_error = e
            time.sleep(interval_seconds)

    raise RuntimeError(
        f"❌ Postgres did not become ready within {timeout_seconds} seconds.\n"
        f"Last error: {last_error}"
    )


if __name__ == "__main__":
    main()
