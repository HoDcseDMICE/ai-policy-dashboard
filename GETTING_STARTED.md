# 🤖 AI Policy Trends Dashboard - Complete Setup Guide

Welcome! This comprehensive guide will help you get the entire dashboard up and running.

## 📋 What You Have

A complete, production-ready AI policy dashboard with:

✅ **Data Processing Pipeline**
- Loads from multiple AI policy datasets (AGORA, generative AI opinions, etc.)
- Cleans and validates 1000+ policy documents
- Enriches with metadata

✅ **Machine Learning Components**
- Topic modeling (LDA analysis)
- Sentiment analysis (Positive/Negative/Neutral)
- Policy domain detection
- Keyword extraction
- Document clustering
- Policy maturity scoring

✅ **Interactive Dashboard** (7 Pages)
1. **Home** - Overview and data loading
2. **Policy Analytics** - Document exploration with filters
3. **Sentiment Analysis** - Public opinion visualization
4. **Topic Modeling** - Key themes extraction
5. **Trends & Forecasting** - Regulatory patterns
6. **Search & Explore** - Full-text search
7. **Reports** - Custom report generation

✅ **Deployment Ready**
- Docker container configuration
- Streamlit Cloud compatible
- AWS/Azure deployment guides included
- Production-grade security practices

---

## 🚀 Getting Started (Choose Your Path)

### Path 1: Local Development (Recommended First)

Perfect for testing and customization.

**Windows:**
```bash
cd dashboard_project
setup.bat
```

**Mac/Linux:**
```bash
cd dashboard_project
chmod +x setup.sh
./setup.sh
```

Both scripts will:
1. Create Python virtual environment
2. Install all dependencies (pandas, streamlit, plotly, sklearn, etc.)
3. Download NLP models (NLTK data)
4. Run data preprocessing
5. Show you how to start the dashboard

**Next Step:** After setup, run:
```bash
streamlit run app.py
```

Access at: `http://localhost:8501`

### Path 2: Docker (No Python Installation)

Perfect if you have Docker installed.

```bash
cd dashboard_project

# Build
docker build -t ai-policy-dashboard .

# Run
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  ai-policy-dashboard

# Or use Docker Compose
docker-compose up -d
```

Access at: `http://localhost:8501`

### Path 3: Cloud Deployment (Production)

Perfect for sharing with others.

**Streamlit Cloud (Free, Easiest):**
1. Push to GitHub
2. Go to share.streamlit.io
3. Create app from your GitHub repo
4. Done! Your dashboard is live

**AWS/Azure/Google Cloud:**
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 📂 Project Structure

```
dashboard_project/
├── 📄 app.py                      ← Main Streamlit app
├── 📄 preprocess_data.py          ← Data preparation
├── 📋 requirements.txt            ← Python packages
├── 🐳 Dockerfile                  ← Docker config
├── 🐳 docker-compose.yml          ← Docker Compose
│
├── 📁 src/                        ← Core modules
│   ├── data_processor.py          ← Load & clean data
│   ├── nlp_analyzer.py            ← ML models
│   └── utils.py                   ← Helper functions
│
├── 📁 data/                       ← Processed data (auto-generated)
├── 📁 models/                     ← Saved ML models (auto-generated)
│
├── 📖 README.md                   ← Full documentation
├── 📖 DEPLOYMENT.md               ← Deployment guide
├── 📖 QUICKSTART.md               ← Quick setup
└── 📖 ARCHITECTURE.md             ← Technical details
```

---

## 🔄 Data Pipeline Explained

### Input Data
Located in parent directory:
```
../agora/
├── documents.csv      ← AI policy documents
├── authorities.csv    ← Governments/organizations
├── segments.csv       ← Policy segments
└── collections.csv    ← Document collections

../generativeaiopinion.csv ← Social media opinions
```

### Processing Steps
1. **Load** - Read CSV files
2. **Clean** - Remove duplicates, handle missing values
3. **Enrich** - Extract features, add metadata
4. **Analyze** - Run NLP models
5. **Export** - Save processed data

### Output Data
Generated in `data/` folder:
```
data/
├── processed_documents.csv        ← Cleaned documents
├── merged_policy_data.csv         ← With metadata
├── processed_opinions.csv         ← Cleaned opinions
├── sentiment_analysis.csv         ← Sentiment scores
├── topics.csv                     ← Topic modeling results
├── keywords.csv                   ← Top keywords
├── maturity_scores.csv            ← Policy rankings
└── regulatory_intensity.csv       ← Domain analysis
```

