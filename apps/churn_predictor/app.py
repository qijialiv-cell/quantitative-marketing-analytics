"""
apps/churn_predictor/app.py
Churn Prediction Simulator — Teaching Demo
University of Liverpool | MKTS 301

Deployment: Render
Run locally: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Churn Predictor | UoL Marketing",
    page_icon="📊",
    layout="wide",
)

# ── Sidebar: About ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("About this tool")
    st.markdown("""
    This interactive tool demonstrates how a logistic regression model
    scores individual customers for churn risk.

    **Use in teaching:** MKTS 301 — ML for Marketing, Week 5

    **How to interpret:**
    - Churn probability = likelihood the customer leaves in the next 30 days
    - Lift = how much better than random targeting

    **Limitations:**
    - Trained on synthetic data for demonstration only
    - Real deployment requires retraining on actual customer data
    """)
    st.divider()
    st.caption("University of Liverpool | Marketing Department")

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("Customer Churn Prediction Simulator")
st.caption(
    "Enter customer characteristics to generate a churn probability score. "
    "Model: Logistic Regression trained on synthetic telco-style data."
)

# ── Generate and train on synthetic data (cached) ─────────────────────────────
@st.cache_data
def train_model():
    """Train a demo logistic regression model on synthetic data."""
    np.random.seed(42)
    X, y = make_classification(
        n_samples=2000, n_features=5, n_informative=4,
        n_redundant=1, random_state=42
    )
    scaler = StandardScaler()
    X_sc = scaler.fit_transform(X)
    model = LogisticRegression(random_state=42)
    model.fit(X_sc, y)
    return model, scaler


model, scaler = train_model()

# ── Input panel ───────────────────────────────────────────────────────────────
st.subheader("Customer Profile")

col1, col2, col3 = st.columns(3)

with col1:
    tenure = st.slider("Tenure (months)", 1, 72, 12)
    monthly_charge = st.slider("Monthly Charge (£)", 10, 150, 60)

with col2:
    num_products = st.selectbox("Number of Products", [1, 2, 3, 4], index=1)
    has_support = st.toggle("Has Support Contract", value=False)

with col3:
    nps = st.slider("NPS Score (0–10)", 0, 10, 5)

# Construct feature vector (mapped to 5 synthetic features)
x_input = np.array([[
    (tenure - 36) / 20,
    (monthly_charge - 80) / 30,
    num_products - 2,
    int(has_support) * 2 - 1,
    (nps - 5) / 3,
]])

# ── Prediction ────────────────────────────────────────────────────────────────
churn_prob = model.predict_proba(x_input)[0, 1]
base_rate = 0.26  # synthetic base rate
lift = (churn_prob / base_rate) if base_rate > 0 else 0

st.divider()
st.subheader("Prediction Results")

col_a, col_b, col_c = st.columns(3)

col_a.metric(
    "Churn Probability",
    f"{churn_prob:.1%}",
    delta=f"{churn_prob - base_rate:+.1%} vs. base rate",
    delta_color="inverse",
)
col_b.metric("Lift over Random", f"{lift:.2f}×")
col_c.metric(
    "Risk Level",
    "High" if churn_prob > 0.6 else ("Medium" if churn_prob > 0.35 else "Low"),
)

# ── Gauge chart ───────────────────────────────────────────────────────────────
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=churn_prob * 100,
    number={"suffix": "%", "font": {"size": 28}},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "#e74c3c" if churn_prob > 0.6 else ("#f39c12" if churn_prob > 0.35 else "#2ecc71")},
        "steps": [
            {"range": [0, 35], "color": "#d5f5e3"},
            {"range": [35, 60], "color": "#fef9e7"},
            {"range": [60, 100], "color": "#fadbd8"},
        ],
        "threshold": {"line": {"color": "black", "width": 3}, "value": base_rate * 100},
    },
    title={"text": "Churn Risk Score"},
))
fig.update_layout(height=280, margin=dict(t=40, b=0, l=20, r=20))
st.plotly_chart(fig, use_container_width=True)

# ── Interpretation ────────────────────────────────────────────────────────────
st.subheader("How to interpret this result")
st.markdown(f"""
- **Base rate:** {base_rate:.0%} of customers churn on average each month.
- **This customer:** Predicted churn probability is **{churn_prob:.1%}**.
- **Lift = {lift:.2f}×** means this customer is **{lift:.1f}× more likely** to churn
  than a randomly selected customer.

**Marketing implication:** {"⚠️ Priority for retention intervention — consider a targeted offer or proactive outreach." if churn_prob > 0.5 else "✅ No immediate intervention required — monitor monthly."}

> *Note: Lift is the key metric for campaign targeting. A campaign budget covering 20% of customers
> should target those with the highest predicted churn probability — not a random selection.*
""")

# ── Feature influence (coefficients) ──────────────────────────────────────────
with st.expander("Model internals — coefficient plot"):
    feature_names = ["Tenure", "Monthly Charge", "Num Products", "Support Contract", "NPS Score"]
    coefs = model.coef_[0]

    fig2 = px.bar(
        x=coefs, y=feature_names, orientation="h",
        color=coefs, color_continuous_scale="RdYlGn_r",
        title="Logistic Regression Coefficients (positive = increases churn risk)",
        labels={"x": "Coefficient", "y": "Feature"},
        template="simple_white",
    )
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "Each coefficient shows the direction of effect. "
        "Longer tenure reduces churn risk; higher monthly charges increase it."
    )
