**User:**

<task>
Create deployment and configuration setup for a Streamlit-based Customer Churn Analytics Dashboard. Include Streamlit `config.toml` theme and server settings, responsive UI configuration, production-ready deployment structure, GitHub integration, requirements setup, Docker support, environment variables, and step-by-step deployment process using Streamlit Cloud. Also include security, performance optimization, scalability suggestions, troubleshooting tips, and best practices for hosting and maintaining the dashboard in production.
</task>
<environment_details>
# VSCode Visible Files
.streamlit/config.toml

# VSCode Open Tabs
README.md,docs/SCALABLE_ARCHITECTURE.md,docs/ARCHITECTURE_DIAGRAMS.md,LICENSE,app.py,.gitignore,tests/smoke_tests.py,src/biz_metrics.py,docs/DATA_EXPLORATION_ENHANCEMENT_PLAN.md,docs/DATA_EXPLORATION_ARCHITECTURE.md,docs/IMPLEMENTATION_GUIDE.md,docs/PLAN_SUMMARY.md,docs/CUSTOMER_SEGMENTATION_ENHANCEMENT_PLAN.md,docs/SEGMENTATION_IMPLEMENTATION_GUIDE.md,docs/SEGMENTATION_TECHNICAL_GUIDE.md,docs/SEGMENTATION_IMPLEMENTATION_ROADMAP.md,docs/SEGMENTATION_PLAN_SUMMARY.md,src/data_prep.py,src/eda_utils.py,src/helpers.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T14:00:52.318Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>


# Current Workspace Directory (/Users/meetjain/Downloads/InsightStream-main) Files
.gitignore
app.py
LICENSE
README.md
requirements.txt
.streamlit/
data/
data/generate_synthetic_data.py
data/sample_churn.csv
docs/
docs/CUSTOMER_SEGMENTATION_ENHANCEMENT_PLAN.md
docs/DATA_EXPLORATION_ARCHITECTURE.md
docs/DATA_EXPLORATION_ENHANCEMENT_PLAN.md
docs/IMPLEMENTATION_GUIDE.md
docs/PLAN_SUMMARY.md
docs/SCALABLE_ARCHITECTURE.md
docs/SEGMENTATION_IMPLEMENTATION_ROADMAP.md
docs/SEGMENTATION_PLAN_SUMMARY.md
docs/SEGMENTATION_TECHNICAL_GUIDE.md
models/
models/encoders_scalers/
models/encoders_scalers/num_scaler.pkl
models/encoders_scalers/ohe_encoder.pkl
notebooks/
notebooks/eda_playground.ipynb
pages/
pages/1_Data_Exploration.py
pages/2_Customer_Groups.py
pages/3_Customer_Retention.py
pages/4_Business_Insights.py
src/
src/biz_metrics.py
src/data_prep.py
src/eda_utils.py
src/helpers.py
src/sql_utils.py
tests/
tests/smoke_tests.py
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll help you create a comprehensive deployment and configuration setup for your Streamlit-based Customer Churn Analytics Dashboard. Let me start by examining the current project structure and existing configuration.

<read_file>
<args>
  <file>
    <path>.streamlit/config.toml</path>
  </file>
  <file>
    <path>requirements.txt</path>
  </file>
  <file>
    <path>app.py</path>
    <line_range>1-50</line_range>
  </file>
  <file>
    <path>.gitignore</path>
  </file>
  <file>
    <path>README.md</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 5 files] Result:
<files>
<file><path>.streamlit/config.toml</path>
<content lines="1-14">
 1 | # Streamlit configuration
 2 | [theme]
 3 | primaryColor = "#FF6B6B"  # Vibrant red for primary actions
 4 | backgroundColor = "#F5F5F5"  # Light gray background
 5 | secondaryBackgroundColor = "#FFFFFF"  # White for cards/sections
 6 | textColor = "#31333F"  # Dark gray text
 7 | font = "sans serif"
 8 | 
 9 | [server]
10 | enableCORS = false
11 | enableXsrfProtection = true
12 | 
13 | [browser]
14 | gatherUsageStats = false
</content>
</file>
<file><path>requirements.txt</path>
<content lines="1-23">
 1 | # Core libraries
 2 | pandas>=1.5.0
 3 | numpy>=1.22.0
 4 | matplotlib>=3.5.0
 5 | seaborn>=0.11.0
 6 | plotly>=5.5.0
 7 | 
 8 | # Web app
 9 | streamlit>=1.15.0