---

## 🎯 Key Components

### Data Processor (`src/data_processor.py`)
```python
processor = DataProcessor(data_dir)
processor.load_agora_data()           # Load policies
processor.load_opinion_data()          # Load opinions
processor.clean_documents()            # Clean data
processor.merge_policy_data()          # Enrich with metadata
processor.export_processed_data()      # Save results
```

### NLP Analyzer (`src/nlp_analyzer.py`)
```python
analyzer = NLPAnalyzer()
sentiments = analyzer.sentiment_analysis(texts)        # Sentiment
lda_matrix, topics = analyzer.topic_modeling(texts)   # Topics
keywords = analyzer.extract_keywords(texts)            # Keywords
domains = analyzer.detect_policy_domains(texts)        # Domains
clusters = analyzer.clustering_analysis(texts)         # Clusters
```

### Regulation Scorer (`src/nlp_analyzer.py`)
```python
scorer = RegulationScorer()
scores = scorer.calculate_maturity_score(df)          # Rankings
intensity = scorer.regulatory_intensity(df)           # Domain analysis
```

---

## 🎨 Dashboard Features

### 📊 Interactive Visualizations
- Bar charts, line charts, pie charts
- Heatmaps and scatter plots
- Word clouds and network diagrams
- Geographic maps (with extensions)

### 🔍 Advanced Filtering
- Filter by authority/country
- Date range selection
- Domain/topic filters
- Custom search

### 📈 Analytics
- Policy maturity scoring
- Regulatory intensity tracking
- Sentiment distribution
- Topic trends over time

### 📥 Export Options
- CSV downloads
- PDF reports
- JSON data
- Custom formats

---

## ⚙️ Configuration

### Streamlit Settings
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"          # Main color
backgroundColor = "#ffffff"       # Background

[server]
port = 8501                       # Server port
maxUploadSize = 1024              # Max upload size
```

### NLP Parameters
Edit `src/nlp_analyzer.py`:
```python
# Number of topics
n_topics = 8

# TF-IDF settings
max_features = 1000
min_df = 2
max_df = 0.8

# Sentiment thresholds
positive_threshold = 0.05
negative_threshold = -0.05
```

### Data Processing
Edit `preprocess_data.py`:
```python
# Sample size (reduce for faster processing)
texts = df['full_text'].values[:1000]

# Topic modeling
lda_matrix, topics = analyzer.topic_modeling(texts, n_topics=10)
```

---

## 🚀 Running the Dashboard

### Start Dashboard
```bash
# Activate environment (if needed)
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate.bat # Windows

# Run app
streamlit run app.py

# Optional: specify port
streamlit run app.py --server.port 8502
```

### Access Dashboard
Open browser: `http://localhost:8501`

### Stop Dashboard
Press `Ctrl+C` in terminal

### View Logs
```bash
streamlit run app.py --logger.level=debug
```

---

## 🧪 Testing & Validation

### Test Data Loading
```bash
python -c "from src.data_processor import DataProcessor; p = DataProcessor('.'); p.load_agora_data(); print('✓ Data loaded')"
```

### Test NLP Models
```bash
python -c "from src.nlp_analyzer import NLPAnalyzer; a = NLPAnalyzer(); print('✓ Models ready')"
```

### Test Streamlit
```bash
streamlit hello  # Built-in demo
```

### Manual Data Processing
```bash
python preprocess_data.py
```

---

## 📊 Dashboard Pages Explained

### 1️⃣ Home Page
- Project overview
- Feature highlights
- Data loading button
- Quick statistics

### 2️⃣ Policy Analytics
- Top authorities chart
- Document timeline
- Filterable data table
- Export button

### 3️⃣ Sentiment Analysis
- Sentiment distribution pie chart
- Sentiment score histogram
- Sample opinions by sentiment
- Sentiment filtering

### 4️⃣ Topic Modeling
- Configurable topic count
- Top topics display
- Keywords extraction
- Domain analysis

### 5️⃣ Trends & Forecasting
- Maturity index ranking
- Regulatory intensity by domain
- Temporal trend analysis
- Growth metrics

### 6️⃣ Search & Explore
- Full-text search box
- Search results display
- Document preview
- Direct links to sources

### 7️⃣ Reports
- Executive summary
- Country comparison
- Domain analysis
- Custom report builder
- Download options

---

## 🔒 Security Best Practices

