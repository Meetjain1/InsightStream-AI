**User:**

<task>
Design a scalable architecture for a Customer Churn Analytics Dashboard using Streamlit, Python, SQLite, and Machine Learning. Include frontend dashboard structure, backend data processing flow, database layer, churn prediction module, customer segmentation module, visualization layer, and recommendation engine. Explain folder structure and how components communicate with each other
</task>
<environment_details>
# VSCode Visible Files
../bob_task_may-16-2026_5-47-09-pm.md

# VSCode Open Tabs
README.md,../bob_task_may-16-2026_5-47-09-pm.md,LICENSE,app.py,.gitignore,tests/smoke_tests.py,src/biz_metrics.py,src/data_prep.py,src/eda_utils.py,src/helpers.py,pages/1_Data_Exploration.py,pages/3_Customer_Retention.py,src/sql_utils.py,data/generate_synthetic_data.py,notebooks/eda_playground.ipynb,pages/4_Business_Insights.py,pages/2_Customer_Groups.py,requirements.txt

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T12:40:18.371Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>


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

I'll analyze the existing project structure and design a scalable architecture for the Customer Churn Analytics Dashboard. Let me start by gathering more context about the current implementation.

<read_file>
<args>
  <file>
    <path>README.md</path>
  </file>
  <file>
    <path>app.py</path>
  </file>
  <file>
    <path>requirements.txt</path>
  </file>
  <file>
    <path>src/helpers.py</path>
  </file>
  <file>
    <path>src/data_prep.py</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 5 files] Result:
<files>
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
<file><path>app.py</path>
<content lines="1-304">
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
 51 | st.markdown("""
 52 | ## Unlock the Hidden Potential in Your Customer Data!
 53 | 
 54 | This powerful dashboard transforms raw customer information into **game-changing business insights**. 
 55 | Discover what makes your customers tick, why they stay (or leave), and how to boost your bottom line!
 56 | 
 57 | ### What You'll Discover:
 58 | - **Reveal surprising patterns** in your customer data with eye-popping visualizations
 59 | - **Unearth valuable insights** with custom SQL queries anyone can use
 60 | - **Identify your VIP customers** and target them with laser precision
 61 | - **Spot at-risk customers** before they leave and win them back
 62 | - **Get brilliant, actionable ideas** to skyrocket your retention rates
 63 | 
 64 | **Get started now!** Load your data or try our sample dataset below.
 65 | """)
 66 | 
 67 | # Sidebar with data options
 68 | with st.sidebar:
 69 |     st.header("Fire Up Your Analysis!")
 70 |     
 71 |     # Load sample data button
 72 |     if st.button("Load Amazing Sample Data!"):
 73 |         # Check if sample data exists
 74 |         if os.path.exists(SAMPLE_DATA_PATH):
 75 |             with st.spinner("Loading sample data..."):
 76 |                 df = load_csv(SAMPLE_DATA_PATH)
 77 |                 if df is not None and not df.empty:
 78 |                     st.session_state.data = df
 79 |                     st.success(f"Loaded {len(df)} sample records! Now you can explore")
 80 |                 else:
 81 |                     st.error("Failed to load sample data")
 82 |         else:
 83 |             # Try to generate sample data
 84 |             st.info("Sample data not found. Generating synthetic data...")
 85 |             try:
 86 |                 # Run the data generation script
 87 |                 import subprocess
 88 |                 result = subprocess.run(["python", "data/generate_synthetic_data.py"], 
 89 |                                         capture_output=True, text=True)
 90 |                 
 91 |                 if os.path.exists(SAMPLE_DATA_PATH):
 92 |                     df = load_csv(SAMPLE_DATA_PATH)
 93 |                     if df is not None and not df.empty:
 94 |                         st.session_state.data = df
 95 |                         st.success(f"Generated and loaded {len(df)} sample records!")
 96 |                     else:
 97 |                         st.error("Failed to load generated data")
 98 |                 else:
 99 |                     st.error("Failed to generate sample data")
100 |                     st.code(result.stderr)
101 |             except Exception as e:
102 |                 st.error(f"Error generating sample data: {str(e)}")
103 |     
104 |     # Upload own data
105 |     st.subheader("Or Upload Your Own Fantastic Data!")
106 |     uploaded_file = st.file_uploader("Drop your CSV file here and let's make magic!", type=["csv"])
107 |     if uploaded_file is not None:
108 |         try:
109 |             df = pd.read_csv(uploaded_file)
110 |             
111 |             # Basic validation
112 |             required_cols = [ID_COL, TARGET_COL]
113 |             missing_cols = [col for col in required_cols if col not in df.columns]
114 |             
115 |             if missing_cols:
116 |                 st.error(f"Missing required columns: {', '.join(missing_cols)}")
117 |                 st.info(f"Required columns: {', '.join(required_cols)}")
118 |             else:
119 |                 st.session_state.data = df
120 |                 st.success(f"Uploaded {len(df)} records. Ready for analysis!")
121 |         except Exception as e:
122 |             st.error(f"Error uploading file: {str(e)}")
123 |     
124 |     # Save to database button
125 |     if st.session_state.data is not None:
126 |         if st.button("Blast Off to Database!"):
127 |             with st.spinner("Saving to database..."):
128 |                 # First apply data preparation steps
129 |                 processed_data = prepare_data_for_analysis(st.session_state.data)
130 |                 result = upsert_clean_data(processed_data)
131 |                 if result:
132 |                     st.session_state.db_created = True
133 |                     st.session_state.data_processed = True
134 |                     st.success("Data saved to database! SQL queries ready to go")
135 |                 else:
136 |                     st.error("Failed to save to database")
137 |     
138 |     # Help text
139 |     st.markdown("---")
140 |     st.subheader("Quick Start Guide")
141 |     st.markdown("""
142 |     1. Load our awesome sample data or upload your own
143 |     2. Dive into dazzling visualizations
144 |     3. Run powerful SQL queries (no tech skills needed!)
145 |     4. Group customers and discover hidden patterns
146 |     5. Get brilliant ideas to boost your business
147 |     """)
148 |     
149 |     # App info
150 |     st.markdown("---")
151 |     st.caption("Customer Insight Revolution | v2.0.0")
152 | 
153 | # Main page content
154 | if st.session_state.data is not None:
155 |     # Show a data preview
156 |     st.header("Your Amazing Data Preview")
157 |     st.write("Behold! A sneak peek at your customer goldmine:")
158 |     st.dataframe(st.session_state.data.head(5), use_container_width=True)
159 |     
160 |     # Data stats
161 |     st.subheader("Power Metrics at a Glance!")
162 |     col1, col2, col3, col4 = st.columns(4)
163 |     with col1:
164 |         st.metric("Total Customers", f"{len(st.session_state.data):,}")
165 |     with col2:
166 |         churn_rate = st.session_state.data[TARGET_COL].mean() * 100
167 |         st.metric("Churn Rate", f"{churn_rate:.1f}%")
168 |     with col3:
169 |         if 'avg_order_value' in st.session_state.data.columns:
170 |             avg_order = st.session_state.data['avg_order_value'].mean()
171 |             st.metric("Avg Order Value", f"${avg_order:.2f}")
172 |     with col4:
173 |         if 'tenure_months' in st.session_state.data.columns:
174 |             avg_tenure = st.session_state.data['tenure_months'].mean()
175 |             st.metric("Avg Customer Lifespan", f"{avg_tenure:.1f} months")
176 |     
177 |     st.markdown("---")
178 |     
179 |     # Business KPIs
180 |     st.header("Treasure Trove of Business Insights")
181 |     
182 |     # Calculate important metrics
183 |     active_customers = len(st.session_state.data[st.session_state.data[TARGET_COL] == 0])
184 |     churn_count = len(st.session_state.data[st.session_state.data[TARGET_COL] == 1])
185 |     
186 |     # Customer Lifetime Value calculation (if relevant columns exist)
187 |     if 'avg_order_value' in st.session_state.data.columns and 'tenure_months' in st.session_state.data.columns:
188 |         # Simplified CLV calculation
189 |         avg_monthly_revenue = st.session_state.data['avg_order_value'].mean()
190 |         avg_lifetime = st.session_state.data['tenure_months'].mean()
191 |         estimated_margin = 0.3  # Assuming 30% profit margin
192 |         clv = avg_monthly_revenue * avg_lifetime * estimated_margin
193 |     else:
194 |         clv = None
195 |     
196 |     # Display metrics in cards
197 |     metric_col1, metric_col2, metric_col3 = st.columns(3)
198 |     
199 |     with metric_col1:
200 |         st.markdown("### Active Customers")
201 |         st.markdown(f"<h2 style='text-align: center; color: #4ECDC4;'>{active_customers:,}</h2>", unsafe_allow_html=True)
202 |         retention_rate = active_customers / len(st.session_state.data) * 100
203 |         st.markdown(f"<p style='text-align: center;'>Retention Rate: {retention_rate:.1f}%</p>", unsafe_allow_html=True)
204 |     
205 |     with metric_col2:
206 |         st.markdown("### Churned Customers")
207 |         st.markdown(f"<h2 style='text-align: center; color: #FF6B6B;'>{churn_count:,}</h2>", unsafe_allow_html=True)
208 |         st.markdown(f"<p style='text-align: center;'>Churn Rate: {churn_rate:.1f}%</p>", unsafe_allow_html=True)
209 |     
210 |     with metric_col3:
211 |         st.markdown("### Customer Lifetime Value")
212 |         if clv:
213 |             st.markdown(f"<h2 style='text-align: center; color: #FFD166;'>${clv:.2f}</h2>", unsafe_allow_html=True)
214 |             st.markdown("<p style='text-align: center;'>Average value per customer</p>", unsafe_allow_html=True)
215 |         else:
216 |             st.markdown("<h2 style='text-align: center; color: #FFD166;'>N/A</h2>", unsafe_allow_html=True)
217 |             st.markdown("<p style='text-align: center;'>Insufficient data to calculate</p>", unsafe_allow_html=True)
218 | 
219 |     st.markdown("---")
220 | 
221 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
222 | 
223 |     # Navigation help
224 |     st.header("Your Adventure Map")
225 |     st.write("Embark on your data journey through these exciting destinations:")
226 |     
227 |     # Page descriptions with icons
228 |     col1, col2 = st.columns(2)
229 |     with col1:
230 |         st.markdown("### Data Exploration")
231 |         st.write("""
232 |         - **Uncover hidden gems** in your customer data
233 |         - **Spot exciting trends** that others miss
234 |         - **Create powerful SQL queries** with ease
235 |         - **Build eye-popping visualizations** instantly
236 |         """)
237 |         
238 |         st.markdown("### Customer Groups")
239 |         st.write("""
240 |         - **Discover your customer tribes** based on real behavior
241 |         - **Decode buying patterns** that drive purchases
242 |         - **Identify your VIP customers** worth pampering
243 |         - **Unlock special insights** for each customer group
244 |         """)
245 |     
246 |     with col2:
247 |         st.markdown("### Customer Retention")
248 |         st.write("""
249 |         - **Discover why customers leave** (and how to make them stay!)
250 |         - **Pinpoint loyalty patterns** across customer groups
251 |         - **Track retention trends** with stunning visuals
252 |         - **Connect the dots** between behavior and loyalty
253 |         """)
254 |         
255 |         st.markdown("### Business Insights")
256 |         st.write("""
257 |         - **Transform data into money-making actions**
258 |         - **Craft laser-targeted strategies** for each group
259 |         - **Calculate the profit impact** of your retention efforts
260 |         - **Generate brilliant action plans** your team will love
261 |         """)
262 | 
263 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
264 | 
265 | else:
266 |     # No data loaded yet
267 |     st.info("Ready for liftoff! Load our amazing sample data or upload your own to begin your data adventure!")
268 |     
269 |     # Show example of what the data should look like
270 |     st.subheader("Example Data Format")
271 |     
272 |     # Create example data
273 |     example_data = {
274 |         'customer_id': ['CUST000123', 'CUST000456', 'CUST000789'],
275 |         'age': [32, 45, 28],
276 |         'gender': ['Female', 'Male', 'Female'],
277 |         'region': ['Urban', 'Suburban', 'Rural'],
278 |         'total_orders': [15, 4, 8],
279 |         'avg_order_value': [75.20, 120.50, 55.30],
280 |         'days_since_last_purchase': [12, 90, 30],
281 |         'loyalty_score': [0.75, 0.30, 0.60],
282 |         'complaints': [0, 2, 1],
283 |         'payment_type': ['Credit Card', 'PayPal', 'Credit Card'],
284 |         'tenure_months': [24, 8, 12],
285 |         'is_promo_user': [0, 1, 0],
286 |         'churn': [0, 1, 0]
287 |     }
288 |     
289 |     example_df = pd.DataFrame(example_data)
290 |     st.dataframe(example_df, use_container_width=True)
291 |     
292 |     st.markdown("""
293 |     **Required columns:**
294 |     - `customer_id`: Unique customer identifier
295 |     - `churn`: Target variable (0 = retained, 1 = churned)
296 |     
297 |     **Recommended columns:**
298 |     - Demographic data (age, gender, region)
299 |     - Purchase history (total_orders, avg_order_value)
300 |     - Engagement metrics (days_since_last_purchase, loyalty_score)
301 |     - Other relevant features (complaints, payment_type, etc.)
302 |     """)
303 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
304 | 
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
<file><path>src/helpers.py</path>
<content lines="1-109">
  1 | """
  2 | The Helper's Toolbox - Making Life Easier!
  3 | 
  4 | This file has all those handy tools and settings that we use throughout the dashboard.
  5 | It's like the utility belt that keeps everything running smoothly.
  6 | 
  7 | No rocket science here - just practical functions that save us time and keep things consistent.
  8 | """
  9 | import os
 10 | import pandas as pd
 11 | import numpy as np
 12 | from pathlib import Path
 13 | 
 14 | # Root dir
 15 | ROOT_DIR = Path(__file__).parent.parent
 16 | 
 17 | # Data paths
 18 | DATA_DIR = os.path.join(ROOT_DIR, "data")
 19 | SAMPLE_DATA_PATH = os.path.join(DATA_DIR, "sample_churn.csv")
 20 | DB_PATH = os.path.join(DATA_DIR, "app.db")
 21 | 
 22 | # Data config
 23 | TARGET_COL = "churn"
 24 | 
 25 | # Feature groups
 26 | NUMERIC_COLS = [
 27 |     "age", 
 28 |     "total_orders", 
 29 |     "avg_order_value", 
 30 |     "days_since_last_purchase", 
 31 |     "loyalty_score", 
 32 |     "complaints", 
 33 |     "tenure_months"
 34 | ]
 35 | 
 36 | CATEGORICAL_COLS = [
 37 |     "gender", 
 38 |     "region", 
 39 |     "payment_type"
 40 | ]
 41 | 
 42 | BINARY_COLS = [
 43 |     "is_promo_user"
 44 | ]
 45 | 
 46 | ID_COL = "customer_id"
 47 | 
 48 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
 49 | # All features (excluding target and id)
 50 | FEATURE_COLS = NUMERIC_COLS + CATEGORICAL_COLS + BINARY_COLS
 51 | 
 52 | # Business config
 53 | COST_RETAIN = 50  # cost of retention offer
 54 | AVG_FUTURE_ORDERS = 3  # expected future orders if customer stays
 55 | 
 56 | # Simple helper to check if a directory exists, if not create it
 57 | def ensure_dir(directory):
 58 |     """Make sure directory exists, if not create it"""
 59 |     if not os.path.exists(directory):
 60 |         os.makedirs(directory)
 61 |         print(f"Created directory: {directory}")
 62 |     return directory
 63 | 
 64 | def get_risk_band(churn_value):
 65 |     """Convert churn value to risk band based on business rules"""
 66 |     if churn_value == 1:
 67 |         return "High Risk"
 68 |     else:
 69 |         return "Low Risk"
 70 | 
 71 | def calculate_days_recency_score(days_since_purchase):
 72 |     """Calculate recency score based on days since last purchase"""
 73 |     if days_since_purchase <= 30:
 74 |         return 3  # Recently active
 75 |     elif days_since_purchase <= 90:
 76 |         return 2  # Active but slipping
 77 |     else:
 78 |         return 1  # Inactive
 79 | 
 80 | def calculate_frequency_score(total_orders):
 81 |     """Calculate frequency score based on total orders"""
 82 |     if total_orders >= 10:
 83 |         return 3  # Frequent buyer
 84 |     elif total_orders >= 5:
 85 |         return 2  # Regular buyer
 86 |     else:
 87 |         return 1  # Occasional buyer
 88 | 
 89 | def calculate_monetary_score(avg_order_value):
 90 |     """Calculate monetary score based on average order value"""
 91 |     if avg_order_value >= 100:
 92 |         return 3  # High value
 93 |     elif avg_order_value >= 50:
 94 |         return 2  # Medium value
 95 |     else:
 96 |         return 1  # Low value
 97 | 
 98 | def calculate_rfm_score(days_since_purchase, total_orders, avg_order_value):
 99 |     """Calculate RFM score for customer segmentation"""
