# 🤖 Global AI Policy Trends Dashboard

A comprehensive, interactive dashboard for monitoring and analyzing global AI policy trends, regulations, and ethical frameworks using advanced data processing, visualization, and machine learning.

## ✨ Features

- **📊 Policy Analytics**: Explore AI policy documents by country, domain, status, and temporal trends
- **🗣️ Sentiment Analysis**: Analyze public opinion on generative AI from social media
- **🎯 Topic Modeling**: Discover key themes and policy domains using LDA analysis
- **📈 Trend & Forecasting**: Track regulatory intensity and policy evolution over time
- **🔍 Advanced Search**: Full-text search across all policy documents
- **📋 Custom Reports**: Generate and export insights in multiple formats
- **🌍 Global Coverage**: 1000+ AI policy documents from 50+ international sources
- **⚡ Real-time Updates**: Process new data and visualize trends instantly

## 📦 Tech Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, NLTK, Gensim, BERTopic
- **Visualization**: Plotly, Matplotlib, Seaborn
- **NLP**: spaCy, TextBlob, VADER
- **Deployment**: Docker, Streamlit Cloud, AWS/Azure
- **Database**: CSV/Parquet (scalable to PostgreSQL)

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip or conda
- (Optional) Docker for containerized deployment

### Local Installation

1. **Clone/Download the project**
```bash
cd dashboard_project
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Preprocess the data**
```bash
python preprocess_data.py
```

This will:
- Load all AI policy datasets
- Clean and normalize documents
- Perform NLP analysis (topic modeling, sentiment analysis)
- Extract keywords and calculate policy maturity scores
- Generate processed data files in the `data/` directory

5. **Run the dashboard**
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## CI/CD: Deploying to Render (example)

This repository includes a sample GitHub Actions workflow to build a Docker image and trigger a Render deploy. To enable it:

1. Push this repo to GitHub and create a `main` branch.
2. In GitHub repository settings -> Secrets, add:
    - `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` (or change the workflow to use GitHub Container Registry)
    - `RENDER_SERVICE_ID` and `RENDER_API_KEY` (obtain from Render dashboard)
3. On push to `main`, the workflow will build and push the image and trigger Render to deploy your service.

Alternatively use Streamlit Cloud by connecting the repo to Streamlit and selecting `app.py` as the entrypoint.

## Landing page & searchability

The `public/index.html` includes a small metadata block with the unique access code (`AI-DASH-2026-7G4Z`) to help basic search discovery and to act as a redirect when you set `DEPLOY_URL`.

## One-command deploy helpers

If you have Docker and want to deploy locally or to Render, use the provided helper scripts.

Local Docker (build & run):
```powershell
.\scripts\deploy_local_docker.ps1 -ImageName ai-policy-dashboard -Port 8501
```

Render deploy (build, push, trigger deploy):
```bash
export DOCKERHUB_USERNAME=your_user
export DOCKERHUB_TOKEN=your_token
export RENDER_SERVICE_ID=svc-xxxxx
export RENDER_API_KEY=your_api_key
bash scripts/deploy_render.sh
```

Automation helpers
- Set production `DEPLOY_URL` in the landing page:
```powershell
.\scripts\set_deploy_url.ps1 -Url "https://yourdomain.example.com"
```
- Push repo to GitHub and set secrets (requires `gh` CLI):
```bash
# Example: create/push repo and set DockerHub + Render secrets
bash scripts/github_deploy_helper.sh my-repo my-github-user my-dockerhub-user svc-xxxxx
```




## 📂 Project Structure

```
dashboard_project/
├── app.py                    # Main Streamlit application
├── preprocess_data.py        # Data preprocessing pipeline
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── src/
│   ├── data_processor.py    # Data loading and processing
│   ├── nlp_analyzer.py      # NLP and ML components
│   └── utils.py             # Utility functions
├── data/                    # Processed data files (generated)
└── models/                  # Saved ML models (generated)
```

## 🔄 Data Processing Pipeline

The preprocessing script performs the following steps:

1. **Data Loading**: Loads from AGORA dataset (documents, authorities, segments, collections)
2. **Data Cleaning**: Removes duplicates, handles missing values, normalizes text
3. **Metadata Enrichment**: Adds derived fields (document length, word count, etc.)
4. **NLP Analysis**:
   - Sentiment analysis on social media opinions
   - Topic modeling (LDA) to extract key themes
   - Keyword extraction using TF-IDF
   - Policy domain detection
5. **Scoring**: Calculates policy maturity indices and regulatory intensity metrics
6. **Export**: Saves processed data for dashboard visualization

## 📊 Dashboard Pages

### 🏠 Home
- Overview of dashboard features
- Quick statistics
- Data loading interface

### 📊 Policy Analytics
- Summary metrics and KPIs
- Top authorities by document count
- Document timeline visualization
- Filterable data table
- CSV export functionality

### 🗣️ Sentiment Analysis
- Sentiment distribution (Positive/Negative/Neutral)
- Compound sentiment score distribution
- Sample opinions by sentiment category
- Real-time sentiment filtering

### 🎯 Topic Modeling
- LDA topic analysis with configurable topic count
- Top keywords extraction
- Topic word cloud visualizations
- Domain identification

### 📈 Trends & Forecasting
- Policy Maturity Index by authority
- Regulatory intensity by domain
- Temporal trend analysis
- Forecasting models (optional)

### 🔍 Search & Explore
- Full-text search across documents
- Document preview and details
- Direct links to source documents
- Search result rankings

### 📋 Reports
- Executive summary generation
- Country comparison reports
- Domain analysis reports
- Custom report builder
- PDF/CSV/TXT export options

## 🐳 Docker Deployment

### Build and Run with Docker

```bash
# Build the image
docker build -t ai-policy-dashboard .

