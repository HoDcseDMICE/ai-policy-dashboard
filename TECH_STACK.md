# Technical Stack for AI Policy Dashboard

This document lists the recommended technical stack for building, deploying, and reporting the AI Policy Dashboard.

## Layered Stack

- **Data Collection**
  - Python: Scrapy, BeautifulSoup
  - Selenium for dynamic scraping / browser automation
  - REST APIs / OAuth-secured endpoints

- **Storage**
  - Relational / transactional: PostgreSQL
  - Document / flexible storage: MongoDB
  - Object storage for raw/full-text documents: AWS S3 (or Azure Blob Storage)

- **Processing & NLP**
  - Dataframes and numeric processing: Pandas, NumPy
  - NLP libraries: spaCy, NLTK, TextBlob, VADER
  - Topic modeling: Gensim (LDA), BERTopic (optional)
  - Embeddings / transformers: sentence-transformers
  - Machine learning: Scikit-learn (clustering, regression, classification)

- **Visualization**
  - Interactive charts: Plotly
  - BI tools (optional): Power BI, Tableau
  - Word clouds / static visuals: Matplotlib, Seaborn, WordCloud

- **Dashboard / Frontend**
  - Streamlit (primary) or Plotly Dash
  - Optional full-stack: Flask (API) + React (frontend)

- **Deployment & DevOps**
  - Containerization: Docker
  - CI/CD: GitHub Actions (or Azure Pipelines)
  - Cloud hosting: AWS (EC2, ECS, EKS, S3, RDS) or Azure (App Service, AKS, Blob, Postgres)
  - Secrets & config: AWS Secrets Manager / Azure Key Vault / environment variables

- **Reporting & Notebooks**
  - Interactive analysis: Jupyter / JupyterLab
  - Automated export: WeasyPrint or Pandoc for PDF/printable exports
  - Reproducible notebooks: nbformat / papermill for scheduled runs

- **Monitoring & Observability**
  - App logs: structured logging to stdout, CloudWatch/Log Analytics
  - Metrics: Prometheus + Grafana (or cloud-native monitoring)

- **Security & Governance**
  - HTTPS, auth (OIDC/OAuth2), RBAC for dashboards
  - Data retention & PII handling policies

## Quick Local Development Requirements

- Python 3.9+ environment (venv or conda)
- Example essential packages (add to `requirements.txt`):
  - streamlit, pandas, numpy, scikit-learn, spacy, nltk, gensim, plotly, sentence-transformers

## Recommended Architecture Pattern

1. Ingest: Scrapers / API collectors push raw documents to S3 and metadata into Postgres/Mongo.
2. Preprocess: Batch jobs (Airflow / cron / script) run NLP pipelines, persist processed CSV/Parquet and model artifacts into `data/` and `models/`.
3. API: Lightweight FastAPI/Flask service to expose processed datasets and model endpoints.
4. Dashboard: Streamlit app for analyst-facing UI; optional React + Flask for advanced UX.
5. CI/CD: Build Docker images, run tests, push to registry, and deploy via GitHub Actions to cloud.

## Notes

- BERTopic and some transformer-based tooling require additional native dependencies and GPU support for heavy workloads; include optional install instructions in `DEPLOYMENT.md`.
- For reproducible ML experiments, pin package versions and store model artifacts with checksums.

---

Created to standardize the stack for building, deploying, and extending the AI Policy Dashboard.