100 |     r_score = calculate_days_recency_score(days_since_purchase)
101 |     f_score = calculate_frequency_score(total_orders)
102 |     m_score = calculate_monetary_score(avg_order_value)
103 |     
104 |     return {
105 |         'recency_score': r_score,
106 |         'frequency_score': f_score,
107 |         'monetary_score': m_score,
108 |         'total_score': r_score + f_score + m_score
109 |     }
</content>
</file>
<file><path>src/data_prep.py</path>
<content lines="1-219">
  1 | """
  2 | Data preparation functions for customer churn analysis dashboard.
  3 | """
  4 | import pandas as pd
  5 | import numpy as np
  6 | import os
  7 | from sklearn.impute import SimpleImputer
  8 | 
  9 | from .helpers import (
 10 |     NUMERIC_COLS, CATEGORICAL_COLS, BINARY_COLS, 
 11 |     TARGET_COL, ID_COL, FEATURE_COLS,
 12 |     ensure_dir, calculate_rfm_score, get_risk_band
 13 | )
 14 | 
 15 | def load_csv(path):
 16 |     """Load CSV file into pandas DataFrame"""
 17 |     try:
 18 |         print(f"Loading data from {path}...")
 19 |         df = pd.read_csv(path)
 20 |         print(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns. not bad!")
 21 |         return df
 22 |     except Exception as e:
 23 |         print(f"Error loading data: {e}")
 24 |         return None
 25 | 
 26 | def basic_clean(df):
 27 |     """Basic cleaning - trim strings, fix weird values, cast dtypes, drop dupes"""
 28 |     if df is None or df.empty:
 29 |         print("No data to clean, sad :(")
 30 |         return None
 31 |     
 32 |     print("Starting basic cleaning...")
 33 |     
 34 |     # Make a copy to avoid modifying original
 35 |     df_clean = df.copy()
 36 |     
 37 |     # Check if we have the expected columns
 38 |     missing_cols = []
 39 |     expected_cols = FEATURE_COLS + [TARGET_COL, ID_COL]
 40 | 
 41 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
 42 |     
 43 |     for col in expected_cols:
 44 |         if col not in df_clean.columns:
 45 |             missing_cols.append(col)
 46 |     
 47 |     if missing_cols:
 48 |         print(f"Warning: Missing expected columns: {missing_cols}")
 49 |         print("Will continue with columns we have, fingers crossed...")
 50 |     
 51 |     # Drop duplicates
 52 |     old_shape = df_clean.shape[0]
 53 |     df_clean = df_clean.drop_duplicates()
 54 |     if old_shape > df_clean.shape[0]:
 55 |         print(f"Dropped {old_shape - df_clean.shape[0]} duplicate rows, sneaky dupes!")
 56 |     
 57 |     # Trim string columns
 58 |     for col in df_clean.select_dtypes(include=['object']).columns:
 59 |         df_clean[col] = df_clean[col].str.strip() if hasattr(df_clean[col], 'str') else df_clean[col]
 60 |     
 61 |     # Fix data types
 62 |     if ID_COL in df_clean.columns:
 63 |         df_clean[ID_COL] = df_clean[ID_COL].astype(str)
 64 |     
 65 |     for col in NUMERIC_COLS:
 66 |         if col in df_clean.columns:
 67 |             try:
 68 |                 df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
 69 |             except:
 70 |                 print(f"Couldn't convert {col} to numeric, weird values maybe?")
 71 |     
 72 |     for col in BINARY_COLS:
 73 |         if col in df_clean.columns:
 74 |             df_clean[col] = df_clean[col].astype(int)
 75 |     
 76 |     if TARGET_COL in df_clean.columns:
 77 |         df_clean[TARGET_COL] = df_clean[TARGET_COL].astype(int)
 78 |     
 79 |     print(f"Basic cleaning complete! We have {df_clean.shape[0]} rows now. cool.")
 80 |     return df_clean
 81 | 
 82 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
 83 | 
 84 | def handle_missing(df):
 85 |     """Handle missing values with simple imputations"""
 86 |     if df is None or df.empty:
 87 |         print("No data to handle missing values, bummer")
 88 |         return None
 89 |     
 90 |     print("Looking for missing values...")
 91 |     
 92 |     # Check if we have missing values
 93 |     missing_counts = df.isnull().sum()
 94 |     missing_cols = missing_counts[missing_counts > 0]
 95 |     
 96 |     if len(missing_cols) == 0:
 97 |         print("No missing values found! lucky us.")
 98 |         return df
 99 |     
100 |     print(f"Found missing values in {len(missing_cols)} columns. gonna fix em...")
101 |     
102 |     # Make a copy to avoid modifying original
103 |     df_clean = df.copy()
104 |     
105 |     # Impute numeric columns with median
106 |     num_imputer = SimpleImputer(strategy='median')
107 |     num_cols_to_impute = [col for col in NUMERIC_COLS if col in df_clean.columns and df_clean[col].isnull().sum() > 0]
108 |     
109 |     if num_cols_to_impute:
110 |         print(f"Filling {len(num_cols_to_impute)} numeric columns with median values")
111 |         df_clean[num_cols_to_impute] = num_imputer.fit_transform(df_clean[num_cols_to_impute])
112 |     
113 |     # Impute categorical columns with most frequent value
114 |     cat_imputer = SimpleImputer(strategy='most_frequent')
115 |     cat_cols_to_impute = [col for col in CATEGORICAL_COLS if col in df_clean.columns and df_clean[col].isnull().sum() > 0]
116 |     
117 |     if cat_cols_to_impute:
118 |         print(f"Filling {len(cat_cols_to_impute)} categorical columns with most common values")
119 |         df_clean[cat_cols_to_impute] = cat_imputer.fit_transform(df_clean[cat_cols_to_impute])
120 |     
121 |     # Binary columns (fill with 0 which is safer)
122 |     bin_cols_to_impute = [col for col in BINARY_COLS if col in df_clean.columns and df_clean[col].isnull().sum() > 0]
123 |     
124 |     if bin_cols_to_impute:
125 |         print(f"Filling {len(bin_cols_to_impute)} binary columns with 0s")
126 |         for col in bin_cols_to_impute:
127 |             df_clean[col] = df_clean[col].fillna(0)
128 |     
129 |     # Check if we've resolved all missing values
130 |     remaining_missing = df_clean.isnull().sum().sum()
131 |     if remaining_missing > 0:
132 |         print(f"Warning: Still have {remaining_missing} missing values. thats weird :/")
133 |     else:
134 |         print("All missing values handled! nice and clean now.")
135 |     
136 |     return df_clean
137 | 
138 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
139 | 
140 | def add_derived_features(df):
141 |     """Add derived features for analysis"""
142 |     if df is None or df.empty:
143 |         print("No data to add derived features to")
144 |         return df
145 |     
146 |     df_derived = df.copy()
147 |     
148 |     # Calculate risk band
149 |     if TARGET_COL in df_derived.columns:
150 |         df_derived['risk_band'] = df_derived[TARGET_COL].apply(get_risk_band)
151 |     
152 |     # Create RFM segments if we have the necessary columns
153 |     required_cols = ['days_since_last_purchase', 'total_orders', 'avg_order_value']
154 |     if all(col in df_derived.columns for col in required_cols):
155 |         print("Adding RFM scores and segments...")
156 |         
157 |         # Apply RFM scoring function
158 |         rfm_scores = df_derived.apply(
159 |             lambda row: calculate_rfm_score(
160 |                 row['days_since_last_purchase'], 
161 |                 row['total_orders'], 
162 |                 row['avg_order_value']
163 |             ), 
164 |             axis=1
165 |         )
166 |         
167 |         # Extract individual scores
168 |         df_derived['recency_score'] = rfm_scores.apply(lambda x: x['recency_score'])
169 |         df_derived['frequency_score'] = rfm_scores.apply(lambda x: x['frequency_score'])
170 |         df_derived['monetary_score'] = rfm_scores.apply(lambda x: x['monetary_score'])
171 |         df_derived['rfm_score'] = rfm_scores.apply(lambda x: x['total_score'])
172 |         
173 |         # Create RFM segments
174 |         df_derived['customer_segment'] = pd.cut(
175 |             df_derived['rfm_score'],
176 |             bins=[0, 3, 6, 9],
177 |             labels=['Low Value', 'Medium Value', 'High Value']
178 |         )
179 |         
180 |         print("Added RFM scores and customer segments!")
181 |     
182 |     # Add tenure buckets
183 |     if 'tenure_months' in df_derived.columns:
184 |         df_derived['tenure_bucket'] = pd.cut(
185 |             df_derived['tenure_months'],
186 |             bins=[0, 6, 12, 24, 36, float('inf')],
187 |             labels=['0-6 months', '7-12 months', '1-2 years', '2-3 years', '3+ years'],
188 |             right=False
189 |         )
190 |     
191 |     # Add days since purchase buckets
192 |     if 'days_since_last_purchase' in df_derived.columns:
193 |         df_derived['recency_bucket'] = pd.cut(
194 |             df_derived['days_since_last_purchase'],
195 |             bins=[0, 30, 60, 90, float('inf')],
196 |             labels=['0-30 days', '31-60 days', '61-90 days', 'Over 90 days'],
197 |             right=False
198 |         )
199 |     
200 |     return df_derived
201 | 
202 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
203 | 
204 | def prepare_data_for_analysis(df):
205 |     """Run full data preparation pipeline for analysis"""
206 |     if df is None or df.empty:
207 |         print("No data to prepare")
208 |         return None
209 |     
210 |     # Clean data
211 |     df_clean = basic_clean(df)
212 |     
213 |     # Handle missing values
214 |     df_clean = handle_missing(df_clean)
215 |     
216 |     # Add derived features
217 |     df_clean = add_derived_features(df_clean)
218 |     
219 |     return df_clean
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
../bob_task_may-16-2026_5-47-09-pm.md

# VSCode Open Tabs
README.md,../bob_task_may-16-2026_5-47-09-pm.md,LICENSE,app.py,.gitignore,tests/smoke_tests.py,src/biz_metrics.py,src/data_prep.py,src/eda_utils.py,src/helpers.py,pages/1_Data_Exploration.py,pages/3_Customer_Retention.py,src/sql_utils.py,data/generate_synthetic_data.py,notebooks/eda_playground.ipynb,pages/4_Business_Insights.py,pages/2_Customer_Groups.py,requirements.txt

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T12:40:31.049Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.03

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll analyze the existing project structure and design a comprehensive scalable architecture for the Customer Churn Analytics Dashboard. Let me gather more information about the current implementation.

<read_file>
<args>
  <file>
    <path>pages/1_Data_Exploration.py</path>
    <line_range>1-50</line_range>
  </file>
  <file>
    <path>pages/2_Customer_Groups.py</path>
    <line_range>1-50</line_range>
  </file>
  <file>
    <path>src/sql_utils.py</path>
  </file>
  <file>
    <path>src/biz_metrics.py</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 4 files] Result:
<files>
<file><path>pages/1_Data_Exploration.py</path>
<content lines="1-50">
 1 | """
 2 | EDA and SQL Checks # Set page config
 3 | st.s# Page title
 4 | st.title("Data Exploration")
 5 | st.markdown("Dive into your customer data to uncover amazing insights and hidden patterns!")page_config(
 6 |     page_title="Data Exploration",
 7 |     page_icon=":mag:",
 8 |     layout="wide"
 9 | )amlit Page
10 | """
11 | import streamlit as st
12 | import pandas as pd
13 | import numpy as np
14 | import os
15 | import sys
16 | import sqlite3
17 | from pathlib import Path
18 | 
19 | # Add parent directory to path
20 | sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
21 | 
22 | # Import utilities
23 | from src.helpers import (
24 |     SAMPLE_DATA_PATH, DB_PATH, NUMERIC_COLS, CATEGORICAL_COLS, 
25 |     BINARY_COLS, TARGET_COL, ID_COL
26 | )
27 | from src.data_prep import load_csv, basic_clean, handle_missing
28 | from src.eda_utils import create_eda_plots
29 | from src.sql_utils import run_sql, get_churn_sql_queries
30 | 
31 | # Set page config
32 | st.set_page_config(
33 |     page_title="Data Exploration",
34 |     page_icon="�",
35 |     layout="wide"
36 | )
37 | 
38 | # Initialize session state if not exists
39 | if 'data' not in st.session_state:
40 |     st.session_state.data = None
41 |     # Try to load sample data
42 |     if os.path.exists(SAMPLE_DATA_PATH):
43 |         st.session_state.data = load_csv(SAMPLE_DATA_PATH)
44 | 
45 | if 'db_created' not in st.session_state:
46 |     st.session_state.db_created = os.path.exists(DB_PATH)
47 | 
48 | # Page title
49 | st.title("� Data Exploration")
50 | st.markdown("Dive into your customer data to uncover amazing insights and hidden patterns!")
</content>
</file>
<file><path>pages/2_Customer_Groups.py</path>
<content lines="1-50">
 1 | """
 2 | Customer Segments # Set page config
 3 | st.set_page_config(
 4 |     page_title="Customer Groups",
 5 |     page_icon=":busts_in_silhouette:",
 6 |     layout="wide"
 7 | )amlit Page
 8 | """
 9 | import streamlit as st
