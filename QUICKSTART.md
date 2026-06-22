# ⚡ Quick Start Guide - AI Policy Trends Dashboard

Get your AI Policy Dashboard running in 5 minutes!

## 🎯 Fastest Way to Start

### Windows Users

```bash
# 1. Download and extract the project
# 2. Open Command Prompt in the project folder
# 3. Run this single command:
setup.bat
```

That's it! The setup script will:
- ✅ Create Python virtual environment
- ✅ Install all dependencies
- ✅ Download NLP models
- ✅ Process your data
- ✅ Show you how to run the dashboard

### Mac/Linux Users

```bash
# 1. Download and extract the project
# 2. Open Terminal in the project folder
# 3. Run these commands:
chmod +x setup.sh
./setup.sh
```

## 🚀 Run Your Dashboard

After setup completes:

```bash
# 1. Activate the environment
# Windows:
venv\Scripts\activate.bat

# Mac/Linux:
source venv/bin/activate

# 2. Start the dashboard
streamlit run app.py

# 3. Open in your browser
# http://localhost:8501
```

## 📊 What You'll See

1. **Home** - Dashboard overview and data loading
2. **Policy Analytics** - Explore AI policy documents
3. **Sentiment Analysis** - Public opinion on AI
4. **Topic Modeling** - Key themes in policies
5. **Trends** - Regulatory intensity and scoring
6. **Search** - Find specific documents
7. **Reports** - Generate and export insights

## 🐳 Docker Users (No Python Installation Needed)

```bash
# Prerequisites: Docker installed

# Build the dashboard
docker build -t ai-policy-dashboard .

# Run it
docker run -p 8501:8501 ai-policy-dashboard

# Open: http://localhost:8501
```

## ☁️ Deploy Online (Easiest)

### Streamlit Cloud (Free Tier Available)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "Create app"
4. Select your GitHub repo and `app.py`
5. Click "Deploy" - Done! 🎉

Your dashboard will be live at: `https://your-username-appname.streamlit.app`

### AWS (Quick)

```bash
# If you have AWS CLI configured:
eb init -p python-3.11 ai-policy-dashboard
eb create production
eb deploy
```

## 📁 Key Files Explained

| File | Purpose |
|------|---------|
| `app.py` | Main dashboard application |
| `preprocess_data.py` | Data preparation script |
| `requirements.txt` | Python dependencies |
| `src/data_processor.py` | Data loading & cleaning |
| `src/nlp_analyzer.py` | ML & sentiment analysis |
| `Dockerfile` | Docker configuration |
| `DEPLOYMENT.md` | Detailed deployment guide |

## 🔧 Troubleshooting

### "Command not found" error
- Make sure you're in the project directory
- Windows: Use Command Prompt (not PowerShell if path issues)

### Data loading error
- Ensure the data files are in the parent directory: `../agora/`
- Run `python preprocess_data.py` manually

### Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
```

### Memory issues
- Use fewer documents for processing (edit `preprocess_data.py`)
- Deploy to cloud with more resources

## 📚 Next Steps

1. **Explore the Dashboard**
   - Load data on the Home page
   - Click through each analytics section

2. **Customize Your Data**
   - Add new datasets in `src/data_processor.py`
   - Modify NLP models in `src/nlp_analyzer.py`

3. **Deploy to Production**
   - Follow [DEPLOYMENT.md](DEPLOYMENT.md) for full setup
   - Choose your platform (AWS, Azure, Streamlit Cloud, etc.)

4. **Monitor Performance**
   - Check logs in deployment platform
   - Setup alerts for issues

## 🆘 Need Help?

- **Can't install?** Check you have Python 3.9+ installed
- **Dashboard won't load?** Check data files exist
- **Performance issues?** Reduce data sample size
- **Want to customize?** Edit files in `src/` folder

## 📖 Full Documentation

- **README.md** - Complete feature overview
- **DEPLOYMENT.md** - Detailed deployment instructions
- **src/data_processor.py** - Data processing code
- **src/nlp_analyzer.py** - ML models and NLP code

## 🎓 Learning Path

1. Run the dashboard locally
2. Explore each page and features
3. Read the DEPLOYMENT guide
4. Choose your deployment method
5. Deploy to production
6. Monitor and maintain

## 💡 Pro Tips

- Use `--logger.level=debug` for Streamlit debugging
- Cache your data processing with `@st.cache_resource`
- Use Streamlit Cloud secrets for sensitive data
- Monitor with CloudWatch (AWS) or Application Insights (Azure)

---

**Ready? Start with:** `setup.bat` (Windows) or `./setup.sh` (Mac/Linux)

**Have questions?** Check DEPLOYMENT.md for comprehensive guide!
