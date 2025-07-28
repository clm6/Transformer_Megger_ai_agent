# Quick Setup Guide

## 1. Clone Repository
`ash
git clone [your-repo-url]
cd transformer-diagnostic-ai
``n
## 2. Install Dependencies
`ash
cd trax-analyzer
pip install -r requirements.txt
``n
## 3. Setup API Key
`ash
copy .env.template .env
``nThen edit .env file and add your OpenAI API key.

## 4. Run Analysis
`ash
python main_json_analyzer.py "../Projects/TRAX_Reports"
python generate_final_report.py
``n
See SECURITY.md for detailed security guidelines.
