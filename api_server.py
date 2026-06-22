from fastapi import FastAPI, HTTPException
from pathlib import Path
import pandas as pd
from typing import Dict, Any

app = FastAPI(
    title="AI Policy Dashboard API",
    description="API endpoints for policy analytics, sentiment, and dashboard health",
    version="1.0.0"
)

data_dir = Path(__file__).parent / "data"


def load_csv(filename: str) -> pd.DataFrame:
    path = data_dir / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Data file not found: {filename}")
    return pd.read_csv(path)


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "message": "AI Policy Dashboard API is running"}


@app.get("/summary")
def summary() -> Dict[str, Any]:
    result = {"available_files": []}
    for filename in ["processed_documents.csv", "processed_opinions.csv", "merged_policy_data.csv", "topics.csv", "keywords.csv"]:
        file_path = data_dir / filename
        result["available_files"].append({
            "filename": filename,
            "exists": file_path.exists(),
            "size_bytes": file_path.stat().st_size if file_path.exists() else 0
        })
    if (data_dir / "processed_documents.csv").exists():
        df = load_csv("processed_documents.csv")
        result.update({
            "document_count": len(df),
            "authority_count": int(df["Authority"].nunique()) if "Authority" in df.columns else 0,
            "sample_document": df["Official name"].iloc[0] if "Official name" in df.columns and len(df) > 0 else None,
        })
    if (data_dir / "processed_opinions.csv").exists():
        opinions = load_csv("processed_opinions.csv")
        result.update({
            "opinion_count": len(opinions),
            "sample_opinion": opinions["full_text"].iloc[0] if "full_text" in opinions.columns and len(opinions) > 0 else None,
        })
    return result


@app.get("/policies")
def policies(limit: int = 20) -> Dict[str, Any]:
    df = load_csv("merged_policy_data.csv")
    display_cols = [col for col in ["Official name", "Authority", "Short summary", "Proposed date"] if col in df.columns]
    records = df[display_cols].head(limit).to_dict(orient="records")
    return {"count": len(records), "policies": records}


@app.get("/opinions")
def opinions(limit: int = 20) -> Dict[str, Any]:
    df = load_csv("processed_opinions.csv")
    display_cols = [col for col in ["full_text", "source_url", "source_handle"] if col in df.columns]
    records = df[display_cols].head(limit).to_dict(orient="records")
    return {"count": len(records), "opinions": records}


@app.get("/topics")
def topics() -> Dict[str, Any]:
    df = load_csv("topics.csv")
    topics_list = df.to_dict(orient="records")
    return {"count": len(topics_list), "topics": topics_list}
