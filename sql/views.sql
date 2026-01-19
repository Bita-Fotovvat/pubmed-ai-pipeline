-- 1) Main view Power BI will use
CREATE OR REPLACE VIEW vw_articles_enriched AS
SELECT
  a.pmid,
  a.title,
  a.journal,
  a.pubdate,
  a.fetched_at,
  e.topic_category,
  e.relevance_score,
  e.summary,
  e.keywords,
  e.model_name,
  e.prompt_version,
  e.processed_at
FROM pubmed_articles a
JOIN article_enrichment e ON e.pmid = a.pmid;

-- 2) Counts by category
CREATE OR REPLACE VIEW vw_category_counts AS
SELECT
  topic_category,
  COUNT(*) AS paper_count,
  AVG(relevance_score) AS avg_relevance
FROM vw_articles_enriched
GROUP BY topic_category
ORDER BY paper_count DESC;

-- 3) Keyword frequency (top keywords)
CREATE OR REPLACE VIEW vw_top_keywords AS
SELECT
  lower(trim(k.value::text, '"')) AS keyword,
  COUNT(*) AS keyword_count
FROM vw_articles_enriched v,
LATERAL jsonb_array_elements(v.keywords) AS k(value)
GROUP BY lower(trim(k.value::text, '"'))
ORDER BY keyword_count DESC;

-- 4) Recent + high relevance
CREATE OR REPLACE VIEW vw_recent_high_relevance AS
SELECT *
FROM vw_articles_enriched
WHERE relevance_score >= 70
ORDER BY processed_at DESC;