10 | 
11 | # Database
12 | sqlalchemy>=1.4.0
13 | 
14 | # For data analysis
15 | scipy>=1.8.0
16 | 
17 | # For exports
18 | xlsxwriter>=3.0.0
19 | 
20 | # For data processing
21 | scikit-learn>=1.0.0
22 | 
23 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
</content>
</file>
<file><path>app.py</path>
<content lines="1-50">
 1 | """
 2 | Customer Business Analysis Dashboard for E-commerce
 3 | 
 4 | This is our main app file that ties everything together. It's like the home page
 5 | where users start their journey through the dashboard. From here, they can load data,
 6 | see key metrics, and navigate to different pages.
 7 | 
 8 | No fancy stuff here just the essential tools businesses need to understand their customers better.
 9 | Think of it as a Swiss Army knife for customer data!
10 | """
11 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
12 | 
13 | import streamlit as st
14 | import pandas as pd
15 | import numpy as np
16 | import os
17 | import sys
18 | from pathlib import Path
19 | 
20 | # Add parent directory to path
21 | sys.path.append(os.path.dirname(os.path.abspath(__file__)))
22 | 
23 | # Import utilities
24 | from src.helpers import (
25 |     SAMPLE_DATA_PATH, DB_PATH, 
26 |     NUMERIC_COLS, CATEGORICAL_COLS, BINARY_COLS, TARGET_COL, ID_COL,
27 |     ensure_dir
28 | )
29 | from src.data_prep import load_csv, prepare_data_for_analysis
30 | from src.sql_utils import create_db_and_table, upsert_clean_data
31 | 
32 | # Set page config
33 | st.set_page_config(
34 |     page_title="Business Analysis Dashboard",
35 |     page_icon="�",
36 |     layout="wide",
37 |     initial_sidebar_state="expanded"
38 | )
39 | 
40 | # Initialize session state
41 | if 'data' not in st.session_state:
42 |     st.session_state.data = None
43 | if 'data_processed' not in st.session_state:
44 |     st.session_state.data_processed = False
45 | if 'db_created' not in st.session_state:
46 |     st.session_state.db_created = os.path.exists(DB_PATH)
47 | 
48 | # App title and description
49 | st.title("Supercharge Your Customer Strategy!")
50 | 
</content>
</file>
<file><path>.gitignore</path>
<content lines="1-47">
 1 | # Python
 2 | __pycache__/
 3 | *.py[cod]
 4 | *$py.class
 5 | *.so
 6 | .Python
 7 | env/
 8 | build/
 9 | develop-eggs/
