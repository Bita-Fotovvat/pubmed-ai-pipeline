-- Raw-ish table for PubMed summary metadata (from ESummary)
CREATE TABLE IF NOT EXISTS pubmed_articles (
  pmid        BIGINT PRIMARY KEY,
  title       TEXT,
  journal     TEXT,
  pubdate     TEXT,
  authors     JSONB,
  fetched_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS article_enrichment (
  pmid            BIGINT PRIMARY KEY REFERENCES pubmed_articles(pmid) ON DELETE CASCADE,
  summary         TEXT,
  keywords        JSONB,
  topic_category  TEXT,
  relevance_score INTEGER,
  model_name      TEXT,
  prompt_version  TEXT,
  processed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