✅ **Implement for Production:**
- [ ] Enable HTTPS/SSL
- [ ] Use environment variables for secrets
- [ ] Implement authentication
- [ ] Regular security updates
- [ ] Monitor and log access
- [ ] Backup data regularly
- [ ] Set up firewalls
- [ ] Use read-only access where possible

---

## 📈 Performance Optimization

### Speed Up Dashboard
```python
# Cache expensive operations
@st.cache_data
def load_data():
    return pd.read_csv(...)

# Limit data rows
df = df.head(10000)

# Use smaller sample for testing
df_sample = df.sample(n=1000)
```

### Reduce Memory Usage
```python
# Use dtype optimization
df['date'] = pd.to_datetime(df['date'])
df['category'] = df['category'].astype('category')

# Delete unused columns
df = df.drop(['unused_col'], axis=1)
```

---

## 🐛 Troubleshooting

### Setup Issues
| Problem | Solution |
|---------|----------|
| Python not found | Install Python 3.9+ |
| Permission denied (Mac/Linux) | Run `chmod +x setup.sh` |
| Virtual env fails | Try `python3 -m venv venv` |

### Data Issues
| Problem | Solution |
|---------|----------|
| Data files not found | Check paths in `../agora/` |
| Processing fails | Try running `python preprocess_data.py` |
| Memory error | Reduce sample size in preprocessing |

### Dashboard Issues
| Problem | Solution |
|---------|----------|
| Port in use | Run on different port: `--server.port 8502` |
| Slow loading | Clear cache: `streamlit cache clear` |
| NLTK errors | Download: `python -m nltk.downloader vader_lexicon` |

---

## 🔗 Deployment Paths

### Option 1: Local Development
- **Setup:** 5 minutes
- **Cost:** Free
- **Use:** Testing, customization

### Option 2: Docker
- **Setup:** 10 minutes
- **Cost:** Free (or cheap cloud instance)
- **Use:** Local testing, easy deployment

### Option 3: Streamlit Cloud
- **Setup:** 10 minutes
- **Cost:** Free tier available
- **Use:** Production, sharing with team

### Option 4: AWS/Azure
- **Setup:** 30-60 minutes
- **Cost:** $10-100/month
- **Use:** Enterprise, high traffic

### Option 5: Self-Hosted
- **Setup:** 1-2 hours
- **Cost:** Server costs
- **Use:** Full control, on-premise

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Feature overview & documentation |
| QUICKSTART.md | 5-minute quick start |
| DEPLOYMENT.md | Detailed deployment guide |
| This file | Getting started guide |

---

## ✅ Checklist

- [ ] Download/extract project
- [ ] Review this Getting Started guide
- [ ] Run setup script (`setup.bat` or `setup.sh`)
- [ ] Start dashboard (`streamlit run app.py`)
- [ ] Explore each page
- [ ] Test data filtering and exports
- [ ] Choose deployment method
- [ ] Deploy to your platform
- [ ] Share with team/stakeholders

---

## 🎓 Next Steps

1. **Explore Locally** (15 min)
   - Run dashboard
   - Load data
   - Click through pages

2. **Customize** (1-2 hours)
   - Add your own data
   - Modify NLP models
   - Change colors/branding

3. **Deploy** (1-2 hours)
   - Choose platform
   - Follow deployment guide
   - Go live

4. **Monitor** (Ongoing)
   - Check logs
   - Monitor performance
   - Update as needed

---

## 🤝 Support

- **Questions?** Check README.md or DEPLOYMENT.md
- **Issues?** Review Troubleshooting section above
- **Custom needs?** Modify code in `src/` folder
- **Help wanted?** Refer to documentation and comments in code

---

## 📞 Quick Reference

```bash
# Setup (one-time)
setup.bat                    # Windows
./setup.sh                   # Mac/Linux

# Activate environment
venv\Scripts\activate.bat    # Windows
source venv/bin/activate     # Mac/Linux

# Run dashboard
streamlit run app.py

# Preprocess data
python preprocess_data.py

# Run with Docker
docker-compose up

# Deploy
# See DEPLOYMENT.md

# Stop
Ctrl+C                       # In terminal
```

---

**Ready to start?** 
👉 Run `setup.bat` (Windows) or `./setup.sh` (Mac/Linux)

**Questions?** 
📖 Check [README.md](README.md) or [DEPLOYMENT.md](DEPLOYMENT.md)

**Let's build something amazing! 🚀**