# Run the container
docker run -p 8501:8501 ai-policy-dashboard

# Or use Docker Compose
docker-compose up -d
```

Access the dashboard at `http://localhost:8501`

### Docker Environment Variables

```bash
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_LOGGER_LEVEL=info
```

## ☁️ Cloud Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Create a new app and connect your GitHub repo
4. Select `app.py` as the main file
5. Deploy!

### AWS Deployment

```bash
# Using EC2
# 1. Launch an EC2 instance (Ubuntu 22.04)
# 2. SSH into the instance
# 3. Clone the repository
# 4. Run installation steps above
# 5. Use a process manager like systemd or supervisor

# Using Elastic Beanstalk
eb create ai-policy-dashboard
eb deploy
```

### Azure Deployment

```bash
# Create App Service
az appservice plan create --name dashboardplan --resource-group mygroup --sku B1 --is-linux
az webapp create --resource-group mygroup --plan dashboardplan --name ai-policy-dashboard --deployment-container-image-name-user <image>
```

## HTTPS & Custom Domain (Hosting)

These steps help you secure the app with HTTPS and attach a custom domain when hosting on common platforms.

- Streamlit Cloud: Streamlit manages HTTPS automatically when you add a custom domain in the app settings. Follow Streamlit Cloud domain setup and add the supplied CNAME record to your DNS provider.
- Render: In your Render service settings -> Custom Domains, add your domain and follow Render's DNS instructions. Render provides automatic Let's Encrypt certificates — enable "Force HTTPS" in the service settings.
- Docker on a VM / EC2: Use a reverse proxy (Nginx) with Certbot for Let's Encrypt. Example Nginx server block:

```nginx
server {
    listen 80;
    server_name yourdomain.example.com;
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Then run Certbot:
```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.example.com
```

- Azure App Service: Add a custom domain in the Azure portal and then upload a certificate or use App Service Managed Certificate (free) — follow Azure docs to bind the certificate to your app.

Notes:
- Ensure your DNS A or CNAME records point to the hosting provider's target.
- After DNS propagates, verify HTTPS by visiting `https://yourdomain.example.com`.
- For production, consider HSTS and auto-renewal (Certbot handles renewals via cron/systemd timers).