10 | import pandas as pd
11 | import numpy as np
12 | import os
13 | import sys
14 | from pathlib import Path
15 | import plotly.express as px
16 | import plotly.graph_objects as go
17 | 
18 | # Add parent directory to path
19 | sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
20 | 
21 | # Import utilities
22 | from src.helpers import (
23 |     NUMERIC_COLS, CATEGORICAL_COLS, BINARY_COLS, TARGET_COL, ID_COL,
24 |     calculate_rfm_score
25 | )
26 | from src.data_prep import prepare_data_for_analysis
27 | 
28 | # Set page config
29 | st.set_page_config(
30 |     page_title="Customer Groups",
31 |     page_icon="�",
32 |     layout="wide"
33 | )
34 | 
35 | # Initialize session state if not exists
36 | if 'data' not in st.session_state:
37 |     st.session_state.data = None
38 | 
39 | # Page title
40 | st.title("Discover Your Customer Groups!")
41 | st.markdown("Group your customers by their shopping habits and create powerful targeted strategies")
42 | 
43 | # Check if data is loaded
44 | if st.session_state.data is None:
45 |     st.warning("No data loaded. Please load data from the home page.")
46 |     st.stop()
47 | 
48 | # Get data
49 | df = st.session_state.data
50 | 
</content>
</file>
<file><path>src/sql_utils.py</path>
<content lines="1-493">
  1 | """
  2 | SQL utilities for business analysis dashboard.
  3 | """
  4 | import os
  5 | import pandas as pd
  6 | from sqlalchemy import create_engine, text
  7 | import sqlite3
  8 | from typing import Optional, List, Dict, Any, Tuple
  9 | 
 10 | from .helpers import DB_PATH, ensure_dir
 11 | 
 12 | def create_db_and_table():
 13 |     """
 14 |     Create SQLite database and customers_clean table
 15 |     """
 16 |     try:
 17 |         # Make sure the directory exists
 18 |         ensure_dir(os.path.dirname(DB_PATH))
 19 |         
 20 |         # Create engine
 21 |         engine = create_engine(f"sqlite:///{DB_PATH}")
 22 |         
 23 |         # Create the table with the schema
 24 |         create_table_query = """
 25 |         CREATE TABLE IF NOT EXISTS customers_clean (
 26 |             customer_id TEXT PRIMARY KEY,
 27 |             age INTEGER,
 28 |             gender TEXT,
 29 |             region TEXT,
 30 |             total_orders INTEGER,
 31 |             avg_order_value REAL,
 32 |             days_since_last_purchase INTEGER,
 33 |             loyalty_score REAL,
 34 |             complaints INTEGER,
 35 |             payment_type TEXT,
 36 |             tenure_months INTEGER,
 37 |             is_promo_user INTEGER,
 38 |             churn INTEGER
 39 |         );
 40 |         """
 41 |         
 42 |         with engine.connect() as conn:
 43 |             conn.execute(text(create_table_query))
 44 |             conn.commit()
 45 |         
 46 |         print(f"Created database at {DB_PATH} with customers_clean table. nice!")
 47 |         return True
 48 |     
 49 |     except Exception as e:
 50 |         print(f"Error creating database: {e}")
 51 |         return False
 52 | 
 53 | def upsert_clean_data(df):
 54 |     """
 55 |     Insert or update data into customers_clean table
 56 |     """
 57 |     if df is None or df.empty:
 58 |         print("No data to insert, nothing to do :(")
 59 |         return False
 60 |     
 61 |     try:
 62 |         # Create the database and table if they don't exist
 63 |         create_db_and_table()
 64 |         
 65 |         # Create engine
 66 |         engine = create_engine(f"sqlite:///{DB_PATH}")
 67 |         
 68 |         # Insert data with "replace" method (SQLite's upsert)
 69 |         df.to_sql("customers_clean", engine, if_exists="replace", index=False)
 70 |         
 71 |         # Get row count to confirm
 72 |         with engine.connect() as conn:
 73 |             result = conn.execute(text("SELECT COUNT(*) FROM customers_clean"))
 74 |             count = result.scalar()
 75 |         
 76 |         print(f"Successfully saved {count} rows to customers_clean table! data is safe.")
 77 |         return True
 78 |     
 79 |     except Exception as e:
 80 |         print(f"Error inserting data: {e}")
 81 |         return False
 82 | 
 83 | def run_sql(query):
 84 |     """
 85 |     Run SQL query and return results as DataFrame
 86 |     """
 87 |     if not os.path.exists(DB_PATH):
 88 |         print(f"Database not found at {DB_PATH}. need to create it first!")
 89 |         return None
 90 |     
 91 |     try:
 92 |         # Create engine
 93 |         engine = create_engine(f"sqlite:///{DB_PATH}")
 94 |         
 95 |         # Execute query
 96 |         with engine.connect() as conn:
 97 |             result = pd.read_sql_query(query, conn)
 98 |         
 99 |         print(f"Query returned {result.shape[0]} rows. sql magic worked!")
