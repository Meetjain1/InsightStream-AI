# ⚠️ PROTECTED CODE - DO NOT COPY ⚠️

This is a Team project by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). This repository is publicly visible for demonstration purposes only.

Author: Meet Jain & Aditi Gopinath
- This project is protected. Do not copy, fork, or reuse without permission.
- Unauthorized use is strictly prohibited. Only the official deployment is allowed to run.

## Legal Protection
This project is protected by copyright law and includes proprietary security measures. Unauthorized use or attempts to circumvent security measures may result in legal consequences.

## Contact
For any inquiries about this project please contact: meetofficialhere@gmail.com

# Customer Business Analysis Dashboard

A powerful, easy-to-use dashboard for analyzing customer behavior, identifying segments, and preventing customer churn.

## Overview

This dashboard helps businesses understand their customers better and make smart decisions to keep them happy. It takes customer data, shows important patterns, and gives actionable advice that anyone can understand - no fancy statistics degree needed!

## Features

The dashboard comes packed with tools that make customer analysis simple:

- **See Your Data Come to Life**: Interactive charts that show customer patterns anyone can understand
- **Ask Questions Using SQL**: Run simple queries to dig into your customer data
- **Group Similar Customers**: Automatically sort customers into meaningful groups
- **Spot Why Customers Leave**: Find the real reasons behind customer churn
- **Get Plain-English Advice**: Receive clear recommendations anyone can implement

## Dashboard Pages

Our dashboard has four main sections:

1. **Data Explorer**: Look at your customer data in different ways and spot patterns
2. **Customer Groups**: See which types of customers you have and how they behave
3. **Churn Analysis**: Understand why customers leave and who's at risk
4. **Recommendations**: Get practical advice on keeping customers happy

## Architecture

The dashboard is built with a clean, modular structure that makes it easy to understand and extend.

```
┌─────────────────────────────────────┐
│           Web Interface             │
│    (Streamlit Interactive Pages)    │
└───────────────┬─────────────────────┘
                │
┌───────────────▼─────────────────────┐
│         Business Logic Layer         │
│   (Data Analysis & Visualization)   │
└───────────────┬─────────────────────┘
                │
┌───────────────▼─────────────────────┐
│           Data Access Layer          │
│      (CSV Import & SQLite DB)       │
└─────────────────────────────────────┘
```

### Component Diagram

```
┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│  Data Input  │───▶│  Processing   │───▶│ Visualization│
│  & Storage   │    │  & Analysis   │    │  & Reports   │
└──────────────┘    └───────────────┘    └──────────────┘
       │                   │                    │
       ▼                   ▼                    ▼
┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│ CSV Importer │    │ Segmentation  │    │ Interactive  │
│ SQLite DB    │    │ Churn Models  │    │ Dashboards   │
└──────────────┘    └───────────────┘    └──────────────┘
```

## How to Use the Dashboard

### Getting Started

When you open the dashboard, you'll see a home page with these options:

1. **Load Sample Data**: Click this button to try out the dashboard with example data
2. **Upload Your Own Data**: Upload your customer data file (CSV format)
3. **Save to Database**: Store your data for faster access next time

### Understanding Your Customers

Once your data is loaded, you can:

- **See Key Numbers**: Total customers, churn rate, and customer value at a glance
- **Explore Different Pages**: Use the sidebar to navigate between dashboard sections
- **Download Reports**: Export insights as CSV files to share with your team

### Data You Can Use

To get the most from this dashboard, your customer data should include:

- **Must Have**:
  - `customer_id`: A unique number/code for each customer
  - `churn`: Whether they've left (1) or stayed (0)

- **Good to Have**:
  - **Who they are**: Age, gender, location
  - **What they buy**: Number of orders, average spending
  - **How they engage**: Days since last purchase, loyalty points
  - **Customer experience**: Number of complaints
  - **Other useful info**: Payment method, months as customer, etc.

Sample data is included if you just want to try things out!

## Project Organization

The project is organized into these key folders:

```
Customer-Churn-Dashboard/
├── app.py                # Main dashboard entry point
├── requirements.txt      # Python package dependencies
├── .streamlit/           # Streamlit configuration
├── data/                 # Data files and database
│   └── sample_churn.csv  # Example customer dataset
├── pages/                # Dashboard page files
│   ├── 1_EDA_and_SQL_Checks.py           # Data exploration page
│   ├── 2_Customer_Segments.py            # Customer segmentation page
│   ├── 3_Churn_Analysis.py               # Churn analysis page
│   └── 4_Insights_and_Recommendations.py  # Insights page
└── src/                  # Source code modules
    ├── data_prep.py      # Data preparation functions
    ├── helpers.py        # Helper utilities and constants
    └── sql_utils.py      # Database functions
```

## Analysis Methods Made Simple

The dashboard uses these business techniques, explained in plain language:

1. **RFM Grouping**: Groups customers based on:
   - How Recently they purchased
   - How Frequently they buy
   - How Much Money they spend

2. **Customer Journey**: Tracks how customers behave over time from when they first joined

3. **Churn Reasons**: Finds the real factors that make customers leave

4. **Customer Value**: Shows how much a customer is worth to your business long-term

5. **Ask Your Own Questions**: Use simple SQL queries to answer specific business questions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Connect us through the following platforms:

### Professional Networking
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/meet-jain-413015265/)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=flat&logo=twitter&logoColor=white)](https://twitter.com/Meetjain_100)

### Social Media and Platforms
[![Discord](https://img.shields.io/badge/Discord-7289DA?style=flat&logo=discord&logoColor=white)](https://discordapp.com/users/meetofficial)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/m.jain_17/)