## 🔐 Secure Local Launcher (unique access code)

You can create a short reusable access code that lets you start the dashboard locally and open it in your browser.

Files:
- `scripts/generate_access_code.py` — generate and save a code to `scripts/access_code.txt`
- `scripts/access_code.txt` — stores the current code (generated once)
- `scripts/start_with_access.ps1` — PowerShell starter that prompts for the code and launches the app

Usage (PowerShell):
```powershell
cd "c:\Users\Sai Pranav\Downloads\AI policy dataset\dashboard_project"
python scripts/generate_access_code.py    # optionally regenerate a new code
.\scripts\start_with_access.ps1          # enter the code when prompted
```

The starter will activate the project's `venv` (if present), run `streamlit run app.py` and open `http://localhost:8501` in your default browser.


## 🔧 Configuration

### Streamlit Configuration
Edit `.streamlit/config.toml` to customize:
- Theme colors
- Server port and address
- Browser behavior
- Security settings
- Logging levels

### NLP Parameters
Modify in `src/nlp_analyzer.py`:
- Number of topics for LDA
- TF-IDF parameters
- Sentiment analysis thresholds
- Clustering parameters

## 📈 Key Metrics & KPIs

The dashboard tracks:
- Total policy documents and authorities
- Average document length and word count
- Sentiment distribution (Positive/Negative/Neutral)
- Topic distribution across documents
- Policy maturity scores by jurisdiction
- Regulatory intensity by domain
- Temporal trends in policy adoption

## 🛠️ Development

### Adding New Data Sources

Edit `src/data_processor.py`:

```python
def load_custom_data(self):
    """Load custom data source"""
    custom_df = pd.read_csv('path/to/data.csv')
    # Process and integrate
    return custom_df
```

### Adding New Visualizations

Edit `app.py` and add to relevant page:

```python
fig = px.scatter(data, x='column1', y='column2', title='New Chart')
st.plotly_chart(fig, use_container_width=True)
```

### Custom ML Models

Add to `src/nlp_analyzer.py`:

```python
def custom_model(self, texts):
    """Implement custom ML logic"""
    # Your code here
    return results
```

## 📊 Sample Data

The dashboard includes sample data from:
- **AGORA Dataset**: 1000+ AI policy documents
- **Generative AI Opinions**: Social media sentiment data
- **Regulatory Documents**: Official policy texts
- **Domain Classifications**: Application and impact area categorizations

## 🔒 Security Considerations

- Store sensitive configuration in environment variables
- Use HTTPS for production deployments
- Implement user authentication for sensitive data
- Regular security audits
- Keep dependencies updated: `pip install --upgrade -r requirements.txt`

## 📝 License

This project is provided as-is for analysis and research purposes.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting section below

## 🔧 Troubleshooting

### Data Loading Issues
```bash
# Ensure data files are in the correct location
ls -la ../agora/
ls -la ../generativeaiopinion.csv

# Try preprocessing again
python preprocess_data.py
```

### Memory Issues with Large Datasets
```python
# In app.py, reduce sample size:
texts = df['full_text'].fillna('').values[:5000]  # Instead of all
```

### Streamlit Port Already in Use
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Missing NLTK Data
```bash
python -m nltk.downloader vader_lexicon punkt stopwords
```

## 📚 Further Reading

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Documentation](https://plotly.com/python/)
- [Scikit-learn NLP Guide](https://scikit-learn.org/stable/modules/)
- [NLTK Book](https://www.nltk.org/book/)
- [Policy Analytics Research](https://cset.georgetown.edu/)

## 🎯 Roadmap

- [ ] Real-time policy document scraping
- [ ] Advanced forecasting models (ARIMA, Prophet)
- [ ] Multi-language support
- [ ] Database integration (PostgreSQL)
- [ ] User authentication and dashboards
- [ ] API endpoints for integration
- [ ] Advanced clustering visualizations
- [ ] Policy impact simulation tools

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Active Development ✅