100 |         return result
101 |     
102 |     except Exception as e:
103 |         print(f"Error running query: {e}")
104 |         return None
105 | 
106 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
107 | 
108 | def get_churn_sql_queries():
109 |     """
110 |     Return a dictionary of SQL queries for churn analysis
111 |     """
112 |     return {
113 |         "total_customers": """
114 |             SELECT COUNT(*) AS total_customers 
115 |             FROM customers_clean;
116 |         """,
117 |         
118 |         "churn_rate_overall": """
119 |             SELECT 
120 |                 COUNT(*) AS total_customers,
121 |                 SUM(churn) AS churned_customers,
122 |                 ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct
123 |             FROM customers_clean;
124 |         """,
125 |         
126 |         "churn_by_region": """
127 |             SELECT 
128 |                 region,
129 |                 COUNT(*) AS total_customers,
130 |                 SUM(churn) AS churned_customers,
131 |                 ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct
132 |             FROM customers_clean
133 |             GROUP BY region
134 |             ORDER BY churn_rate_pct DESC;
135 |         """,
136 |         
137 |         "churn_by_payment_type": """
138 |             SELECT 
139 |                 payment_type,
140 |                 COUNT(*) AS total_customers,
141 |                 SUM(churn) AS churned_customers,
142 |                 ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct
143 |             FROM customers_clean
144 |             GROUP BY payment_type
145 |             ORDER BY churn_rate_pct DESC;
146 |         """,
147 |         
148 |         "avg_metrics_by_churn": """
149 |             SELECT 
150 |                 CASE WHEN churn = 1 THEN 'Churned' ELSE 'Retained' END AS customer_status,
151 |                 ROUND(AVG(tenure_months), 1) AS avg_tenure_months,
152 |                 ROUND(AVG(avg_order_value), 2) AS avg_order_value,
153 |                 ROUND(AVG(days_since_last_purchase), 1) AS avg_days_since_purchase,
154 |                 ROUND(AVG(complaints), 2) AS avg_complaints,
155 |                 ROUND(AVG(loyalty_score), 2) AS avg_loyalty_score
156 |             FROM customers_clean
157 |             GROUP BY churn;
158 |         """,
159 |         
160 |         "days_since_purchase_buckets": """
161 |             SELECT 
162 |                 CASE 
163 |                     WHEN days_since_last_purchase BETWEEN 0 AND 30 THEN '0-30 days'
164 |                     WHEN days_since_last_purchase BETWEEN 31 AND 60 THEN '31-60 days'
165 |                     WHEN days_since_last_purchase BETWEEN 61 AND 90 THEN '61-90 days'
166 |                     ELSE 'Over 90 days'
167 |                 END AS days_bucket,
168 |                 COUNT(*) AS total_customers,
169 |                 SUM(churn) AS churned_customers,
170 |                 ROUND(CAST(SUM(churn) AS FLOAT) / COUNT(*) * 100, 2) AS churn_rate_pct
171 |             FROM customers_clean
172 |             GROUP BY days_bucket
173 |             ORDER BY 
174 |                 CASE days_bucket
175 |                     WHEN '0-30 days' THEN 1
176 |                     WHEN '31-60 days' THEN 2
177 |                     WHEN '61-90 days' THEN 3
178 |                     ELSE 4
179 |                 END;
180 |         """
181 |     }
182 | 
183 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
184 | 
185 | # Business Analysis SQL Queries
186 | def get_business_analysis_queries():
187 |     """
188 |     Return a dictionary of SQL queries for business analysis
189 |     """
190 |     return {
191 |         "customer_overview": """
192 |             SELECT 
193 |                 COUNT(*) as total_customers,
194 |                 SUM(CASE WHEN churn = 1 THEN 1 ELSE 0 END) as churned_customers,
195 |                 ROUND(SUM(CASE WHEN churn = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as churn_rate,
196 |                 ROUND(AVG(tenure_months), 1) as avg_tenure_months,
197 |                 ROUND(AVG(total_orders), 1) as avg_orders_per_customer,
198 |                 ROUND(AVG(avg_order_value), 2) as avg_order_value
199 |             FROM customers_clean;
200 |         """,
201 |         
202 |         "customer_segments": """
203 |             WITH customer_segments AS (
204 |                 SELECT 
205 |                     *,
206 |                     CASE 
207 |                         WHEN tenure_months < 6 THEN 'New (0-6 months)'
208 |                         WHEN tenure_months BETWEEN 6 AND 12 THEN 'Recent (6-12 months)'
209 |                         WHEN tenure_months BETWEEN 13 AND 24 THEN 'Established (1-2 years)'
210 |                         ELSE 'Loyal (2+ years)'
211 |                     END AS tenure_segment,
212 |                     CASE 
213 |                         WHEN days_since_last_purchase BETWEEN 0 AND 30 THEN 'Active (0-30 days)'
214 |                         WHEN days_since_last_purchase BETWEEN 31 AND 90 THEN 'Recent (31-90 days)'
215 |                         WHEN days_since_last_purchase BETWEEN 91 AND 180 THEN 'Lapsed (91-180 days)'
216 |                         ELSE 'Inactive (180+ days)'
217 |                     END AS recency_segment,
218 |                     CASE 
219 |                         WHEN total_orders >= 10 AND avg_order_value >= 50 THEN 'High Value'
220 |                         WHEN total_orders >= 10 THEN 'High Frequency'
221 |                         WHEN avg_order_value >= 50 THEN 'Big Spender'
222 |                         ELSE 'Standard'
223 |                     END AS value_segment
224 |                 FROM customers_clean
225 |             )
226 |             
227 |             SELECT 
228 |                 tenure_segment,
229 |                 recency_segment,
230 |                 value_segment,
231 |                 COUNT(*) AS total_customers,
232 |                 SUM(churn) AS churned_customers,
233 |                 ROUND(SUM(churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct
234 |             FROM customer_segments
235 |             GROUP BY tenure_segment, recency_segment, value_segment
236 |             HAVING COUNT(*) >= 5
237 |             ORDER BY churn_rate_pct DESC;
238 |         """,
239 |         
240 |         "rfm_analysis": """
241 |             WITH rfm_scores AS (
242 |                 SELECT 
243 |                     *,
244 |                     CASE 
245 |                         WHEN days_since_last_purchase BETWEEN 0 AND 30 THEN 5
246 |                         WHEN days_since_last_purchase BETWEEN 31 AND 60 THEN 4
247 |                         WHEN days_since_last_purchase BETWEEN 61 AND 90 THEN 3
248 |                         WHEN days_since_last_purchase BETWEEN 91 AND 180 THEN 2
249 |                         ELSE 1
250 |                     END AS recency_score,
251 |                     CASE 
252 |                         WHEN total_orders >= 15 THEN 5
253 |                         WHEN total_orders BETWEEN 10 AND 14 THEN 4
254 |                         WHEN total_orders BETWEEN 5 AND 9 THEN 3
255 |                         WHEN total_orders BETWEEN 2 AND 4 THEN 2
256 |                         ELSE 1
257 |                     END AS frequency_score,
258 |                     CASE 
259 |                         WHEN avg_order_value >= 100 THEN 5
260 |                         WHEN avg_order_value BETWEEN 75 AND 99.99 THEN 4
261 |                         WHEN avg_order_value BETWEEN 50 AND 74.99 THEN 3
262 |                         WHEN avg_order_value BETWEEN 25 AND 49.99 THEN 2
263 |                         ELSE 1
264 |                     END AS monetary_score
265 |                 FROM customers_clean
266 |             ),
267 |             rfm_segments AS (
268 |                 SELECT 
269 |                     *,
270 |                     CASE 
271 |                         WHEN recency_score >= 4 AND frequency_score >= 4 AND monetary_score >= 4 THEN 'Champions'
272 |                         WHEN recency_score >= 4 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'Loyal Customers'
273 |                         WHEN recency_score >= 3 AND frequency_score >= 1 AND monetary_score >= 2 THEN 'Potential Loyalists'
274 |                         WHEN recency_score >= 4 AND frequency_score <= 2 AND monetary_score <= 2 THEN 'New Customers'
275 |                         WHEN recency_score >= 3 AND frequency_score <= 2 AND monetary_score <= 2 THEN 'Promising'
276 |                         WHEN recency_score <= 2 AND frequency_score >= 4 AND monetary_score >= 4 THEN 'At Risk'
277 |                         WHEN recency_score <= 2 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'Need Attention'
278 |                         WHEN recency_score <= 2 AND frequency_score <= 2 AND monetary_score <= 2 THEN 'Hibernating'
279 |                         WHEN recency_score <= 1 AND frequency_score <= 1 AND monetary_score <= 1 THEN 'Lost'
280 |                         ELSE 'Others'
281 |                     END AS rfm_segment
282 |                 FROM rfm_scores
283 |             )
284 |             
285 |             SELECT 
286 |                 rfm_segment,
287 |                 COUNT(*) AS total_customers,
288 |                 SUM(churn) AS churned_customers,
289 |                 ROUND(SUM(churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
290 |                 ROUND(AVG(tenure_months), 1) AS avg_tenure_months,
291 |                 ROUND(AVG(total_orders), 1) AS avg_orders,
292 |                 ROUND(AVG(avg_order_value), 2) AS avg_order_value,
293 |                 ROUND(AVG(days_since_last_purchase), 1) AS avg_days_since_purchase
294 |             FROM rfm_segments
295 |             GROUP BY rfm_segment
296 |             ORDER BY churn_rate_pct DESC;
297 |         """,
298 |         
299 |         "purchase_patterns": """
300 |             SELECT 
301 |                 CASE 
302 |                     WHEN total_orders BETWEEN 1 AND 2 THEN '1-2 orders'
303 |                     WHEN total_orders BETWEEN 3 AND 5 THEN '3-5 orders'
304 |                     WHEN total_orders BETWEEN 6 AND 10 THEN '6-10 orders'
305 |                     WHEN total_orders > 10 THEN '10+ orders'
306 |                     ELSE 'No orders'
307 |                 END AS order_frequency,
308 |                 CASE 
309 |                     WHEN avg_order_value < 25 THEN 'Under $25'
310 |                     WHEN avg_order_value BETWEEN 25 AND 49.99 THEN '$25-$50'
311 |                     WHEN avg_order_value BETWEEN 50 AND 99.99 THEN '$50-$100'
312 |                     ELSE 'Over $100'
313 |                 END AS order_value_bracket,
314 |                 COUNT(*) AS total_customers,
315 |                 SUM(churn) AS churned_customers,
316 |                 ROUND(SUM(churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct
317 |             FROM customers_clean
318 |             GROUP BY order_frequency, order_value_bracket
319 |             ORDER BY churn_rate_pct DESC;
320 |         """,
321 |         
322 |         "demographic_analysis": """
323 |             SELECT 
324 |                 gender,
325 |                 CASE 
326 |                     WHEN age < 25 THEN 'Under 25'
327 |                     WHEN age BETWEEN 25 AND 34 THEN '25-34'
328 |                     WHEN age BETWEEN 35 AND 44 THEN '35-44'
329 |                     WHEN age BETWEEN 45 AND 54 THEN '45-54'
330 |                     WHEN age BETWEEN 55 AND 64 THEN '55-64'
331 |                     ELSE '65+'
332 |                 END AS age_group,
333 |                 region,
334 |                 COUNT(*) AS total_customers,
335 |                 SUM(churn) AS churned_customers,
336 |                 ROUND(SUM(churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct
337 |             FROM customers_clean
338 |             GROUP BY gender, age_group, region
339 |             HAVING COUNT(*) >= 5
340 |             ORDER BY churn_rate_pct DESC;
341 |         """,
342 |         
343 |         "loyalty_analysis": """
344 |             SELECT 
345 |                 CASE 
346 |                     WHEN loyalty_score < 2 THEN 'Very Low (0-1.9)'
347 |                     WHEN loyalty_score BETWEEN 2 AND 3.9 THEN 'Low (2-3.9)'
348 |                     WHEN loyalty_score BETWEEN 4 AND 5.9 THEN 'Medium (4-5.9)'
349 |                     WHEN loyalty_score BETWEEN 6 AND 7.9 THEN 'High (6-7.9)'
350 |                     ELSE 'Very High (8-10)'
351 |                 END AS loyalty_bracket,
352 |                 COUNT(*) AS total_customers,
353 |                 SUM(churn) AS churned_customers,
354 |                 ROUND(SUM(churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
355 |                 ROUND(AVG(tenure_months), 1) AS avg_tenure_months,
356 |                 ROUND(AVG(total_orders), 1) AS avg_orders,
357 |                 ROUND(AVG(avg_order_value), 2) AS avg_order_value
358 |             FROM customers_clean
359 |             GROUP BY loyalty_bracket
360 |             ORDER BY CASE 
361 |                     WHEN loyalty_bracket = 'Very Low (0-1.9)' THEN 1
362 |                     WHEN loyalty_bracket = 'Low (2-3.9)' THEN 2
363 |                     WHEN loyalty_bracket = 'Medium (4-5.9)' THEN 3
364 |                     WHEN loyalty_bracket = 'High (6-7.9)' THEN 4
365 |                     ELSE 5
366 |                 END;
367 |         """,
368 |         
369 |         "complaints_impact": """
370 |             SELECT 
371 |                 CASE 
372 |                     WHEN complaints = 0 THEN 'No Complaints'
373 |                     WHEN complaints = 1 THEN '1 Complaint'
374 |                     WHEN complaints = 2 THEN '2 Complaints'
375 |                     ELSE '3+ Complaints'
376 |                 END AS complaint_group,
377 |                 COUNT(*) AS total_customers,
378 |                 SUM(churn) AS churned_customers,
379 |                 ROUND(SUM(churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct
380 |             FROM customers_clean
381 |             GROUP BY complaint_group
382 |             ORDER BY CASE 
383 |                     WHEN complaint_group = 'No Complaints' THEN 1
384 |                     WHEN complaint_group = '1 Complaint' THEN 2
385 |                     WHEN complaint_group = '2 Complaints' THEN 3
386 |                     ELSE 4
387 |                 END;
388 |         """,
389 |         
390 |         "promo_effectiveness": """
391 |             SELECT 
392 |                 CASE WHEN is_promo_user = 1 THEN 'Promo User' ELSE 'Non-Promo User' END AS promo_status,
393 |                 COUNT(*) AS total_customers,
394 |                 SUM(churn) AS churned_customers,
395 |                 ROUND(SUM(churn) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
396 |                 ROUND(AVG(tenure_months), 1) AS avg_tenure_months,
397 |                 ROUND(AVG(total_orders), 1) AS avg_orders,
398 |                 ROUND(AVG(avg_order_value), 2) AS avg_order_value
399 |             FROM customers_clean
400 |             GROUP BY promo_status;
401 |         """,
402 |         
403 |         "high_risk_customers": """
404 |             SELECT 
405 |                 customer_id,
406 |                 age,
407 |                 gender,
408 |                 region,
409 |                 tenure_months,
410 |                 total_orders,
411 |                 avg_order_value,
412 |                 days_since_last_purchase,
413 |                 loyalty_score,
414 |                 complaints
415 |             FROM customers_clean
416 |             WHERE churn = 0
417 |                 AND days_since_last_purchase > 60
418 |                 AND (
419 |                     complaints > 0
420 |                     OR loyalty_score < 4
421 |                     OR (tenure_months < 6 AND total_orders < 3)
422 |                 )
423 |             ORDER BY days_since_last_purchase DESC, loyalty_score ASC
424 |             LIMIT 100;
425 |         """
426 |     }
427 | 
428 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
429 | 
430 | def create_visualization_from_query(df, viz_type="bar", x_col=None, y_col=None, color_col=None, title=None):
431 |     """
432 |     Create a visualization from SQL query results
433 |     
434 |     Args:
435 |         df: DataFrame with query results
436 |         viz_type: Type of visualization (bar, line, pie, scatter)
437 |         x_col: Column for x-axis
438 |         y_col: Column for y-axis
439 |         color_col: Column for color
440 |         title: Chart title
441 |         
442 |     Returns:
443 |         Plotly figure object
444 |     """
445 |     import plotly.express as px
446 |     
447 |     if df.empty:
448 |         return None
449 |     
450 |     if not x_col:
451 |         x_col = df.columns[0]
452 |     if not y_col:
453 |         y_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
454 |     
455 |     if not title:
456 |         title = f"{y_col} by {x_col}"
457 |     
458 |     if viz_type == "bar":
459 |         fig = px.bar(
460 |             df,
461 |             x=x_col,
462 |             y=y_col,
463 |             color=color_col,
464 |             title=title
465 |         )
466 |     elif viz_type == "line":
467 |         fig = px.line(
468 |             df,
469 |             x=x_col,
470 |             y=y_col,
471 |             color=color_col,
472 |             markers=True,
473 |             title=title
474 |         )
475 |     elif viz_type == "pie":
476 |         fig = px.pie(
477 |             df,
478 |             names=x_col,
479 |             values=y_col,
480 |             title=title
481 |         )
482 |     elif viz_type == "scatter":
483 |         fig = px.scatter(
484 |             df,
485 |             x=x_col,
486 |             y=y_col,
487 |             color=color_col,
488 |             title=title
489 |         )
490 |     else:
491 |         return None
492 |     
493 |     return fig
</content>
</file>
<file><path>src/biz_metrics.py</path>
<content lines="1-397">
  1 | """
  2 | Business metrics for customer churn prediction app.
  3 | """
  4 | import pandas as pd
  5 | import numpy as np
  6 | 
  7 | from .helpers import COST_RETAIN, AVG_FUTURE_ORDERS
  8 | 
  9 | def calculate_revenue_impact(df, churn_prob_col, avg_order_value_col):
 10 |     """
 11 |     Calculate the expected revenue impact of churn
 12 |     """
 13 |     if df is None or df.empty:
 14 |         return {
 15 |             'error': "No data provided for revenue impact calculation."
 16 |         }
 17 |     
 18 |     if churn_prob_col not in df.columns:
 19 |         return {
 20 |             'error': f"Churn probability column '{churn_prob_col}' not found in data."
 21 |         }
 22 |     
 23 |     if avg_order_value_col not in df.columns:
 24 |         return {
 25 |             'error': f"Average order value column '{avg_order_value_col}' not found in data."
 26 |         }
 27 |     
 28 |     try:
 29 |         # Total customers
 30 |         total_customers = len(df)
 31 |         
 32 |         # Expected number of churners
 33 |         expected_churners = df[churn_prob_col].sum()
 34 |         expected_churn_rate = expected_churners / total_customers * 100
 35 |         
 36 |         # Expected revenue loss
 37 |         avg_order_value = df[avg_order_value_col].mean()
 38 |         expected_revenue_loss = expected_churners * avg_order_value * AVG_FUTURE_ORDERS
 39 |         
 40 |         # Per customer metrics
 41 |         avg_expected_loss_per_customer = expected_revenue_loss / total_customers
 42 |         
 43 |         # Results
 44 |         results = {
 45 |             'total_customers': total_customers,
 46 |             'expected_churners': expected_churners,
 47 |             'expected_churn_rate': expected_churn_rate,
 48 |             'avg_order_value': avg_order_value,
 49 |             'expected_revenue_loss': expected_revenue_loss,
 50 |             'avg_expected_loss_per_customer': avg_expected_loss_per_customer
 51 |         }
 52 |         
 53 |         return results
 54 |     
 55 |     except Exception as e:
 56 |         print(f"Error calculating revenue impact: {e}")
 57 |         return {
 58 |             'error': f"Revenue impact calculation failed: {str(e)}"
 59 |         }
 60 | 
 61 | def calculate_targeting_roi(df, churn_prob_col, avg_order_value_col, risk_band_col=None):
 62 |     """
 63 |     Calculate ROI for targeting different risk segments
 64 |     """
 65 |     if df is None or df.empty:
 66 |         return {
 67 |             'error': "No data provided for ROI calculation."
 68 |         }
 69 |     
 70 |     if churn_prob_col not in df.columns:
 71 |         return {
 72 |             'error': f"Churn probability column '{churn_prob_col}' not found in data."
 73 |         }
 74 |     
 75 |     if avg_order_value_col not in df.columns:
 76 |         return {
 77 |             'error': f"Average order value column '{avg_order_value_col}' not found in data."
 78 |         }
 79 |     
 80 |     try:
 81 |         # Make a copy of the data
 82 |         df_calc = df.copy()
 83 |         
 84 |         # Sort by churn probability (descending)
 85 |         df_calc = df_calc.sort_values(churn_prob_col, ascending=False)
 86 |         
 87 |         # Calculate potential loss per customer
 88 |         df_calc['potential_loss'] = df_calc[avg_order_value_col] * AVG_FUTURE_ORDERS
 89 |         
 90 |         # Calculate expected loss (probability × potential loss)
 91 |         df_calc['expected_loss'] = df_calc[churn_prob_col] * df_calc['potential_loss']
 92 |         
 93 |         # Calculate retention cost
 94 |         df_calc['retention_cost'] = COST_RETAIN
 95 |         
 96 |         # Calculate expected benefit (expected loss - retention cost)
 97 |         df_calc['expected_benefit'] = df_calc['expected_loss'] - df_calc['retention_cost']
 98 |         
 99 |         # Calculate cumulative metrics at different targeting thresholds
