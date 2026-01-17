-- Raw-ish table for PubMed summary metadata (from ESummary)
CREATE TABLE IF NOT EXISTS pubmed_articles (
  pmid        BIGINT PRIMARY KEY,
  title       TEXT,
  journal     TEXT,
  pubdate     TEXT,
  authors     JSONB,
  fetched_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
