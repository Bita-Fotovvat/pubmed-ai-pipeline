import json
import os
from typing import Dict, Any, List

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from openai import OpenAI

from pubmed_fetch_abstracts import fetch_abstracts

# Load .env variables (DATABASE_URL, OPENAI_API_KEY)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in .env")

client = OpenAI(api_key=OPENAI_API_KEY)

PROMPT_VERSION = "v1"
MODEL_NAME = "gpt-4o-mini"  # cost-effective for summarization/classification

# Put your real email here (PubMed likes this for API usage)
PUBMED_EMAIL = "fotovvab@mcmaster.ca"


def build_prompt(title: str, abstract: str) -> str:
    return f"""
You are helping analyze scientific papers for a literature review.

Return ONLY JSON. No markdown. No extra text.

Return a JSON object with these keys:
- summary: string (2-3 sentences)
- keywords: array of 5-10 short strings
- topic_category: one of ["salt crystallization","masonry materials","finite element / modelling","durability / degradation","other"]
- relevance_score: integer 0-100 (how relevant to salt crystallization in porous masonry)

Title: {title}

Abstract:
{abstract}
""".strip()


def get_articles_to_enrich(conn, limit: int = 20) -> List[Dict[str, Any]]:
    rows = conn.execute(text("""
        SELECT a.pmid, a.title
        FROM pubmed_articles a
        LEFT JOIN article_enrichment e ON e.pmid = a.pmid
        WHERE e.pmid IS NULL
        ORDER BY a.pmid DESC
        LIMIT :limit
    """), {"limit": limit}).fetchall()

    return [{"pmid": int(r[0]), "title": r[1] or ""} for r in rows]


def call_openai(title: str, abstract: str) -> Dict[str, Any]:
    prompt = build_prompt(title, abstract)

    # ✅ Correct way to force JSON output in the Responses API:
    resp = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
        text={"format": {"type": "json_object"}},
    )

    output_text = (resp.output_text or "").strip()
    if not output_text:
        # show minimal debug if OpenAI returns empty content
        raise ValueError("Empty output_text from OpenAI. Check your API key, model, or rate limits.")

    # Parse the JSON
    try:
        return json.loads(output_text)
    except json.JSONDecodeError as e:
        print("❌ OpenAI returned something that is not valid JSON. First 300 chars:")
        print(output_text[:300])
        raise e


def main():
    engine = create_engine(DATABASE_URL)

    with engine.begin() as conn:
        items = get_articles_to_enrich(conn, limit=20)
        if not items:
            print("✅ No new articles to enrich.")
            return

        pmids = [it["pmid"] for it in items]

        # Fetch abstracts from PubMed using efetch
        abstracts = fetch_abstracts(pmids, email=PUBMED_EMAIL)

        insert_sql = text("""
            INSERT INTO article_enrichment
              (pmid, summary, keywords, topic_category, relevance_score, model_name, prompt_version)
            VALUES
              (:pmid, :summary, CAST(:keywords AS jsonb), :topic_category, :relevance_score, :model_name, :prompt_version)
            ON CONFLICT (pmid) DO UPDATE SET
              summary = EXCLUDED.summary,
              keywords = EXCLUDED.keywords,
              topic_category = EXCLUDED.topic_category,
              relevance_score = EXCLUDED.relevance_score,
              model_name = EXCLUDED.model_name,
              prompt_version = EXCLUDED.prompt_version,
              processed_at = NOW();
        """)

        for it in items:
            pmid = it["pmid"]
            title = it["title"]
            abstract = abstracts.get(pmid, "")

            if not abstract:
                print(f"⚠️ PMID {pmid}: no abstract found; skipping.")
                continue

            try:
                result = call_openai(title, abstract)
            except Exception as e:
                print(f"❌ PMID {pmid} OpenAI/JSON error: {repr(e)}")
                continue

            # Safe defaults
            summary = result.get("summary", "")
            keywords = result.get("keywords", [])
            topic_category = result.get("topic_category", "other")
            relevance_score = result.get("relevance_score", 0)

            # Clean relevance_score to int
            try:
                relevance_score = int(relevance_score)
            except Exception:
                relevance_score = 0

            conn.execute(insert_sql, {
                "pmid": pmid,
                "summary": summary,
                "keywords": json.dumps(keywords),
                "topic_category": topic_category,
                "relevance_score": relevance_score,
                "model_name": MODEL_NAME,
                "prompt_version": PROMPT_VERSION,
            })

            print(f"✅ Enriched PMID {pmid} | category={topic_category} | score={relevance_score}")

    print("✅ Done enriching.")


if __name__ == "__main__":
    main()