100 |         results = []
101 |         
102 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
103 |         
104 |         # Calculate total expected loss
105 |         total_expected_loss = df_calc['expected_loss'].sum()
106 |         
107 |         # Get risk bands if available
108 |         has_risk_bands = risk_band_col in df_calc.columns
109 |         
110 |         if has_risk_bands:
111 |             # Calculate metrics for each risk band
112 |             for band in ['High Risk', 'Medium Risk', 'Low Risk']:
113 |                 band_df = df_calc[df_calc[risk_band_col] == band]
114 |                 
115 |                 if len(band_df) == 0:
116 |                     continue
117 |                 
118 |                 customers_count = len(band_df)
119 |                 total_retention_cost = customers_count * COST_RETAIN
120 |                 expected_loss_saved = band_df['expected_loss'].sum()
121 |                 expected_benefit = expected_loss_saved - total_retention_cost
122 |                 percentage_targeted = customers_count / len(df_calc) * 100
123 |                 
124 |                 results.append({
125 |                     'segment': band,
126 |                     'customers_count': customers_count,
127 |                     'percentage_targeted': percentage_targeted,
128 |                     'total_retention_cost': total_retention_cost,
129 |                     'expected_loss_saved': expected_loss_saved,
130 |                     'expected_benefit': expected_benefit,
131 |                     'roi_ratio': expected_loss_saved / total_retention_cost if total_retention_cost > 0 else 0
132 |                 })
133 |         
134 |         # Calculate metrics for different targeting percentages
135 |         percentiles = range(10, 101, 10)
136 |         
137 |         for p in percentiles:
138 |             cutoff_idx = int(len(df_calc) * p / 100)
139 |             targeted_df = df_calc.iloc[:cutoff_idx]
140 |             
141 |             customers_count = len(targeted_df)
142 |             total_retention_cost = customers_count * COST_RETAIN
143 |             expected_loss_saved = targeted_df['expected_loss'].sum()
144 |             expected_benefit = expected_loss_saved - total_retention_cost
145 |             
146 |             results.append({
147 |                 'segment': f"Top {p}%",
148 |                 'customers_count': customers_count,
149 |                 'percentage_targeted': p,
150 |                 'total_retention_cost': total_retention_cost,
151 |                 'expected_loss_saved': expected_loss_saved,
152 |                 'expected_benefit': expected_benefit,
153 |                 'roi_ratio': expected_loss_saved / total_retention_cost if total_retention_cost > 0 else 0,
154 |                 'percent_of_total_loss': expected_loss_saved / total_expected_loss * 100 if total_expected_loss > 0 else 0
155 |             })
156 |         
157 |         return {
158 |             'by_segment': results,
159 |             'total_expected_loss': total_expected_loss
160 |         }
161 |     
162 |     except Exception as e:
163 |         print(f"Error calculating targeting ROI: {e}")
164 |         return {
165 |             'error': f"ROI calculation failed: {str(e)}"
166 |         }
167 |     
168 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
169 | 
170 | 
171 | def get_retention_playbook_by_risk(risk_band):
172 |     """
173 |     Get retention playbook recommendations based on risk band
174 |     """
175 |     if risk_band == "High Risk":
176 |         actions = [
177 |             "Send personalized email with 20% discount coupon valid for 7 days",
178 |             "Follow up with a phone call from customer service within 48 hours",
179 |             "Offer free expedited shipping on next order",
180 |             "Add loyalty points boost (2x points for next 30 days)",
181 |             "Invite to exclusive product preview or early access"
182 |         ]
183 |     elif risk_band == "Medium Risk":
184 |         actions = [
185 |             "Send email with 10% discount coupon valid for 14 days",
186 |             "Recommend products based on previous purchases",
187 |             "Send reminder about loyalty points balance and upcoming expiration",
188 |             "Share new product announcements in their favorite categories",
189 |             "Ask for feedback or product review with small incentive"
190 |         ]
191 |     else:  # Low Risk
192 |         actions = [
193 |             "Include in regular marketing newsletters",
194 |             "Maintain standard loyalty program communications",
195 |             "Periodic engagement with seasonal promotions",
196 |             "Anniversary or birthday special offers",
197 |             "Invite to refer friends with dual incentives"
198 |         ]
199 |     
200 |     return actions
201 | 
202 | def get_targeting_recommendations(roi_results):
203 |     """
204 |     Get recommendations based on ROI calculations
205 |     """
206 |     if 'error' in roi_results:
207 |         return [
208 |             "Couldn't calculate targeting recommendations due to an error.",
209 |             "Please ensure your data includes churn probabilities and order values."
210 |         ]
211 |     
212 |     recommendations = []
213 |     
214 |     # Get segment data
215 |     segments = roi_results.get('by_segment', [])
216 |     total_expected_loss = roi_results.get('total_expected_loss', 0)
217 |     
218 |     # Find best ROI segment
219 |     best_roi_segment = None
220 |     best_roi = 0
221 |     
222 |     for segment in segments:
223 |         if segment['roi_ratio'] > best_roi:
224 |             best_roi = segment['roi_ratio']
225 |             best_roi_segment = segment
226 |     
227 |     if best_roi_segment:
228 |         if 'High Risk' in best_roi_segment.get('segment', ''):
229 |             recommendations.append(
230 |                 f"Focus on High Risk customers first - each $1 spent on retention saves ${best_roi:.2f} in revenue!"
231 |             )
232 |         elif 'Top' in best_roi_segment.get('segment', ''):
233 |             recommendations.append(
234 |                 f"Target the {best_roi_segment['segment']} of customers for best ROI - each $1 spent saves ${best_roi:.2f}!"
235 |             )
236 |     
237 |     # Find optimal targeting percentage
238 |     optimal_segment = None
239 |     max_benefit = 0
240 |     
241 |     for segment in segments:
242 |         if 'Top' in segment.get('segment', '') and segment['expected_benefit'] > max_benefit:
243 |             max_benefit = segment['expected_benefit']
244 |             optimal_segment = segment
245 |     
246 |     if optimal_segment:
247 |         recommendations.append(
248 |             f"Optimal targeting strategy: {optimal_segment['segment']} of customers (saves ${optimal_segment['expected_benefit']:.2f})"
249 |         )
250 |     
251 |     # Add general recommendations
252 |     recommendations.extend([
253 |         f"Total expected loss from churn: ${total_expected_loss:.2f} - this is what we're trying to prevent!",
254 |         "Customize retention offers based on customer value and risk level for best results",
255 |         "Track campaign performance and adjust targeting thresholds over time"
256 |     ])
257 |     
258 |     return recommendations
259 | 
260 | def generate_business_report(df, churn_predictions, feature_importance, cost_benefit_df=None):
261 |     """
262 |     Generate a business report with insights and recommendations
263 |     """
264 |     if df is None or df.empty:
265 |         return "No data available for business report."
266 |     
267 |     # Calculate basic metrics
268 |     total_customers = len(df)
269 |     churn_rate = df['churn'].mean() * 100 if 'churn' in df.columns else None
270 |     
271 |     # Start building the report
272 |     report = "# Customer Churn Business Report\n\n"
273 |     
274 |     # Current situation
275 |     report += "## Current Situation\n\n"
276 |     
277 |     if churn_rate is not None:
278 |         report += f"- Current churn rate: **{churn_rate:.1f}%** of customers\n"
279 |     
280 |     # Get average order value and tenure
281 |     avg_order = df['avg_order_value'].mean() if 'avg_order_value' in df.columns else None
282 |     avg_tenure = df['tenure_months'].mean() if 'tenure_months' in df.columns else None
283 |     
284 |     if avg_order is not None:
285 |         report += f"- Average order value: **${avg_order:.2f}**\n"
286 |     
287 |     if avg_tenure is not None:
288 |         report += f"- Average customer tenure: **{avg_tenure:.1f} months**\n"
289 |     
290 |     # Risky segments
291 |     report += "\n## High-Risk Customer Segments\n\n"
292 |     
293 |     # By region if available
294 |     if 'region' in df.columns:
295 |         churn_by_region = df.groupby('region')['churn'].mean().sort_values(ascending=False)
296 |         highest_region = churn_by_region.index[0]
297 |         highest_region_rate = churn_by_region.iloc[0] * 100
298 |         
299 |         report += f"- **{highest_region} region** has highest churn rate at {highest_region_rate:.1f}%\n"
300 |     
301 |     # By payment type if available
302 |     if 'payment_type' in df.columns:
303 |         churn_by_payment = df.groupby('payment_type')['churn'].mean().sort_values(ascending=False)
304 |         highest_payment = churn_by_payment.index[0]
305 |         highest_payment_rate = churn_by_payment.iloc[0] * 100
306 |         
307 |         report += f"- **{highest_payment} payment** users churn at {highest_payment_rate:.1f}%\n"
308 |     
309 |     # By tenure buckets if available
310 |     if 'tenure_months' in df.columns:
311 |         df['tenure_bucket'] = pd.cut(
312 |             df['tenure_months'], 
313 |             bins=[0, 6, 12, 24, 36, float('inf')],
314 |             labels=['0-6 months', '7-12 months', '1-2 years', '2-3 years', '3+ years']
315 |         )
316 |         churn_by_tenure = df.groupby('tenure_bucket')['churn'].mean().sort_values(ascending=False)
317 |         highest_tenure = churn_by_tenure.index[0]
318 |         highest_tenure_rate = churn_by_tenure.iloc[0] * 100
319 |         
320 |         report += f"- Customers in **{highest_tenure}** tenure bracket churn at {highest_tenure_rate:.1f}%\n"
321 |     
322 |     # Key drivers section
323 |     report += "\n## Top 5 Churn Drivers\n\n"
324 |     
325 |     # Use feature importance if available
326 |     if feature_importance and len(feature_importance) > 0:
327 |         for i, feature in enumerate(feature_importance[:5], 1):
328 |             name = feature.get('feature', '')
329 |             explanation = feature.get('explanation', '')
330 |             
331 |             report += f"{i}. **{name}**: {explanation}\n"
332 |     else:
333 |         report += "Feature importance data not available.\n"
334 | 
335 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
336 | 
337 |     # Targeting plan
338 |     report += "\n## Targeting Plan\n\n"
339 |     
340 |     if cost_benefit_df is not None and not cost_benefit_df.empty:
341 |         # Find optimal targeting percentage
342 |         optimal_row = cost_benefit_df.loc[cost_benefit_df['net_benefit'].idxmax()]
343 |         optimal_percent = optimal_row['targeting_percent']
344 |         optimal_benefit = optimal_row['net_benefit']
345 |         optimal_customers = optimal_row['customers_targeted']
346 |         optimal_churners = optimal_row['churners_caught']
347 |         optimal_churners_pct = optimal_row['churners_caught_percent']
348 |         
349 |         report += f"- **Optimal strategy**: Target top {optimal_percent:.0f}% highest-risk customers\n"
350 |         report += f"- This means focusing on **{optimal_customers:.0f} customers**\n"
351 |         report += f"- Expected to save **${optimal_benefit:.2f}** in revenue\n"
352 |         report += f"- Would catch **{optimal_churners:.0f} churners** ({optimal_churners_pct:.1f}% of all churners)\n"
353 |     else:
354 |         report += "Cost-benefit analysis data not available.\n"
355 |     
356 |     # Action items
357 |     report += "\n## Recommended Actions\n\n"
358 |     
359 |     # High risk actions
360 |     report += "### For High-Risk Customers:\n"
361 |     report += "1. Send personalized email with 20% discount coupon valid for 7 days\n"
362 |     report += "2. Follow up with a phone call from customer service within 48 hours\n"
363 |     report += "3. Offer free expedited shipping on next order\n"
364 |     
365 |     # Medium risk actions
366 |     report += "\n### For Medium-Risk Customers:\n"
367 |     report += "1. Send email with 10% discount coupon valid for 14 days\n"
368 |     report += "2. Recommend products based on previous purchases\n"
369 |     report += "3. Send reminder about loyalty points balance\n"
370 |     
371 |     # Product/service improvements
372 |     report += "\n### Product/Service Improvements:\n"
373 |     
374 |     # Look at complaints if available
375 |     if 'complaints' in df.columns and df['complaints'].sum() > 0:
376 |         report += "1. Address common customer complaints to improve retention\n"
377 |     else:
378 |         report += "1. Review customer feedback for product improvement opportunities\n"
379 |     
380 |     report += "2. Consider loyalty program adjustments for better engagement\n"
381 |     report += "3. Improve onboarding for new customers (first 6 months critical)\n"
382 |     
383 |     # 30-day roadmap
384 |     report += "\n## Next 30 Days Roadmap\n\n"
385 |     report += "1. **Week 1**: Launch high-risk customer retention campaign\n"
386 |     report += "2. **Week 2**: Begin medium-risk customer engagement\n"
387 |     report += "3. **Week 3**: Analyze initial campaign results and adjust\n"
388 |     report += "4. **Week 4**: Prepare follow-up actions and long-term strategy\n"
389 |     
390 |     # Final notes
391 |     report += "\n## Notes\n\n"
392 |     report += "- This is an initial analysis based on available data\n"
393 |     report += "- Campaign effectiveness should be measured and tactics adjusted\n"
394 |     report += "- Consider A/B testing different retention offers\n"
395 |     report += "- Long-term product/service improvements will have most sustainable impact\n"
396 |     
397 |     return report
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
../bob_task_may-16-2026_5-47-09-pm.md

# VSCode Open Tabs
README.md,../bob_task_may-16-2026_5-47-09-pm.md,LICENSE,app.py,.gitignore,tests/smoke_tests.py,src/biz_metrics.py,src/data_prep.py,src/eda_utils.py,src/helpers.py,pages/1_Data_Exploration.py,pages/3_Customer_Retention.py,src/sql_utils.py,data/generate_synthetic_data.py,notebooks/eda_playground.ipynb,pages/4_Business_Insights.py,pages/2_Customer_Groups.py,requirements.txt

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T12:40:36.617Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.09

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Now I have a comprehensive understanding of the existing project. Let me create a detailed scalable architecture plan for the Customer Churn Analytics Dashboard.

<update_todo_list>
<todos>
[-] Analyze existing project structure and components
[ ] Design comprehensive scalable architecture document
[ ] Create detailed folder structure specification
[ ] Document component communication patterns
[ ] Design ML pipeline architecture
[ ] Create system architecture diagrams
[ ] Document deployment and scaling strategies
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
../bob_task_may-16-2026_5-47-09-pm.md

# VSCode Open Tabs
README.md,../bob_task_may-16-2026_5-47-09-pm.md,LICENSE,app.py,.gitignore,tests/smoke_tests.py,src/biz_metrics.py,src/data_prep.py,src/eda_utils.py,src/helpers.py,pages/1_Data_Exploration.py,pages/3_Customer_Retention.py,src/sql_utils.py,data/generate_synthetic_data.py,notebooks/eda_playground.ipynb,pages/4_Business_Insights.py,pages/2_Customer_Groups.py,requirements.txt

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T12:40:43.473Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.19

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Analyze existing project structure and components | In Progress |
| 2 | Design comprehensive scalable architecture document | Pending |
| 3 | Create detailed folder structure specification | Pending |
| 4 | Document component communication patterns | Pending |
| 5 | Design ML pipeline architecture | Pending |
| 6 | Create system architecture diagrams | Pending |
| 7 | Document deployment and scaling strategies | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<ask_followup_question>
<question>I've analyzed the existing Customer Churn Analytics Dashboard. Before I design the scalable architecture, I'd like to clarify a few requirements:

1. **Machine Learning Integration**: Should the architecture include real-time ML model training and prediction capabilities, or batch processing?

2. **Scale Target**: What's the expected data volume and user concurrency? (e.g., thousands of customers, 10-50 concurrent users, or enterprise-scale with millions of records?)

3. **Deployment Environment**: Are you planning to deploy this on cloud infrastructure (AWS, Azure, GCP), on-premises, or as a containerized solution?

4. **Additional Features**: Should the architecture include:
   - Real-time churn prediction API endpoints?
   - Automated model retraining pipeline?
   - Advanced customer segmentation with clustering algorithms?
   - A/B testing framework for retention strategies?</question>
<follow_up>
<suggest>Real-time ML predictions, medium scale (10K-100K customers, 10-20 users), cloud deployment (AWS/Azure), include all advanced features</suggest>
<suggest>Batch processing ML, small-medium scale (1K-50K customers, 5-10 users), containerized deployment (Docker), focus on core churn prediction and segmentation</suggest>
<suggest>Hybrid approach with both real-time and batch ML, enterprise scale (100K+ customers, 50+ users), multi-cloud deployment, include all features plus API layer</suggest>
<suggest>Keep it simple - batch ML processing, small scale (up to 10K customers, 1-5 users), local/single-server deployment, core features only</suggest>
</follow_up>
</ask_followup_question>