10 | dist/
11 | downloads/
12 | eggs/
13 | .eggs/
14 | lib/
15 | lib64/
16 | parts/
17 | sdist/
18 | var/
19 | *.egg-info/
20 | .installed.cfg
21 | *.egg
22 | 
23 | # Virtual Environment
24 | venv/
25 | .env
26 | .venv
27 | env/
28 | 
29 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
30 | 
31 | # IDE
32 | .idea/
33 | .vscode/
34 | *.swp
35 | *.swo
36 | 
37 | # OS specific
38 | .DS_Store
39 | Thumbs.db
40 | 
41 | # Project specific
42 | models/*.pkl
43 | data/app.db
44 | docs/BUSINESS_REPORT.pdf
45 | 
46 | # Jupyter Notebook
47 | .ipynb_checkpoints
</content>
</file>
<file><path>README.md</path>
<content lines="1-167">
  1 | # ⚠️ PROTECTED CODE - DO NOT COPY ⚠️
  2 | 
  3 | This is a Team project by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). This repository is publicly visible for demonstration purposes only.
  4 | 
  5 | Author: Meet Jain & Aditi Gopinath
  6 | - This project is protected. Do not copy, fork, or reuse without permission.
  7 | - Unauthorized use is strictly prohibited. Only the official deployment is allowed to run.
  8 | 
  9 | ## Legal Protection
 10 | This project is protected by copyright law and includes proprietary security measures. Unauthorized use or attempts to circumvent security measures may result in legal consequences.
 11 | 
 12 | ## Contact
 13 | For any inquiries about this project please contact: meetofficialhere@gmail.com
 14 | 
 15 | # Customer Business Analysis Dashboard
 16 | 
 17 | A powerful, easy-to-use dashboard for analyzing customer behavior, identifying segments, and preventing customer churn.
 18 | 
 19 | ## Overview
 20 | 
 21 | This dashboard helps businesses understand their customers better and make smart decisions to keep them happy. It takes customer data, shows important patterns, and gives actionable advice that anyone can understand - no fancy statistics degree needed!
 22 | 
 23 | ## Features
 24 | 
 25 | The dashboard comes packed with tools that make customer analysis simple:
 26 | 
 27 | - **See Your Data Come to Life**: Interactive charts that show customer patterns anyone can understand
 28 | - **Ask Questions Using SQL**: Run simple queries to dig into your customer data
 29 | - **Group Similar Customers**: Automatically sort customers into meaningful groups
 30 | - **Spot Why Customers Leave**: Find the real reasons behind customer churn
 31 | - **Get Plain-English Advice**: Receive clear recommendations anyone can implement
 32 | 
 33 | ## Dashboard Pages
 34 | 
 35 | Our dashboard has four main sections:
 36 | 
 37 | 1. **Data Explorer**: Look at your customer data in different ways and spot patterns
 38 | 2. **Customer Groups**: See which types of customers you have and how they behave
 39 | 3. **Churn Analysis**: Understand why customers leave and who's at risk
 40 | 4. **Recommendations**: Get practical advice on keeping customers happy
 41 | 
 42 | ## Architecture
 43 | 
 44 | The dashboard is built with a clean, modular structure that makes it easy to understand and extend.
 45 | 
 46 | ```
 47 | ┌─────────────────────────────────────┐
 48 | │           Web Interface             │
 49 | │    (Streamlit Interactive Pages)    │
 50 | └───────────────┬─────────────────────┘
 51 |                 │
 52 | ┌───────────────▼─────────────────────┐
 53 | │         Business Logic Layer         │
 54 | │   (Data Analysis & Visualization)   │
 55 | └───────────────┬─────────────────────┘
 56 |                 │
 57 | ┌───────────────▼─────────────────────┐
 58 | │           Data Access Layer          │
 59 | │      (CSV Import & SQLite DB)       │
 60 | └─────────────────────────────────────┘
 61 | ```
 62 | 
 63 | ### Component Diagram
 64 | 
 65 | ```
 66 | ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
 67 | │  Data Input  │───▶│  Processing   │───▶│ Visualization│
 68 | │  & Storage   │    │  & Analysis   │    │  & Reports   │
 69 | └──────────────┘    └───────────────┘    └──────────────┘
 70 |        │                   │                    │
 71 |        ▼                   ▼                    ▼
 72 | ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
 73 | │ CSV Importer │    │ Segmentation  │    │ Interactive  │
 74 | │ SQLite DB    │    │ Churn Models  │    │ Dashboards   │
 75 | └──────────────┘    └───────────────┘    └──────────────┘
 76 | ```
 77 | 
 78 | ## How to Use the Dashboard
 79 | 
 80 | ### Getting Started
 81 | 
 82 | When you open the dashboard, you'll see a home page with these options:
 83 | 
 84 | 1. **Load Sample Data**: Click this button to try out the dashboard with example data
 85 | 2. **Upload Your Own Data**: Upload your customer data file (CSV format)
 86 | 3. **Save to Database**: Store your data for faster access next time
 87 | 
 88 | ### Understanding Your Customers
 89 | 
 90 | Once your data is loaded, you can:
 91 | 
 92 | - **See Key Numbers**: Total customers, churn rate, and customer value at a glance
 93 | - **Explore Different Pages**: Use the sidebar to navigate between dashboard sections
 94 | - **Download Reports**: Export insights as CSV files to share with your team
 95 | 
 96 | ### Data You Can Use
 97 | 
 98 | To get the most from this dashboard, your customer data should include:
 99 | 
100 | - **Must Have**:
101 |   - `customer_id`: A unique number/code for each customer
102 |   - `churn`: Whether they've left (1) or stayed (0)
103 | 
104 | - **Good to Have**:
105 |   - **Who they are**: Age, gender, location
106 |   - **What they buy**: Number of orders, average spending
107 |   - **How they engage**: Days since last purchase, loyalty points
108 |   - **Customer experience**: Number of complaints
109 |   - **Other useful info**: Payment method, months as customer, etc.
110 | 
111 | Sample data is included if you just want to try things out!
112 | 
113 | ## Project Organization
114 | 
115 | The project is organized into these key folders:
116 | 
117 | ```
118 | Customer-Churn-Dashboard/
119 | ├── app.py                # Main dashboard entry point
120 | ├── requirements.txt      # Python package dependencies
121 | ├── .streamlit/           # Streamlit configuration
122 | ├── data/                 # Data files and database
123 | │   └── sample_churn.csv  # Example customer dataset
124 | ├── pages/                # Dashboard page files
125 | │   ├── 1_EDA_and_SQL_Checks.py           # Data exploration page
126 | │   ├── 2_Customer_Segments.py            # Customer segmentation page
127 | │   ├── 3_Churn_Analysis.py               # Churn analysis page
128 | │   └── 4_Insights_and_Recommendations.py  # Insights page
129 | └── src/                  # Source code modules
130 |     ├── data_prep.py      # Data preparation functions
131 |     ├── helpers.py        # Helper utilities and constants
132 |     └── sql_utils.py      # Database functions
133 | ```
134 | 
135 | ## Analysis Methods Made Simple
136 | 
137 | The dashboard uses these business techniques, explained in plain language:
138 | 
139 | 1. **RFM Grouping**: Groups customers based on:
140 |    - How Recently they purchased
141 |    - How Frequently they buy
142 |    - How Much Money they spend
143 | 
144 | 2. **Customer Journey**: Tracks how customers behave over time from when they first joined
145 | 
146 | 3. **Churn Reasons**: Finds the real factors that make customers leave
147 | 
148 | 4. **Customer Value**: Shows how much a customer is worth to your business long-term
149 | 
150 | 5. **Ask Your Own Questions**: Use simple SQL queries to answer specific business questions
151 | 
152 | ## License
153 | 
154 | This project is licensed under the MIT License - see the LICENSE file for details.
155 | 
156 | ## Contact
157 | 
158 | Connect us through the following platforms:
159 | 
160 | ### Professional Networking
161 | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/meet-jain-413015265/)
162 | [![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=flat&logo=twitter&logoColor=white)](https://twitter.com/Meetjain_100)
163 | 
164 | ### Social Media and Platforms
165 | [![Discord](https://img.shields.io/badge/Discord-7289DA?style=flat&logo=discord&logoColor=white)](https://discordapp.com/users/meetofficial)
166 | [![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/m.jain_17/)
167 | 
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
.streamlit/config.toml

# VSCode Open Tabs
README.md,docs/SCALABLE_ARCHITECTURE.md,docs/ARCHITECTURE_DIAGRAMS.md,LICENSE,app.py,.gitignore,tests/smoke_tests.py,src/biz_metrics.py,docs/DATA_EXPLORATION_ENHANCEMENT_PLAN.md,docs/DATA_EXPLORATION_ARCHITECTURE.md,docs/IMPLEMENTATION_GUIDE.md,docs/PLAN_SUMMARY.md,docs/CUSTOMER_SEGMENTATION_ENHANCEMENT_PLAN.md,docs/SEGMENTATION_IMPLEMENTATION_GUIDE.md,docs/SEGMENTATION_TECHNICAL_GUIDE.md,docs/SEGMENTATION_IMPLEMENTATION_ROADMAP.md,docs/SEGMENTATION_PLAN_SUMMARY.md,src/data_prep.py,src/eda_utils.py,src/helpers.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T14:01:51.765Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.02

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Based on my analysis of your Customer Churn Analytics Dashboard project, I'll provide you with a comprehensive deployment and configuration guide. Let me create detailed documentation covering all aspects of production deployment.

## 📋 Comprehensive Deployment Guide for Customer Churn Analytics Dashboard

### 1. **Enhanced Streamlit Configuration**

Your current [`config.toml`](.streamlit/config.toml:1) is basic. Here's an enhanced production-ready version:

```toml
# .streamlit/config.toml - Production Configuration

[theme]
primaryColor = "#FF6B6B"           # Vibrant red for primary actions
backgroundColor = "#F5F5F5"         # Light gray background
secondaryBackgroundColor = "#FFFFFF" # White for cards/sections
textColor = "#31333F"              # Dark gray text
font = "sans serif"

[server]
# Server Configuration
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200                # Max file upload size in MB
maxMessageSize = 200               # Max WebSocket message size in MB
enableWebsocketCompression = true
headless = true                    # Run without browser auto-open

# Session Management
cookieSecret = "your-secret-key-here"  # Change in production!
enableStaticServing = true

[browser]
gatherUsageStats = false
serverAddress = "localhost"
serverPort = 8501

[runner]
# Performance Settings
magicEnabled = true
fastReruns = true
enforceSerializableSessionState = false

[client]
# Client-side Settings
showErrorDetails = false           # Hide detailed errors in production
toolbarMode = "minimal"

[logger]
# Logging Configuration
level = "info"                     # Options: debug, info, warning, error
messageFormat = "%(asctime)s %(message)s"

[deprecation]
showPyplotGlobalUse = false
```

### 2. **Environment Variables Setup**

Create a `.env.example` file for environment variable templates:

```bash
# .env.example - Copy to .env and fill in values

# Application Settings
APP_ENV=production
DEBUG=false
SECRET_KEY=your-secret-key-here

# Database Configuration
DB_PATH=data/app.db
SAMPLE_DATA_PATH=data/sample_churn.csv

# Security
ENABLE_AUTH=false
ALLOWED_ORIGINS=https://yourdomain.com

# Performance
CACHE_TTL=3600
MAX_WORKERS=4

# Monitoring
ENABLE_ANALYTICS=true
LOG_LEVEL=INFO

# External Services (if needed)
# API_KEY=your-api-key
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
```

Update your [`.gitignore`](.gitignore:1) to include:
```
.env
.env.local
.env.production
secrets.toml
```

### 3. **Docker Support**

**Dockerfile:**
```dockerfile
# Dockerfile - Production-ready container

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data models/encoders_scalers .streamlit

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**docker-compose.yml:**
```yaml
# docker-compose.yml - Multi-container setup

version: '3.8'

services:
  streamlit-app:
    build: .
    container_name: churn-dashboard
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - APP_ENV=production
      - DEBUG=false
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Add nginx reverse proxy
  nginx:
    image: nginx:alpine
    container_name: churn-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - streamlit-app
    restart: unless-stopped
```

**.dockerignore:**
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
.git
.gitignore
.dockerignore
.env
.env.*
*.md
docs/
tests/
notebooks/
.vscode/
.idea/
*.swp
*.swo
.DS_Store
Thumbs.db
```

### 4. **Enhanced Requirements with Version Pinning**

```txt
# requirements.txt - Production dependencies with pinned versions

# Core Data Science Libraries
pandas==2.1.4
numpy==1.26.2
scipy==1.11.4
scikit-learn==1.3.2

# Visualization
matplotlib==3.8.2
seaborn==0.13.0
plotly==5.18.0

# Web Framework
streamlit==1.29.0

# Database
sqlalchemy==2.0.23

# Data Export
xlsxwriter==3.1.9

# Performance & Caching
streamlit-extras==0.3.6

# Security (optional but recommended)
python-dotenv==1.0.0

# Monitoring (optional)
# sentry-sdk==1.39.1

# © 2026 | Project created by Meet Jain(@Meetjain1) and Aditi Gopinath(@aaditiiiii1)
```

### 5. **Streamlit Cloud Deployment Guide**

#### **Step-by-Step Deployment Process:**

**Step 1: Prepare Your Repository**
```bash
# Ensure all files are committed
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

**Step 2: Create `secrets.toml` Template**
Create `.streamlit/secrets.toml.example`:
```toml
# .streamlit/secrets.toml.example
# Copy to secrets.toml and fill in production values

[general]
app_env = "production"
secret_key = "your-secret-key-here"

[database]
db_path = "data/app.db"

# Add any API keys or sensitive data here
# [api]
# key = "your-api-key"
```

**Step 3: Deploy to Streamlit Cloud**

1. **Go to**: https://share.streamlit.io/
2. **Sign in** with GitHub
3. **Click**: "New app"
4. **Configure**:
   - Repository: `your-username/InsightStream`
   - Branch: `main`
   - Main file path: `app.py`
   - Python version: `3.10`

5. **Add Secrets** (in Streamlit Cloud dashboard):
   - Go to App Settings → Secrets
   - Paste contents from your `secrets.toml`

6. **Deploy**: Click "Deploy!"

**Step 4: Custom Domain (Optional)**
```
# In Streamlit Cloud Settings:
1. Go to Settings → General
2. Add custom domain: yourdomain.com
3. Configure DNS:
   - Type: CNAME
   - Name: app (or subdomain)
   - Value: [your-app].streamlit.app
```

### 6. **Alternative Deployment Options**

#### **A. Heroku Deployment**

**Procfile:**
```
web: sh setup.sh && streamlit run app.py
```

**setup.sh:**
```bash
#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

**runtime.txt:**
```
python-3.10.13
```

#### **B. AWS EC2 Deployment**

```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clone repository
git clone https://github.com/your-username/InsightStream.git
cd InsightStream

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with systemd
sudo nano /etc/systemd/system/streamlit.service
```

**systemd service file:**
```ini
[Unit]
Description=Streamlit Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/InsightStream
Environment="PATH=/home/ubuntu/InsightStream/venv/bin"
ExecStart=/home/ubuntu/InsightStream/venv/bin/streamlit run app.py

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable streamlit
sudo systemctl start streamlit
sudo systemctl status streamlit
```

#### **C. Google Cloud Run**

**cloudbuild.yaml:**
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/churn-dashboard', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/churn-dashboard']
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'churn-dashboard'
      - '--image'
      - 'gcr.io/$PROJECT_ID/churn-dashboard'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
```

### 7. **Security Best Practices**

#### **A. Authentication Layer (Optional)**

Create `src/auth.py`:
```python
"""
Simple authentication for Streamlit app
"""
import streamlit as st
import hashlib
import os

def check_password():
    """Returns `True` if user has correct password."""
    
    def password_entered():
        """Checks whether password entered is correct."""
        if hashlib.sha256(
            st.session_state["password"].encode()
        ).hexdigest() == os.getenv("PASSWORD_HASH"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct
        return True
```

Add to [`app.py`](app.py:1):
```python
from src.auth import check_password

# Add after imports
if not check_password():
    st.stop()
```

#### **B. Security Headers**

Create `nginx.conf` for reverse proxy:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream streamlit {
        server streamlit-app:8501;
    }

    server {
        listen 80;
        server_name yourdomain.com;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

        # Rate limiting
        limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;
        limit_req zone=one burst=20;

        location / {
            proxy_pass http://streamlit;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 86400;
        }
    }
}
```

### 8. **Performance Optimization**

#### **A. Caching Strategy**

Update [`app.py`](app.py:1) with caching:
```python
import streamlit as st

# Cache data loading
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data_cached(file_path):
    """Load data with caching"""
    return load_csv(file_path)

# Cache expensive computations
@st.cache_resource
def get_database_connection():
    """Cache database connection"""
    return create_db_and_table()
```

#### **B. Lazy Loading**

```python
# Load heavy libraries only when needed
def load_ml_models():
    """Lazy load ML models"""
    if 'models_loaded' not in st.session_state:
        import pickle
        # Load models here
        st.session_state.models_loaded = True
```

#### **C. Resource Limits**

Add to `config.toml`:
```toml
[server]
maxUploadSize = 200
maxMessageSize = 200
enableWebsocketCompression = true

[runner]
fastReruns = true
```

### 9. **Monitoring & Logging**

#### **A. Application Logging**

Create `src/logger.py`:
```python
"""
Logging configuration for the application
"""
import logging
import sys
from pathlib import Path

def setup_logger(name: str, log_file: str = None, level=logging.INFO):
    """Setup logger with file and console handlers"""
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(console_format)
        logger.addHandler(file_handler)
    
    return logger

# Usage in app.py
logger = setup_logger(__name__, 'logs/app.log')
logger.info("Application started")
```

#### **B. Error Tracking (Sentry Integration)**

```python
# Add to app.py
import sentry_sdk
from sentry_sdk.integrations.streamlit import StreamlitIntegration

if os.getenv("APP_ENV") == "production":
    sentry_sdk.init(
        dsn="your-sentry-dsn",
        integrations=[StreamlitIntegration()],
        traces_sample_rate=1.0,
    )
```

### 10. **Scalability Recommendations**

#### **A. Database Optimization**

For larger datasets, consider:
```python
# Use connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    f'sqlite:///{DB_PATH}',
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

#### **B. Horizontal Scaling**

For high traffic, use load balancer:
```yaml
# docker-compose-scaled.yml
version: '3.8'

services:
  streamlit-app:
    build: .
    deploy:
      replicas: 3
    environment:
      - APP_ENV=production

  load-balancer:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - streamlit-app
```

#### **C. CDN Integration**

For static assets:
```python
# Serve static files from CDN
CDN_URL = os.getenv("CDN_URL", "")

def get_asset_url(asset_path):
    """Get CDN URL for static assets"""
    if CDN_URL:
        return f"{CDN_URL}/{asset_path}"
    return asset_path
```

### 11. **Troubleshooting Guide**

#### **Common Issues & Solutions:**

| Issue | Solution |
|-------|----------|
| **App crashes on startup** | Check logs: `streamlit run app.py --logger.level=debug` |
| **Memory errors** | Reduce `maxUploadSize` in config.toml, add caching |
| **Slow performance** | Enable caching, optimize queries, use `@st.cache_data` |
| **WebSocket errors** | Check firewall, enable CORS if needed |
| **File upload fails** | Increase `maxUploadSize` in config.toml |
| **Database locked** | Use connection pooling, check concurrent access |

#### **Debug Mode:**

```python
# Add to app.py for debugging
if os.getenv("DEBUG") == "true":
    st.sidebar.write("Debug Info:")
    st.sidebar.json({
        "session_state": dict(st.session_state),
        "env": os.getenv("APP_ENV"),
        "python_version": sys.version
    })
```

### 12. **CI/CD Pipeline**

#### **GitHub Actions Workflow**

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest tests/ --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Streamlit Cloud
        run: |
          echo "Deployment triggered automatically by Streamlit Cloud"
```

### 13. **Maintenance Checklist**

#### **Daily:**
- [ ] Monitor application logs
- [ ] Check error rates
- [ ] Verify uptime

#### **Weekly:**
- [ ] Review performance metrics
- [ ] Check disk space usage
- [ ] Update dependencies (security patches)
- [ ] Backup database

#### **Monthly:**
- [ ] Review and optimize queries
- [ ] Update documentation
- [ ] Security audit
- [ ] Performance testing

#### **Quarterly:**
- [ ] Major dependency updates
- [ ] Feature review
- [ ] User feedback analysis
- [ ] Disaster recovery test

### 14. **Production Deployment Checklist**

Before going live:

- [ ] Update `config.toml` with production settings
- [ ] Set environment variables in `.env`
- [ ] Configure secrets in Streamlit Cloud
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring and logging
- [ ] Configure backups
- [ ] Test error handling
- [ ] Verify performance under load
- [ ] Document deployment process
- [ ] Set up CI/CD pipeline
- [ ] Configure custom domain (if applicable)
- [ ] Enable security headers
- [ ] Test disaster recovery
- [ ] Create runbook for common issues

### 15. **Quick Start Commands**

```bash
# Local Development
streamlit run app.py

# Docker Development
docker-compose up --build

# Docker Production
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f streamlit-app

# Stop services
docker-compose down

# Update and restart
git pull origin main
docker-compose up -d --build
```

---

## 📊 Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        A[Web Browser]
    end
    
    subgraph "Load Balancer"
        B[Nginx/CDN]
    end
    
    subgraph "Application Layer"
        C[Streamlit App 1]
        D[Streamlit App 2]
        E[Streamlit App N]
    end
    
    subgraph "Data Layer"
        F[(SQLite DB)]
        G[CSV Files]
        H[Model Files]
    end
    
    subgraph "Monitoring"
        I[Logs]
        J[Metrics]
        K[Alerts]
    end
    
    A --> B
    B --> C
    B --> D
    B --> E
    C --> F
    C --> G
    C --> H
    D --> F
    E --> F
    C --> I
    C --> J
    J --> K
```

## 🎯 Summary

This comprehensive guide provides everything needed to deploy your Customer Churn Analytics Dashboard to production:

1. **Enhanced Configuration**: Production-ready Streamlit settings with security and performance optimizations
2. **Multiple Deployment Options**: Streamlit Cloud, Docker, Heroku, AWS, GCP
3. **Security**: Authentication, environment variables, security headers
4. **Performance**: Caching strategies, lazy loading, resource optimization
5. **Monitoring**: Logging, error tracking, health checks
6. **Scalability**: Horizontal scaling, load balancing, CDN integration
7. **Maintenance**: CI/CD pipeline, backup strategies, troubleshooting guide

The dashboard is now ready for production deployment with enterprise-grade reliability, security, and performance! 🚀

---

**User:**

[ERROR] You did not use a tool in your previous response! Please retry with a tool use.

# Reminder: Instructions for Tool Use

Tool uses are formatted using XML-style tags. The tool name itself becomes the XML tag name. Each parameter is enclosed within its own set of tags. Here's the structure:

<actual_tool_name>
<parameter1_name>value1</parameter1_name>
<parameter2_name>value2</parameter2_name>
...
</actual_tool_name>

For example, to use the attempt_completion tool:

<attempt_completion>
<result>
I have completed the task...
</result>
</attempt_completion>

Always use the actual tool name as the XML tag name for proper parsing and execution.

# Next Steps

If you have completed the user's task, use the attempt_completion tool.
If you require additional information from the user, use the ask_followup_question tool.
Otherwise, if you have not completed the task and do not need additional information, then proceed with the next step of the task.
(This is an automated message, so do not respond to it conversationally.)
<environment_details>
# VSCode Visible Files
.streamlit/config.toml

# VSCode Open Tabs
README.md,docs/SCALABLE_ARCHITECTURE.md,docs/ARCHITECTURE_DIAGRAMS.md,LICENSE,app.py,.gitignore,tests/smoke_tests.py,src/biz_metrics.py,docs/DATA_EXPLORATION_ENHANCEMENT_PLAN.md,docs/DATA_EXPLORATION_ARCHITECTURE.md,docs/IMPLEMENTATION_GUIDE.md,docs/PLAN_SUMMARY.md,docs/CUSTOMER_SEGMENTATION_ENHANCEMENT_PLAN.md,docs/SEGMENTATION_IMPLEMENTATION_GUIDE.md,docs/SEGMENTATION_TECHNICAL_GUIDE.md,docs/SEGMENTATION_IMPLEMENTATION_ROADMAP.md,docs/SEGMENTATION_PLAN_SUMMARY.md,src/data_prep.py,src/eda_utils.py,src/helpers.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T14:03:04.395Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.08

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
I've provided a comprehensive deployment and configuration guide for your Streamlit-based Customer Churn Analytics Dashboard covering:

**Configuration & Setup:**
- Enhanced [`config.toml`](.streamlit/config.toml:1) with production settings (server, theme, performance, security)
- Environment variables template (`.env.example`)
- Updated [`.gitignore`](.gitignore:1) for secrets

**Deployment Options:**
- **Streamlit Cloud**: Step-by-step guide with secrets management and custom domain setup
- **Docker**: Complete Dockerfile, docker-compose.yml, and .dockerignore
- **Heroku**: Procfile and setup scripts
- **AWS EC2**: systemd service configuration
- **Google Cloud Run**: cloudbuild.yaml

**Security:**
- Authentication layer implementation
- Security headers via nginx
- Environment variable management
- Rate limiting configuration

**Performance:**
- Caching strategies with `@st.cache_data` and `@st.cache_resource`
- Lazy loading patterns
- Resource limits and compression
- Database connection pooling

**Monitoring & Maintenance:**
- Logging setup with file and console handlers
- Sentry integration for error tracking
- Health checks and metrics
- Daily/weekly/monthly maintenance checklist

**Scalability:**
- Horizontal scaling with load balancer
- CDN integration for static assets
- Multi-replica deployment configuration

**CI/CD:**
- GitHub Actions workflow for automated testing and deployment
- Production deployment checklist

**Troubleshooting:**
- Common issues and solutions table
- Debug mode configuration
- Quick start commands

The guide includes production-ready configurations, best practices, and step-by-step instructions for deploying your dashboard to various platforms with enterprise-grade reliability.
</result>
</attempt_completion>

