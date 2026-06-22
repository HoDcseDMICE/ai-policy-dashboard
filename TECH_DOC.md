# Technical Documentation (ETL, Visualization, Scoring)

This document summarizes the ETL process, visualization components, and scoring logic used by the AI Policy Dashboard.

## ETL Pipeline

1. Raw ingestion
   - Data sources: AGORA CSVs, scraped documents, API feeds
   - Store raw full-text documents in object storage (S3) and metadata in Postgres/MongoDB

2. Preprocessing (`preprocess_data.py`)
   - Load AGORA files: `documents.csv`, `segments.csv`, `authorities.csv`
   - Clean text (lowercase, remove excess whitespace, basic punctuation removal)
   - Enrich metadata: word counts, document length, primary domain mapping
   - Export processed artifacts to `dashboard_project/data/` as CSV

3. NLP processing (`src/nlp_analyzer.py`, `src/dashboard_models.py`)
   - Sentiment: ensemble of VADER + TextBlob (fallback heuristic) mapped to labels
   - Topic modeling: LDA (Gensim/sklearn) for fast reproducible topics; optional BERTopic for embedding-based topics
   - Keyword extraction: TF-IDF n-grams with semantic filtering
   - Clustering: TF-IDF + KMeans for document grouping

## Visualization & Dashboard

- Implemented in `app.py` using Streamlit and Plotly for interactive charts.
- Pages include: Home, Policy Analytics, Sentiment Analysis, Topic Modeling, Trends, Analytics, Search, Reports.
- Export endpoints: CSV downloads for filtered datasets and text report generation.

## Scoring Logic

- Policy Maturity Score (simplified): weighted sum of features
  - Document completeness (0-1)
  - Recent activity (recency boost)
  - Coverage across policy domains
  - Authority publication frequency

- Regulatory Intensity: per-domain counts normalized by total documents

- Sentiment mapping: polarity thresholds map to Enabling / Neutral / Restrictive

## Deployment

- Containerize with `Dockerfile`; orchestrate with `docker-compose.yml`.
- CI: GitHub Actions workflows to run tests and build images.
- Recommend cloud components: RDS (Postgres), S3 for storage, ECS/EKS or App Service for hosting.

## Reproducibility & Model Artifacts

- Store model artifacts in `models/` with versioned filenames.
- Pin dependency versions in `requirements.txt`.

## Runbook (local)

```powershell
cd dashboard_project
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python preprocess_data.py
streamlit run app.py --server.address=127.0.0.1 --server.port=8501
```

## Contact

For questions about scoring parameters or dataset curation, contact the project lead.
