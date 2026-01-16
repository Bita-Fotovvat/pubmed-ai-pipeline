# PubMed → OpenAI → PostgreSQL → Power BI Pipeline

This project ingests PubMed articles, stores raw metadata in PostgreSQL, enriches records using the OpenAI API, stores enriched results back in PostgreSQL, and visualizes insights in Power BI.

## Architecture
PubMed API → Python ETL → PostgreSQL (raw) → OpenAI enrichment → PostgreSQL (enriched) → Power BI

## Project Structure
- src/: Python code (ETL + enrichment)
- sql/: Database schema + views
- docs/: diagrams + notes
- powerbi/: Power BI files / screenshots

## Setup (high level)
1. Start PostgreSQL (Docker)
2. Initialize DB schema
3. Run ingestion script
4. Run enrichment script
5. Connect Power BI to PostgreSQL views
