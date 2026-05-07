# Churn Prediction Simulator

**Platform:** Render (Streamlit)
**Module:** MKTS 301 — Machine Learning for Marketing, Week 5

## Purpose
Interactive demo allowing students to adjust customer characteristics and observe how
a logistic regression model scores churn probability. Includes lift interpretation.

## Run locally
```bash
cd apps/churn_predictor
streamlit run app.py
```

## Deploy on Render
1. Connect this GitHub repo to Render
2. Set root directory to `apps/churn_predictor`
3. Build command: `pip install -r ../../requirements.txt`
4. Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

Or use the included `render.yaml` for blueprint deployment.

## Deployed URL
<!-- Update when live -->
https://uol-churn-predictor.onrender.com