---

**User:**

[ask_followup_question for 'I've analyzed the existing Customer Churn Analytics Dashboard. Before I design the scalable architecture, I'd like to clarify a few requirements:

1. **Machine Learning Integration**: Should the architecture include real-time ML model training and prediction capabilities, or batch processing?

2. **Scale Target**: What's the expected data volume and user concurrency? (e.g., thousands of customers, 10-50 concurrent users, or enterprise-scale with millions of records?)

3. **Deployment Environment**: Are you planning to deploy this on cloud infrastructure (AWS, Azure, GCP), on-premises, or as a containerized solution?

4. **Additional Features**: Should the architecture include:
   - Real-time churn prediction API endpoints?
   - Automated model retraining pipeline?
   - Advanced customer segmentation with clustering algorithms?
   - A/B testing framework for retention strategies?'] Result:
<answer>
Real-time ML predictions, medium scale (10K-100K customers, 10-20 users), cloud deployment (AWS/Azure), include all advanced features
</answer>
<environment_details>
# VSCode Visible Files
../bob_task_may-16-2026_5-47-09-pm.md

# VSCode Open Tabs
README.md,../bob_task_may-16-2026_5-47-09-pm.md,LICENSE,app.py,.gitignore,tests/smoke_tests.py,src/biz_metrics.py,src/data_prep.py,src/eda_utils.py,src/helpers.py,pages/1_Data_Exploration.py,pages/3_Customer_Retention.py,src/sql_utils.py,data/generate_synthetic_data.py,notebooks/eda_playground.ipynb,pages/4_Business_Insights.py,pages/2_Customer_Groups.py,requirements.txt

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T12:41:18.595Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.29

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Analyze existing project structure and components | In Progress |
| 2 | Design comprehensive scalable architecture document | Pending |
| 3 | Create detailed folder structure specification | Pending |
| 4 | Document component communication patterns | Pending |
| 5 | Design ML pipeline architecture | Pending |
| 6 | Create system architecture diagrams | Pending |
| 7 | Document deployment and scaling strategies | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Perfect! I'll now design a comprehensive scalable architecture for a Customer Churn Analytics Dashboard with real-time ML predictions, medium scale (10K-100K customers, 10-20 concurrent users), cloud deployment, and all advanced features.

<update_todo_list>
<todos>
[x] Analyze existing project structure and components
[-] Design comprehensive scalable architecture document
[ ] Create detailed folder structure specification
[ ] Document component communication patterns
[ ] Design ML pipeline architecture
[ ] Create system architecture diagrams
[ ] Document deployment and scaling strategies
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
../bob_task_may-16-2026_5-47-09-pm.md

# VSCode Open Tabs
README.md,../bob_task_may-16-2026_5-47-09-pm.md,LICENSE,app.py,.gitignore,tests/smoke_tests.py,src/biz_metrics.py,src/data_prep.py,src/eda_utils.py,src/helpers.py,pages/1_Data_Exploration.py,pages/3_Customer_Retention.py,src/sql_utils.py,data/generate_synthetic_data.py,notebooks/eda_playground.ipynb,pages/4_Business_Insights.py,pages/2_Customer_Groups.py,requirements.txt

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T12:41:29.244Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.40

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Analyze existing project structure and components | Completed |
| 2 | Design comprehensive scalable architecture document | In Progress |
| 3 | Create detailed folder structure specification | Pending |
| 4 | Document component communication patterns | Pending |
| 5 | Design ML pipeline architecture | Pending |
| 6 | Create system architecture diagrams | Pending |
| 7 | Document deployment and scaling strategies | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I'll create a comprehensive scalable architecture document for the Customer Churn Analytics Dashboard.

<write_to_file>
<path>docs/SCALABLE_ARCHITECTURE.md</path>
<content>
# Scalable Architecture for Customer Churn Analytics Dashboard

## Executive Summary

This document outlines a comprehensive, production-ready architecture for a Customer Churn Analytics Dashboard built with Streamlit, Python, SQLite/PostgreSQL, and Machine Learning. The architecture supports real-time ML predictions, handles 10K-100K customers with 10-20 concurrent users, and is designed for cloud deployment (AWS/Azure).

**Key Features:**
- Real-time churn prediction with ML models
- Advanced customer segmentation using clustering algorithms
- Automated model retraining pipeline
- RESTful API for external integrations
- Scalable data processing with caching
- Comprehensive monitoring and logging
- A/B testing framework for retention strategies

---

## Table of Contents

1. [System Architecture Overview](#system-architecture-overview)
2. [Detailed Folder Structure](#detailed-folder-structure)
3. [Component Architecture](#component-architecture)
4. [Data Flow and Communication](#data-flow-and-communication)
5. [Machine Learning Pipeline](#machine-learning-pipeline)
6. [API Layer Design](#api-layer-design)
7. [Database Architecture](#database-architecture)
8. [Deployment Strategy](#deployment-strategy)
9. [Scaling Considerations](#scaling-considerations)
10. [Security and Compliance](#security-and-compliance)

---

## 1. System Architecture Overview

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                           │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │  Streamlit UI    │  │   REST API       │  │  Admin Dashboard │ │
│  │  (Dashboard)     │  │  (FastAPI)       │  │   (Monitoring)   │ │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘ │
└───────────┼─────────────────────┼─────────────────────┼───────────┘
            │                     │                     │
┌───────────┼─────────────────────┼─────────────────────┼───────────┐
│           │         APPLICATION LAYER                 │           │
│  ┌────────▼─────────┐  ┌────────▼─────────┐  ┌───────▼────────┐ │
│  │  Business Logic  │  │  API Controllers │  │  Auth Service  │ │
│  │   - Analytics    │  │  - Endpoints     │  │  - JWT Tokens  │ │
│  │   - Metrics      │  │  - Validation    │  │  - RBAC        │ │
│  └────────┬─────────┘  └────────┬─────────┘  └───────┬────────┘ │
└───────────┼─────────────────────┼─────────────────────┼───────────┘
            │                     │                     │
┌───────────┼─────────────────────┼─────────────────────┼───────────┐
│           │         SERVICE LAYER                     │           │
│  ┌────────▼─────────┐  ┌────────▼─────────┐  ┌───────▼────────┐ │
│  │  ML Service      │  │  Data Service    │  │  Cache Service │ │
│  │  - Prediction    │  │  - ETL Pipeline  │  │  - Redis       │ │
│  │  - Training      │  │  - Validation    │  │  - Session     │ │
│  │  - Segmentation  │  │  - Transform     │  │  - Results     │ │
│  └────────┬─────────┘  └────────┬─────────┘  └───────┬────────┘ │
└───────────┼─────────────────────┼─────────────────────┼───────────┘
            │                     │                     │
┌───────────┼─────────────────────┼─────────────────────┼───────────┐
│           │         DATA LAYER                        │           │
│  ┌────────▼─────────┐  ┌────────▼─────────┐  ┌───────▼────────┐ │
│  │  PostgreSQL DB   │  │  Model Registry  │  │  Object Store  │ │
│  │  - Customer Data │  │  - MLflow        │  │  - S3/Blob     │ │
│  │  - Predictions   │  │  - Versions      │  │  - Raw Data    │ │
│  │  - Metrics       │  │  - Metadata      │  │  - Exports     │ │
│  └──────────────────┘  └──────────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │  Message Queue   │  │  Monitoring      │  │  CI/CD Pipeline  │ │
│  │  - Celery/RabbitMQ│ │  - Prometheus    │  │  - GitHub Actions│ │
│  │  - Task Queue    │  │  - Grafana       │  │  - Docker        │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Architecture Principles

1. **Separation of Concerns**: Clear boundaries between presentation, business logic, and data layers
2. **Scalability**: Horizontal scaling through containerization and load balancing
3. **Modularity**: Independent, loosely-coupled components
4. **Observability**: Comprehensive logging, monitoring, and alerting
5. **Security**: Authentication, authorization, and data encryption
6. **Performance**: Caching strategies and async processing
7. **Maintainability**: Clean code, documentation, and testing

---

## 2. Detailed Folder Structure

```
customer-churn-dashboard/
│
├── app.py                          # Main Streamlit application entry point
├── api_server.py                   # FastAPI server entry point
├── requirements.txt                # Python dependencies
├── requirements-dev.txt            # Development dependencies
├── setup.py                        # Package setup configuration
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── README.md                       # Project documentation
├── LICENSE                         # License file
│
├── config/                         # Configuration files
│   ├── __init__.py
│   ├── settings.py                 # Application settings (env-based)
│   ├── database.py                 # Database configuration
│   ├── logging.py                  # Logging configuration
│   ├── ml_config.yaml              # ML model hyperparameters
│   └── feature_config.yaml         # Feature engineering config
│
├── src/                            # Source code modules
│   ├── __init__.py
│   │
│   ├── core/                       # Core utilities and helpers
│   │   ├── __init__.py
│   │   ├── constants.py            # Application constants
│   │   ├── exceptions.py           # Custom exceptions
│   │   ├── logging.py              # Logging utilities
│   │   └── validators.py           # Data validators
│   │
│   ├── data/                       # Data layer
│   │   ├── __init__.py
│   │   ├── database.py             # Database connection manager
│   │   ├── models.py               # SQLAlchemy ORM models
│   │   ├── repositories.py         # Data access layer (Repository pattern)
│   │   ├── schemas.py              # Pydantic schemas for validation
│   │   └── migrations/             # Database migrations (Alembic)
│   │       ├── versions/
│   │       └── env.py
│   │
│   ├── etl/                        # ETL Pipeline
│   │   ├── __init__.py
│   │   ├── extractors.py           # Data extraction from sources
│   │   ├── transformers.py         # Data transformation logic
│   │   ├── loaders.py              # Data loading to database
│   │   ├── validators.py           # Data quality checks
│   │   └── pipeline.py             # ETL orchestration
│   │
│   ├── features/                   # Feature Engineering
│   │   ├── __init__.py
│   │   ├── base.py                 # Base feature transformer
│   │   ├── numeric.py              # Numeric feature engineering
│   │   ├── categorical.py          # Categorical feature engineering
│   │   ├── temporal.py             # Time-based features
│   │   ├── rfm.py                  # RFM segmentation features
│   │   └── aggregations.py         # Aggregated features
│   │
│   ├── ml/                         # Machine Learning
│   │   ├── __init__.py
│   │   │
│   │   ├── models/                 # ML Models
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Base model interface
│   │   │   ├── churn_predictor.py  # Churn prediction model
│   │   │   ├── segmentation.py     # Customer segmentation (K-Means, DBSCAN)
│   │   │   ├── lifetime_value.py   # CLV prediction model
│   │   │   └── ensemble.py         # Ensemble models
│   │   │
│   │   ├── training/               # Model Training
│   │   │   ├── __init__.py
│   │   │   ├──trainer.py           # Training orchestrator
│   │   │   ├── hyperopt.py         # Hyperparameter optimization
│   │   │   ├── cross_validation.py # Cross-validation utilities
│   │   │   └── evaluation.py       # Model evaluation metrics
│   │   │
│   │   ├── inference/              # Model Inference
│   │   │   ├── __init__.py
│   │   │   ├── predictor.py        # Real-time prediction service
│   │   │   ├── batch_predictor.py  # Batch prediction service
│   │   │   └── model_loader.py     # Model loading utilities
│   │   │
│   │   └── registry/               # Model Registry
│   │       ├── __init__.py
│   │       ├── mlflow_registry.py  # MLflow integration
│   │       ├── model_versioning.py # Model version management
│   │       └── deployment.py       # Model deployment utilities
│   │
│   ├── analytics/                  # Business Analytics
│   │   ├── __init__.py
│   │   ├── metrics.py              # Business metrics calculation
│   │   ├── cohort_analysis.py      # Cohort analysis
│   │   ├── retention_analysis.py   # Retention analysis
│   │   ├── segmentation_analysis.py# Segmentation insights
│   │   └── roi_calculator.py       # ROI calculations
│   │
│   ├── visualization/              # Visualization Components
│   │   ├── __init__.py
│   │   ├── charts.py               # Chart generation utilities
│   │   ├── plotly_components.py    # Plotly-specific components
│   │   ├── streamlit_components.py # Custom Streamlit components
│   │   └── dashboard_layouts.py    # Dashboard layout templates
│   │
│   ├── api/                        # API Layer
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application
│   │   ├── dependencies.py         # API dependencies
│   │   ├── middleware.py           # Custom middleware
│   │   │
│   │   ├── routes/                 # API Routes
│   │   │   ├── __init__.py
│   │   │   ├── auth.py             # Authentication endpoints
│   │   │   ├── customers.py        # Customer data endpoints
│   │   │   ├── predictions.py      # ML prediction endpoints
│   │   │   ├── analytics.py        # Analytics endpoints
│   │   │   └── health.py           # Health check endpoints
│   │   │
│   │   └── auth/                   # Authentication
│   │       ├── __init__.py
│   │       ├── jwt_handler.py      # JWT token handling
│   │       ├── permissions.py      # Role-based access control
│   │       └── oauth.py            # OAuth integration
│   │
│   ├── services/                   # Business Services
│   │   ├── __init__.py
│   │   ├── customer_service.py     # Customer business logic
│   │   ├── prediction_service.py   # Prediction business logic
│   │   ├── analytics_service.py    # Analytics business logic
│   │   ├── notification_service.py # Notification handling
│   │   └── export_service.py       # Data export functionality
│   │
│   └── utils/                      # Utilities
│       ├── __init__.py
│       ├── cache.py                # Caching utilities (Redis)
│       ├── file_handlers.py        # File I/O operations
│       ├── date_utils.py           # Date/time utilities
│       ├── encryption.py           # Data encryption utilities
│       └── monitoring.py           # Application monitoring
│
├── pages/                          # Streamlit Pages
│   ├── __init__.py
│   ├── 1_📊_Data_Exploration.py    # Enhanced data exploration
│   ├── 2_👥_Customer_Segments.py   # Advanced segmentation
│   ├── 3_🎯_Churn_Prediction.py    # Real-time predictions
│   ├── 4_📈_Retention_Analysis.py  # Retention insights
│   ├── 5_💰_Business_Impact.py     # ROI and business metrics
│   ├── 6_🧪_AB_Testing.py          # A/B testing framework
│   └── 7_⚙️_Model_Management.py    # ML model management
│
├── data/                           # Data Storage
│   ├── raw/                        # Raw data files
│   ├── processed/                  # Processed data
│   ├── external/                   # External data sources
│   ├── models/                     # Serialized ML models
│   │   ├── churn/                  # Churn prediction models
│   │   ├── segmentation/           # Segmentation models
│   │   └── encoders/               # Feature encoders/scalers
│   └── exports/                    # Generated reports/exports
│
├── notebooks/                      # Jupyter Notebooks
│   ├── 01_data_exploration.ipynb   # Initial data analysis
│   ├── 02_feature_engineering.ipynb# Feature development
│   ├── 03_model_development.ipynb  # Model experimentation
│   ├── 04_model_evaluation.ipynb   # Model performance analysis
│   └── 05_business_analysis.ipynb  # Business insights
│
├── tests/                          # Test Suite
│   ├── __init__.py
│   ├── conftest.py                 # Pytest configuration
│   │
│   ├── unit/                       # Unit tests
│   │   ├── test_data/
│   │   ├── test_ml/
│   │   ├── test_analytics/
│   │   └── test_api/
│   │
│   ├── integration/                # Integration tests
│   │   ├── test_etl_pipeline.py
│   │   ├── test_ml_pipeline.py
│   │   └── test_api_integration.py
│   │
│   └── e2e/                        # End-to-end tests
│       ├── test_dashboard.py
│       └── test_api_workflows.py
│
├── scripts/                        # Utility Scripts
│   ├── setup_database.py           # Database initialization
│   ├── generate_sample_data.py     # Sample data generation
│   ├── train_models.py             # Model training script
│   ├── deploy_models.py            # Model deployment script
│   ├── backup_data.py              # Data backup utilities
│   └── monitoring_setup.py         # Monitoring configuration
│
├── docker/                         # Docker Configuration
│   ├── Dockerfile                  # Main application container
│   ├── Dockerfile.api              # API server container
│   ├── Dockerfile.worker           # Background worker container
│   ├── docker-compose.yml          # Local development setup
│   ├── docker-compose.prod.yml     # Production setup
│   └── nginx.conf                  # Nginx configuration
│
├── deployment/                     # Deployment Configuration
│   ├── kubernetes/                 # K8s manifests
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   ├── secrets.yaml
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   │
│   ├── terraform/                  # Infrastructure as Code
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── modules/
│   │
│   └── helm/                       # Helm charts
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│
├── monitoring/                     # Monitoring Configuration
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── provisioning/
│   └── alerts/
│       └── alerting_rules.yml
│
└── docs/                           # Documentation
    ├── api/                        # API documentation
    ├── architecture/               # Architecture diagrams
    ├── deployment/                 # Deployment guides
    ├── user_guide/                 # User documentation
    └── development/                # Development guides
```

---

## 3. Component Architecture

### 3.1 Frontend Dashboard Structure

The Streamlit dashboard is organized into modular pages with shared components:

```python
# Enhanced page structure with real-time capabilities
class DashboardPage:
    def __init__(self):
        self.cache_manager = CacheManager()
        self.auth_service = AuthService()
        self.analytics_service = AnalyticsService()
    
    def render(self):
        # Authentication check
        if not self.auth_service.is_authenticated():
            self.render_login()
            return
        
        # Real-time data refresh
        self.setup_auto_refresh()
        
        # Page content
        self.render_content()
    
    def setup_auto_refresh(self):
        # Auto-refresh every 30 seconds for real-time data
        st.rerun()
```

### 3.2 Backend Data Processing Flow

```python
# Data processing pipeline with real-time capabilities
class DataProcessingPipeline:
    def __init__(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.validator = DataValidator()
        self.loader = DataLoader()
        self.ml_service = MLService()
    
    async def process_realtime_data(self, customer_data):
        # Extract and validate
        validated_data = await self.validator.validate(customer_data)
        
        # Transform features
        features = await self.transformer.transform(validated_data)
        
        # Generate predictions
        predictions = await self.ml_service.predict(features)
        
        # Store results
        await self.loader.store_predictions(predictions)
        
        return predictions
```

### 3.3 Machine Learning Service Architecture

```python
# ML service with model registry integration
class MLService:
    def __init__(self):
        self.model_registry = MLflowRegistry()
        self.feature_store = FeatureStore()
        self.prediction_cache = PredictionCache()
    
    async def predict_churn(self, customer_id: str):
        # Check cache first
        cached_prediction = await self.prediction_cache.get(customer_id)
        if cached_prediction:
            return cached_prediction
        
        # Load latest model
        model = await self.model_registry.get_latest_model('churn_predictor')
        
        # Get features
        features = await self.feature_store.get_features(customer_id)
        
        # Make prediction
        prediction = model.predict(features)
        
        # Cache result
        await self.prediction_cache.set(customer_id, prediction, ttl=3600)
        
        return prediction
```

---

## 4. Data Flow and Communication

### 4.1 Real-time Data Flow

```mermaid
graph TD
    A[Customer Data Input] --> B[Data Validation]
    B --> C[Feature Engineering]
    C --> D[ML Prediction Service]
    D --> E[Prediction Cache]
    E --> F[Dashboard Update]
    
    G[Batch Data Processing] --> H[Model Training]
    H --> I[Model Registry]
    I --> D
    
    J[External APIs] --> K[Message Queue]
    K --> L[Background Workers]
    L --> B
```

### 4.2 Component Communication Patterns

#### Synchronous Communication
- **Dashboard ↔ API**: REST API calls for real-time data
- **API ↔ Database**: Direct database queries for CRUD operations
- **API ↔ ML Service**: Direct calls for predictions

#### Asynchronous Communication
- **ETL Pipeline**: Message queue for batch processing
- **Model Training**: Background tasks for model updates
- **Notifications**: Event-driven alerts and reports

### 4.3 Data Storage Strategy

```python
# Multi-tier data storage approach
class DataStorageManager:
    def __init__(self):
        self.primary_db = PostgreSQLDatabase()      # Transactional data
        self.cache = RedisCache()                   # Session & predictions
        self.object_store = S3ObjectStore()         # Raw data & models
        self.time_series_db = InfluxDB()           # Metrics & monitoring
    
    async def store_customer_data(self, data):
        # Primary storage
        await self.primary_db.insert(data)
        
        # Cache frequently accessed data
        await self.cache.set_customer_profile(data.customer_id, data)
        
        # Archive raw data
        await self.object_store.upload_raw_data(data)
```

---

## 5. Machine Learning Pipeline

### 5.1 ML Pipeline Architecture

```mermaid
graph LR
    A[Raw Data] --> B[Data Validation]
    B --> C[Feature Engineering]
    C --> D[Feature Store]
    D --> E[Model Training]
    E --> F[Model Evaluation]
    F --> G[Model Registry]
    G --> H[Model Deployment]
    H --> I[Prediction Service]
    
    J[Monitoring] --> K[Model Drift Detection]
    K --> L[Retraining Trigger]
    L --> E
```

### 5.2 Churn Prediction Module

```python
# Advanced churn prediction with ensemble methods
class ChurnPredictor:
    def __init__(self):
        self.models = {
            'xgboost': XGBoostClassifier(),
            'lightgbm': LGBMClassifier(),
            'neural_network': MLPClassifier(),
            'logistic_regression': LogisticRegression()
        }
        self.ensemble = VotingClassifier(self.models.items())
        self.feature_importance = None
    
    def train(self, X_train, y_train, X_val, y_val):
        # Train individual models
        for name, model in self.models.items():
            model.fit(X_train, y_train)
            val_score = model.score(X_val, y_val)
            mlflow.log_metric(f"{name}_val_score", val_score)
        
        # Train ensemble
        self.ensemble.fit(X_train, y_train)
        
        # Calculate feature importance
        self.feature_importance = self.calculate_feature_importance(X_train)
        
        return self.ensemble
    
    def predict_proba(self, X):
        return self.ensemble.predict_proba(X)[:, 1]
    
    def explain_prediction(self, customer_features):
        # SHAP explanations for interpretability
        explainer = shap.TreeExplainer(self.models['xgboost'])
        shap_values = explainer.shap_values(customer_features)
        return shap_values
```

### 5.3 Customer Segmentation Module

```python
# Advanced segmentation with multiple algorithms
class CustomerSegmentation:
    def __init__(self):
        self.algorithms = {
            'kmeans': KMeans(n_clusters=5),
            'dbscan': DBSCAN(eps=0.5, min_samples=5),
            'gaussian_mixture': GaussianMixture(n_components=5),
            'hierarchical': AgglomerativeClustering(n_clusters=5)
        }
        self.rfm_segmentation = RFMSegmentation()
    
    def segment_customers(self, customer_data):
        # RFM-based segmentation
        rfm_segments = self.rfm_segmentation.segment(customer_data)
        
        # ML-based segmentation
        ml_segments = {}
        for name, algorithm in self.algorithms.items():
            segments = algorithm.fit_predict(customer_data)
            ml_segments[name] = segments
        
        # Combine segmentations
        combined_segments = self.combine_segmentations(
            rfm_segments, ml_segments
        )
        
        return combined_segments
    
    def analyze_segments(self, segments, customer_data):
        # Segment profiling and analysis
        segment_profiles = {}
        for segment_id in np.unique(segments):
            segment_data = customer_data[segments == segment_id]
            profile = {
                'size': len(segment_data),
                'avg_clv': segment_data['clv'].mean(),
                'churn_rate': segment_data['churn'].mean(),
                'characteristics': self.extract_characteristics(segment_data)
            }
            segment_profiles[segment_id] = profile
        
        return segment_profiles
```

### 5.4 Recommendation Engine

```python
# Retention strategy recommendation engine
class RecommendationEngine:
    def __init__(self):
        self.strategy_models = {
            'discount_optimization': DiscountOptimizer(),
            'communication_timing': CommunicationOptimizer(),
            'product_recommendation': ProductRecommender(),
            'channel_optimization': ChannelOptimizer()
        }
        self.ab_testing = ABTestingFramework()
    
    def recommend_retention_strategy(self, customer_profile, churn_probability):
        # Generate personalized retention strategies
        strategies = []
        
        for strategy_name, model in self.strategy_models.items():
            recommendation = model.recommend(customer_profile, churn_probability)
            strategies.append({
                'strategy': strategy_name,
                'recommendation': recommendation,
                'expected_impact': model.estimate_impact(recommendation),
                'confidence': model.confidence_score(recommendation)
            })
        
        # Rank strategies by expected impact
        strategies.sort(key=lambda x: x['expected_impact'], reverse=True)
        
        return strategies
    
    def create_ab_test(self, strategy, target_customers):
        # Create A/B test for strategy validation
        test_config = {
            'strategy': strategy,
            'target_customers': target_customers,
            'control_group_size': 0.3,
            'test_duration_days': 30,
            'success_metrics': ['retention_rate', 'revenue_impact']
        }
        
        return self.ab_testing.create_test(test_config)
```

---

## 6. API Layer Design

### 6.1 RESTful API Structure

```python
# FastAPI application with comprehensive endpoints
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Customer Churn Analytics API",
    description="Comprehensive API for customer churn prediction and analytics",
    version="2.0.0"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication
security = HTTPBearer()

# Customer endpoints
@app.get("/api/v1/customers/{customer_id}/churn-prediction")
async def get_churn_prediction(
    customer_id: str,
    token: str = Depends(security)
):
    """Get real-time churn prediction for a customer"""
    auth_service.verify_token(token)
    prediction = await ml_service.predict_churn(customer_id)
    return {
        "customer_id": customer_id,
        "churn_probability": prediction.probability,
        "risk_level": prediction.risk_level,
        "factors": prediction.contributing_factors,
        "recommendations": prediction.retention_strategies,
        "timestamp": prediction.timestamp
    }

@app.post("/api/v1/customers/batch-prediction")
async def batch_churn_prediction(
    customer_ids: List[str],
    token: str = Depends(security)
):
    """Get churn predictions for multiple customers"""
    auth_service.verify_token(token)
    predictions = await ml_service.batch_predict_churn(customer_ids)
    return {"predictions": predictions}

# Analytics endpoints
@app.get("/api/v1/analytics/segments")
async def get_customer_segments(token: str = Depends(security)):
    """Get customer segmentation analysis"""
    auth_service.verify_token(token)
    segments = await analytics_service.get_customer_segments()
    return segments

@app.get("/api/v1/analytics/cohort-analysis")
async def get_cohort_analysis(
    start_date: date,
    end_date: date,
    token: str = Depends(security)
):
    """Get cohort analysis for specified date range"""
    auth_service.verify_token(token)
    cohort_data = await analytics_service.get_cohort_analysis(start_date, end_date)
    return cohort_data

# Model management endpoints
@app.get("/api/v1/models/performance")
async def get_model_performance(token: str = Depends(security)):
    """Get current model performance metrics"""
    auth_service.verify_token(token)
    performance = await ml_service.get_model_performance()
    return performance

@app.post("/api/v1/models/retrain")
async def trigger_model_retraining(token: str = Depends(security)):
    """Trigger model retraining pipeline"""
    auth_service.verify_token(token)
    task_id = await ml_service.trigger_retraining()
    return {"task_id": task_id, "status": "initiated"}
```

### 6.2 WebSocket Support for Real-time Updates

```python
# WebSocket endpoints for real-time dashboard updates
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/dashboard-updates")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Send real-time updates
            updates = await get_dashboard_updates()
            await websocket.send_json(updates)
            await asyncio.sleep(30)  # Update every 30 seconds
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

---

## 7. Database Architecture

### 7.1 Database Schema Design

```sql
-- PostgreSQL schema for scalable customer churn analytics

-- Customers table (main entity)
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Demographics
    age INTEGER,
    gender VARCHAR(20),
    region VARCHAR(50),
    
    -- Account information
    signup_date DATE,
    tenure_months INTEGER,
    account_status VARCHAR(20) DEFAULT 'active',
    
    -- Behavioral data
    total_orders INTEGER DEFAULT 0,
    avg_order_value DECIMAL(10,2),
    days_since_last_purchase INTEGER,
    loyalty_score DECIMAL(3,2),
    complaints INTEGER DEFAULT 0,
    
    -- Preferences
    payment_type VARCHAR(30),
    is_promo_user BOOLEAN DEFAULT FALSE,
    communication_preference VARCHAR(20),
    
    -- Target variable
    churn BOOLEAN DEFAULT FALSE,
    churn_date DATE,
    
    -- Indexes for performance
    INDEX idx_customer_region (region),
    INDEX idx_customer_tenure (tenure_months),
    INDEX idx_customer_churn (churn),
    INDEX idx_customer_updated (updated_at)
);

-- Predictions table (ML model outputs)
CREATE TABLE predictions (
    prediction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id VARCHAR(50) REFERENCES customers(customer_id),
    model_version VARCHAR(50),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Prediction results
    churn_probability DECIMAL(5,4),
    risk_level VARCHAR(20), -- 'low', 'medium', 'high'
    confidence_score DECIMAL(5,4),
    
    -- Feature contributions (JSONB for flexibility)
    feature_importance JSONB,
    contributing_factors JSONB,
    
    -- Recommendations
    recommended_actions JSONB,
    
    INDEX idx_prediction_customer (customer_id),
    INDEX idx_prediction_date (prediction_date),
    INDEX idx_prediction_risk (risk_level)
);

-- Customer segments table
CREATE TABLE customer_segments (
    segment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id VARCHAR(50) REFERENCES customers(customer_id),
    segmentation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Segmentation results
    rfm_segment VARCHAR(50),
    behavioral_segment VARCHAR(50),
    value_segment VARCHAR(50),
    
    -- Segment characteristics
    segment_scores JSONB,
    
    INDEX idx_segment_customer (customer_id),
    INDEX idx_segment_rfm (rfm_segment),
    INDEX idx_segment_date (segmentation_date)
);

-- Model performance tracking
CREATE TABLE model_performance (
    performance_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name VARCHAR(100),
    model_version VARCHAR(50),
    evaluation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Performance metrics
    accuracy DECIMAL(5,4),
    precision_score DECIMAL(5,4),
    recall DECIMAL(5,4),
    f1_score DECIMAL(5,4),
    auc_roc DECIMAL(5,4),
    
    -- Business metrics
    precision_at_k JSONB, -- Precision at different K values
    lift_curve JSONB,
    
    -- Data drift metrics
    feature_drift_scores JSONB,
    target_drift_score DECIMAL(5,4),
    
    INDEX idx_performance_model (model_name, model_version),
    INDEX idx_performance_date (evaluation_date)
);

-- A/B testing framework tables
CREATE TABLE ab_tests (
    test_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_name VARCHAR(200),
    description TEXT,
    
    -- Test configuration
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'completed', 'paused'
    
    -- Test parameters
    control_group_size DECIMAL(3,2),
    test_group_size DECIMAL(3,2),
    success_metrics JSONB,
    
    -- Results
    results JSONB,
    statistical_significance DECIMAL(5,4),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_test_status (status),
    INDEX idx_test_dates (start_date, end_date)
);

CREATE TABLE ab_test_assignments (
    assignment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_id UUID REFERENCES ab_tests(test_id),
    customer_id VARCHAR(50) REFERENCES customers(customer_id),
    
    group_type VARCHAR(20), -- 'control', 'test'
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Outcome tracking
    converted BOOLEAN DEFAULT FALSE,
    conversion_date TIMESTAMP,
    conversion_value DECIMAL(10,2),
    
    INDEX idx_assignment_test (test_id),
    INDEX idx_assignment_customer (customer_id),
    INDEX idx_assignment_group (group_type)
);

-- Audit and logging tables
CREATE TABLE data_quality_checks (
    check_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    table_name VARCHAR(100),
    
    -- Quality metrics
    total_records INTEGER,
    null_counts JSONB,
    duplicate_counts INTEGER,
    outlier_counts JSONB,
    
    -- Data freshness
    latest_record_date TIMESTAMP,
    data_lag_hours INTEGER,
    
    -- Quality score
    overall_quality_score DECIMAL(5,4),
    
    INDEX idx_quality_table (table_name),
    INDEX idx_quality_date (check_date)
);
```

### 7.2 Data Partitioning Strategy

```sql
-- Partition predictions table by date for better performance
CREATE TABLE predictions_partitioned (
    LIKE predictions INCLUDING ALL
) PARTITION BY RANGE (prediction_date);

-- Create monthly partitions
CREATE TABLE predictions_2024_01 PARTITION OF predictions_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE predictions_2024_02 PARTITION OF predictions_partitioned
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Auto-create partitions using pg_partman extension
SELECT partman.create_parent(
    p_parent_table => 'public.predictions_partitioned',
    p_control => 'prediction_date',
    p_type => 'range',
    p_interval => 'monthly'
);
```

---

## 8. Deployment Strategy

### 8.1 Containerization with Docker

```dockerfile
# Multi-stage Dockerfile for production deployment
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd --create-home --shell /bin/bash app

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership to app user
RUN chown -R app:app /app
USER app

# Production stage
FROM base as production

# Install production dependencies only
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "src.api.main:app"]
```

### 8.2 Kubernetes Deployment

```yaml
# Kubernetes deployment configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: churn-dashboard
  labels:
    app: churn-dashboard
spec:
  replicas: 3
  selector:
    matchLabels:
      app: churn-dashboard
  template:
    metadata:
      labels:
        app: churn-dashboard
    spec:
      containers:
      - name: dashboard
        image: churn-dashboard:latest
        ports:
        - containerPort: 8501
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: redis-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8501
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: churn-dashboard-service
spec:
  selector:
    app: churn-dashboard
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8501
  type: LoadBalancer

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: churn-dashboard-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - churn-dashboard.company.com
    secretName: churn-dashboard-tls
  rules:
  - host: churn-dashboard.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: churn-dashboard-service
            port:
              number: 80
```

### 8.3 CI/CD Pipeline

```yaml
# GitHub Actions workflow
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:6
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t churn-dashboard:${{ github.sha }} .
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push churn-dashboard:${{ github.sha }}
    
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/churn-dashboard churn-dashboard=churn-dashboard:${{ github.sha }}
```

---

## 9. Scaling Considerations

### 9.1 Horizontal Scaling Strategy

```python
# Load balancing and auto-scaling configuration
class ScalingManager:
    def __init__(self):
        self.load_balancer = LoadBalancer()
        self.auto_scaler = AutoScaler()
        self.metrics_collector = MetricsCollector()
    
    def configure_auto_scaling(self):
        # CPU-based scaling
        cpu_policy = ScalingPolicy(
            metric='cpu_utilization',
            target_value=70,
            scale_up_threshold=80,
            scale_down_threshold=30,
            min_replicas=2,
            max_replicas=10
        )
        
        # Memory-based scaling
        memory_policy = ScalingPolicy(
            metric='memory_utilization',
            target_value=75,
            scale_up_threshold=85,
            scale_down_threshold=40,
            min_replicas=2,
            max_replicas=10
        )
        
        # Request-based scaling
        request_policy = ScalingPolicy(
            metric='requests_per_second',
            target_value=100,
            scale_up_threshold=150,
            scale_down_threshold=50,
            min_replicas=2,
            max_replicas=15
        )
        
        self.auto_scaler.add_policies([cpu_policy, memory_policy, request_policy])
```

### 9.2 Database Scaling

```python
# Database scaling with read replicas and connection pooling
class DatabaseScalingManager:
    def __init__(self):
        self.master_db = MasterDatabase()
        self.read_replicas = [ReadReplica(i) for i in range(3)]
        self.connection_pool = ConnectionPool(
            min_connections=10,
            max_connections=100,
            connection_timeout=30
        )
    
    def get_read_connection(self):
        # Load balance read queries across replicas
        replica = self.load_balancer.select_replica(self.read_replicas)
        return self.connection_pool.get_connection(replica)
    
    def get_write_connection(self):
        # All writes go to master
        return self.connection_pool.get_connection(self.master_db)
```

### 9.3 Caching Strategy

```python
# Multi-level caching for performance
class CacheManager:
    def __init__(self):
        self.l1_cache = InMemoryCache(max_size=1000)  # Application cache
        self.l2_cache = RedisCache()                   # Distributed cache
        self.l3_cache = DatabaseCache()                # Database query cache
    
    async def get(self, key: str):
        # Try L1 cache first
        value = self.l1_cache.get(key)
        if value:
            return value
        
        # Try L2 cache
        value = await self.l2_cache.get(key)
        if value:
            self.l1_cache.set(key, value)
            return value
        
        # Try L3 cache
        value = await self.l3_cache.get(key)
        if value:
            await self.l2_cache.set(key, value)
            self.l1_cache.set(key, value)
            return value
        
        return None
    
    async def set(self, key: str, value: any, ttl: int = 3600):
        # Set in all cache levels
        self.l1_cache.set(key, value, ttl)
        await self.l2_cache.set(key, value, ttl)
        await self.l3_cache.set(key, value, ttl)
```

---

## 10. Security and Compliance

### 10.1 Authentication and Authorization

```python
# JWT-based authentication with role-based access control
class AuthenticationService:
    def __init__(self):
        self.jwt_handler = JWTHandler()
        self.user_repository = UserRepository()
        self.permission_manager = PermissionManager()
    
    def authenticate_user(self, username: str, password: str):
        user = self.user_repository.get_by_username(username)
        if not user or not self.verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid credentials")
        
        # Generate JWT token
        token = self.jwt_handler.create_token({
            'user_id': user.id,
            'username': user.username,
            'roles': user.roles,
            'permissions': self.permission_manager.get_user_permissions(user.id)
        })
        
        return token
    
    def authorize_action(self, token: str, required_permission: str):
        payload = self.jwt_handler.decode_token(token)
        user_permissions = payload.get('permissions', [])
        
        if required_permission not in user_permissions:
            raise AuthorizationError("Insufficient permissions")
        
        return True

# Role-based access control
class PermissionManager:
    PERMISSIONS = {
        'admin': [
            'view_all_customers',
            'manage_models',
            'view_system_metrics',
            'manage_users',
            'export_data'
        ],
        'analyst': [
            'view_all_customers',
            'view_analytics',
            'export_reports'
        ],
        'manager': [
            'view_team_customers',
            'view_analytics',
            'create_campaigns'
        ],
        'viewer': [
            'view_assigned_customers',
            'view_basic_analytics'
        ]
    }
```

### 10.2 Data Privacy and Encryption

```python
# Data encryption and privacy protection
class DataPrivacyManager:
    def __init__(self):
        self.encryption_key = self.load_encryption_key()
        self.pii_fields = ['email', 'phone', 'address', 'ssn']
    
    def encrypt_sensitive_data(self, data: dict):
        encrypted_data = data.copy()
        for field in self.pii_fields:
            if field in encrypted_data:
                encrypted_data[field] = self.encrypt_field(encrypted_data[field])
        return encrypted_data
    
    def decrypt_sensitive_data(self, encrypted_data: dict):
        decrypted_data = encrypted_data.copy()
        for field in self.pii_fields:
            if field in decrypted_data:
                decrypted_data[field] = self.decrypt_field(decrypted_data[field])
        return decrypted_data
    
    def anonymize_data(self, data: dict):
        # Remove or hash PII for analytics
        anonymized_data = data.copy()
        for field in self.pii_fields:
            if field in anonymized_data:
                anonymized_data[field] = self.hash_field(anonymized_data[field])
        return anonymized_data
```

### 10.3 Audit Logging

```python
# Comprehensive audit logging
class AuditLogger:
    def __init__(self):
        self.logger = logging.getLogger('audit')
        self.db_logger = DatabaseAuditLogger()
    
    def log_user_action(self, user_id: str, action: str, resource: str, details: dict = None):
        audit_entry = {
            'timestamp': datetime.utcnow(),
            'user_id': user_id,
            'action': action,
            'resource': resource,
            'details': details,
            'ip_address': self.get_client_ip(),
            'user_agent': self.get_user_agent()
        }
        
        # Log to file
        self.logger.info(json.dumps(audit_entry))
        
        # Log to database
        self.db_logger.log_entry(audit_entry)
    
    def log_data_access(self, user_id: str, table: str, operation: str, record_count: int):
        self.log_user_action(
            user_id=user_id,
            action='data_access',
            resource=table,
            details={
                'operation': operation,
                'record_count': record_count
            }
        )
```

---

This comprehensive architecture document provides a solid foundation for building a scalable Customer Churn Analytics Dashboard. The design emphasizes modularity, scalability, security, and maintainability while incorporating modern best practices for ML-powered applications.

The architecture supports real-time predictions, advanced analytics, and can handle the specified scale of 10K-100K customers with 10-20 concurrent users. It's designed for cloud deployment and includes all the advanced features requested: real-time ML predictions, automated model retraining, advanced customer segmentation, and A/B testing framework.
</content>
<line_count>1247</line_count>
</write_to_file>

---

**User:**

[write_to_file for 'docs/SCALABLE_ARCHITECTURE.md'] Result:
<file_write_result>
<path>docs/SCALABLE_ARCHITECTURE.md</path>
<operation>created</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
docs/SCALABLE_ARCHITECTURE.md

# VSCode Open Tabs
README.md,docs/SCALABLE_ARCHITECTURE.md,LICENSE,app.py,.gitignore,tests/smoke_tests.py,src/biz_metrics.py,src/data_prep.py,src/eda_utils.py,src/helpers.py,pages/1_Data_Exploration.py,pages/3_Customer_Retention.py,src/sql_utils.py,data/generate_synthetic_data.py,notebooks/eda_playground.ipynb,pages/4_Business_Insights.py,pages/2_Customer_Groups.py,requirements.txt

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T12:45:21.078Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.54

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Analyze existing project structure and components | Completed |
| 2 | Design comprehensive scalable architecture document | In Progress |
| 3 | Create detailed folder structure specification | Pending |
| 4 | Document component communication patterns | Pending |
| 5 | Design ML pipeline architecture | Pending |
| 6 | Create system architecture diagrams | Pending |
| 7 | Document deployment and scaling strategies | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Analyze existing project structure and components
[x] Design comprehensive scalable architecture document
[-] Create visual architecture diagrams with Mermaid
[ ] Document implementation roadmap
[ ] Create component interaction examples
[ ] Document monitoring and observability setup
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
docs/SCALABLE_ARCHITECTURE.md

# VSCode Open Tabs
README.md,docs/SCALABLE_ARCHITECTURE.md,LICENSE,app.py,.gitignore,tests/smoke_tests.py,src/biz_metrics.py,src/data_prep.py,src/eda_utils.py,src/helpers.py,pages/1_Data_Exploration.py,pages/3_Customer_Retention.py,src/sql_utils.py,data/generate_synthetic_data.py,notebooks/eda_playground.ipynb,pages/4_Business_Insights.py,pages/2_Customer_Groups.py,requirements.txt

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T12:45:29.050Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.68

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Analyze existing project structure and components | Completed |
| 2 | Design comprehensive scalable architecture document | Completed |
| 3 | Create visual architecture diagrams with Mermaid | In Progress |
| 4 | Document implementation roadmap | Pending |
| 5 | Create component interaction examples | Pending |
| 6 | Document monitoring and observability setup | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

