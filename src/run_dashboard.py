import argparse
import os
import subprocess
import sys


def run(cmd: list[str]):
    print("\n▶", " ".join(cmd))
    subprocess.check_call(cmd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="PubMed query string")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite old results (reset DB + overwrite exports)"
    )
    args = parser.parse_args()

    # 0) Save query into env var for the step that fetches PubMed
    os.environ["PUBMED_QUERY"] = args.query

    # 1) Wait for Postgres to be ready  ✅ NEW (must be first DB-related step)
    run([sys.executable, "src/wait_for_db.py"])

    # 2) Overwrite reset
    if args.overwrite:
        run([sys.executable, "src/reset_db.py"])

    # 3) Fetch PubMed -> data/pubmed_results.json
    run([sys.executable, "src/step3_fetch_pubmed.py"])

    # 4) Fetch abstracts
    run([sys.executable, "src/pubmed_fetch_abstracts.py"])

    # 5) Load JSON into Postgres
    run([sys.executable, "src/load_pubmed_json_to_db.py"])

    # 6) Enrich with OpenAI
    run([sys.executable, "src/enrich_articles_openai.py"])

    # 7) Create/refresh views
    run([sys.executable, "src/create_views.py"])

    # 8) Export CSVs for Power BI
    run([sys.executable, "src/export_for_powerbi.py"])

    print("\n🎉 Done. Now open Power BI and press Refresh.")


if __name__ == "__main__":
    main()
