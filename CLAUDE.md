# CLAUDE.md — Academic Computational Marketing System
## University of Liverpool | Marketing Department

> **Purpose:** This file is the operating contract between Claude and this repository.
> It governs all code generation, documentation, teaching material, and research output.
> It is version-controlled and updated at the start of each academic semester.

---

## 0. Quick Reference

| Context | Default behaviour |
|---|---|
| Teaching code | Clarity first, interpret everything, use comments liberally |
| Research code | Reproducibility first, flag causal claims, document assumptions |
| Apps (Streamlit/Gradio) | Minimal UI, interpretable outputs, fast load |
| Quarto | Code-generated figures only, clean YAML frontmatter |
| Ambiguity | Default to interpretability → reproducibility → teaching utility |

---

## 1. Repository Identity

This is a **long-term academic workspace** maintained across semesters at the University of Liverpool.
It serves three integrated purposes:

1. **Teaching** — undergraduate and postgraduate modules in marketing analytics, data visualisation, and applied machine learning
2. **Research** — computational marketing, NLP, causal inference, brand and influencer studies
3. **Demonstration** — interactive student-facing tools and reproducible empirical pipelines

The repository is a *living academic infrastructure*, not a disposable project. Every contribution
should be written with reuse, clarity, and longevity in mind.

---

## 2. Repository Structure

```
/
├── CLAUDE.md                    ← this file (repo root, always)
├── README.md
├── requirements.txt             ← pinned dependencies (see §8)
├── .github/
│   └── workflows/               ← CI/CD for deployment
│
├── teaching/
│   ├── 2025_fall/
│   │   ├── ml_for_marketing/
│   │   │   ├── slides/          ← Quarto .qmd files
│   │   │   ├── labs/            ← Jupyter notebooks
│   │   │   ├── assignments/
│   │   │   └── data/            ← teaching datasets (raw + processed)
│   │   ├── data_viz/
│   │   └── intro_deep_learning/
│   └── 2026_spring/             ← new semester, never overwrite previous
│
├── research/
│   ├── paper_brand_activism/
│   ├── paper_influencer_ml/
│   └── paper_causal_nlp/
│       ├── data/
│       │   ├── raw/             ← NEVER modify
│       │   └── processed/
│       ├── src/
│       │   ├── preprocessing/
│       │   ├── models/
│       │   └── analysis/
│       ├── outputs/
│       │   ├── figures/
│       │   └── tables/
│       └── README.md            ← paper-level README required
│
├── apps/
│   ├── churn_predictor/
│   ├── sentiment_classifier/
│   └── embedding_explorer/
│
├── quarto/
│   ├── website/                 ← academic site source
│   └── shared/                  ← reusable partials and macros
│
└── scripts/
    └── utils/                   ← shared helper functions
```

**Rule: Never overwrite previous semesters. Always version forward.**
When starting a new term, create a new dated folder and copy only what needs to be updated.

---

## 3. Teaching Modules

### 3.1 Machine Learning for Marketing

**Topics:** supervised learning (regression, classification), model evaluation (AUC, RMSE,
cross-validation), feature engineering for marketing data, churn prediction, customer segmentation,
recommendation systems.

**Standards:**
- Every model must have a baseline (e.g. majority class, mean prediction) reported first
- Every metric must be interpreted in marketing terms — not just reported
- Cross-validation is mandatory; train/test split alone is insufficient for teaching
- Feature importance must be visualised and explained
- Never present overfitting as a result

**Example comment standard:**
```python
# XGBoost outperforms logistic regression here (AUC 0.84 vs 0.71),
# but note the interpretability trade-off: logistic coefficients have
# direct marketing meaning (e.g. recency elasticity), XGBoost does not.
```

---

### 3.2 Data Visualisation (ggplot philosophy, Python execution)

Students come with R/ggplot backgrounds. Even when writing Python, preserve the ggplot grammar
of graphics conceptually: data → aesthetics → geometry → facets → theme.

**Core principles:**
- One plot, one message — annotate that message directly on the figure
- Axes always labelled with units
- Colour used for meaning, not decoration; always colourblind-safe palettes
- No chartjunk (3D, unnecessary gridlines, excessive legend entries)
- Figures generated from code, never inserted manually

**Standard imports block for teaching notebooks:**
```python
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

sns.set_theme(style="whitegrid", palette="colorblind")
plt.rcParams.update({"figure.dpi": 150, "font.size": 12})
```

**Required for all teaching figures:**
- Descriptive title (not just variable names)
- Source or dataset noted in caption or comment
- Saved to `/outputs/figures/` with a descriptive filename

---

### 3.3 Introduction to Deep Learning for Marketing

**Topics:** neural embeddings for text (reviews, social media), image-based marketing signals
(brand visuals, influencer content), transformer intuition, CLIP-style multimodal reasoning.

**Pedagogical constraints:**
- Mathematical depth: conceptual correctness required, formal proofs avoided
- Every architectural concept must be motivated by a marketing use case
- Always show input → representation → output, not just the model architecture
- Avoid black-box framing; always explain *what the model has learned*

**Acceptable complexity floor:** A student with no calculus background should follow the intuition.
A student with linear algebra should follow the mechanics.

---

## 4. Research Layer

Research code is **strictly separated** from teaching code. It must meet publication standards.

### 4.1 Empirical Rigour Requirements

Always maintain clear separation between:

| Stage | Description |
|---|---|
| Descriptive | Summary statistics, distributions, correlations — no causal claims |
| Predictive | Model fit, out-of-sample performance — claims limited to prediction |
| Causal | Identification strategy, assumptions, robustness — explicit about what is and is not identified |

**Claude must flag any causal claim made in a predictive or descriptive context.**

### 4.2 Model Standards

- Report robust standard errors by default (HC3 for OLS, clustered where appropriate)
- For panel data: always consider fixed effects before random effects; report Hausman test where relevant
- For ML: report both in-sample and out-of-sample metrics
- For NLP: document tokenisation choices, vocabulary size, embedding strategy, and any preprocessing
- Robustness checks are not optional — include at least one alternative specification per main result

### 4.3 Paper Folder Standard

Each paper folder must contain a `README.md` with:
- Research question (one sentence)
- Data source and version
- Identification strategy (if causal)
- How to reproduce all results from raw data
- Journal target

---

## 5. Application Layer

Interactive tools serve both research dissemination and teaching demonstration.

### 5.1 Framework Selection

| Use case | Framework |
|---|---|
| Teaching demos, student-facing tools | Streamlit |
| ML model interfaces, quick prototypes | Gradio |
| API endpoints (rare) | FastAPI |

Do not introduce new frameworks without justification.

### 5.2 Streamlit Standards

```python
import streamlit as st

st.set_page_config(page_title="App Name | UoL Marketing", layout="wide")
st.title("Descriptive Title")
st.caption("What this tool does and what data it uses.")

# Always include:
# 1. Data description
# 2. Model/method explanation
# 3. Interpretation of outputs
# 4. Limitations section
```

Every app must:
- Load in under 5 seconds (cache heavy computations with `@st.cache_data`)
- Include an "About this tool" section
- Include a "How to interpret results" section
- Run with `streamlit run app.py` from the app directory with no arguments

### 5.3 Deployment Architecture

This repository uses a **four-platform stack**, each with a distinct role. Do not substitute one
for another without justification — each platform is chosen for a specific capability.

```
┌─────────────────────────────────────────────────────────────────┐
│                     DEPLOYMENT STACK                            │
│                                                                 │
│  LAYER 1 — STATIC PUBLISHING                                    │
│  Cloudflare Pages  →  Quarto academic site, lecture slides      │
│  GitHub Pages      →  fallback / mirrors                        │
│                                                                 │
│  LAYER 2 — FRONTEND DASHBOARDS                                  │
│  Vercel            →  React/Next.js interactive dashboards      │
│                        data viz tools, student-facing UIs       │
│                                                                 │
│  LAYER 3 — ML DEMOS                                             │
│  Hugging Face Spaces → Gradio research prototypes               │
│                        model demos, embedding explorers         │
│                                                                 │
│  LAYER 4 — SERIOUS INFRASTRUCTURE                               │
│  Render            →  FastAPI backends, Streamlit apps          │
│                        persistent services, scheduled jobs      │
└─────────────────────────────────────────────────────────────────┘
```

#### Platform decision rules

**Cloudflare Pages / GitHub Pages** — use when:
- Output is a rendered Quarto site or slide deck
- No server-side logic required
- Deployment triggered by push to `main`

**Vercel** — use when:
- Building a React or Next.js dashboard (e.g. interactive data visualisation for students)
- Frontend logic is non-trivial and benefits from edge rendering
- API routes are lightweight and stateless
- Do not use Vercel for Python backends or ML inference

**Hugging Face Spaces** — use when:
- Demoing a trained ML model (classification, embedding, generation)
- Interface is Gradio
- The audience is researchers or technically literate students
- Compute cost must be zero or minimal
- Not suitable for persistent storage or database-backed apps

**Render** — use when:
- App requires a Python backend (FastAPI, Flask)
- Running Streamlit with backend data processing or API calls
- Scheduled jobs or background workers are needed
- Data must persist between sessions (use Render's disk or connect to external DB)
- This is the **serious infrastructure layer**: production-grade, always-on, scalable

#### Deployment rules (all platforms)

- All deployments are **GitHub-driven** — no manual uploads, ever
- Every deployment must be reproducible from the repo state at the deployed commit
- Environment variables (API keys, secrets) stored in platform settings, never in code
- Each app directory must include a `README.md` with: purpose, local run command, deployed URL

#### Example platform mapping

| Asset | Platform | Trigger |
|---|---|---|
| Academic website (`quarto/website/`) | Cloudflare Pages | push to `main` |
| Lecture slides (`teaching/*/slides/`) | Cloudflare Pages | push to `main` |
| Student dashboard (React) | Vercel | push to `main` |
| Churn predictor demo (Gradio) | Hugging Face Spaces | manual or GitHub Action |
| Embedding similarity explorer (Gradio) | Hugging Face Spaces | manual or GitHub Action |
| Sentiment classifier API (FastAPI) | Render | push to `main` |
| Streamlit teaching app | Render | push to `main` |

---

## 6. Quarto Academic System

Quarto is the source of truth for all written academic outputs.

### 6.1 Rules

- `.qmd` files are canonical — never edit rendered HTML/PDF directly
- All figures must be generated by code chunks within the document
- YAML frontmatter must be complete (title, author, date, format, bibliography)
- Use `execute: echo: false` for clean teaching slides, `true` for lab materials

### 6.2 Standard Frontmatter Templates

**Teaching slides:**
```yaml
---
title: "Week 4: Model Evaluation"
subtitle: "MKTS 301 — Machine Learning for Marketing"
author: "University of Liverpool"
date: today
format:
  revealjs:
    theme: simple
    slide-number: true
    code-fold: false
execute:
  echo: true
  warning: false
---
```

**Research manuscript:**
```yaml
---
title: "Paper Title"
author:
  - name: "Author Name"
    affiliation: "University of Liverpool"
date: today
format:
  pdf:
    documentclass: article
    cite-method: biblatex
bibliography: references.bib
execute:
  echo: false
  cache: true
---
```

---

## 7. Data Governance

| Rule | Detail |
|---|---|
| Raw data is immutable | Never modify files in `/data/raw/`. Transform in code only. |
| Processed versions | Always saved to `/data/processed/` with transformation script documented |
| Data dictionaries | Required for all teaching datasets; stored alongside the data |
| External data | Always document source URL, access date, and version |
| Sensitive data | Never committed to the repository; use `.gitignore` and environment variables |

---

## 8. Coding Standards

### 8.1 Python Style

- Python 3.10+ throughout
- `pyproject.toml` or `requirements.txt` with **pinned versions** (e.g. `pandas==2.1.4`)
- Vectorised operations preferred; explicit loops only when unavoidable and commented
- Relative imports within the project; no hardcoded paths
- Reproducibility seed set at the top of every script and notebook:

```python
import numpy as np
import random

SEED = 42
np.random.seed(SEED)
random.seed(SEED)
# For PyTorch:
# torch.manual_seed(SEED)
```

### 8.2 Docstring Standard

All functions must include docstrings. Use Google style:

```python
def evaluate_model(model, X_test, y_test, threshold=0.5):
    """
    Evaluate a binary classifier and return marketing-relevant metrics.

    Parameters:
        model: Fitted sklearn-compatible classifier.
        X_test (pd.DataFrame): Test features.
        y_test (pd.Series): True binary labels.
        threshold (float): Decision threshold. Default 0.5.

    Returns:
        dict: AUC, precision, recall, F1, and lift at threshold.

    Notes:
        Lift is computed relative to random baseline. Relevant for
        marketing campaign targeting where base rate matters.
    """
```

### 8.3 Notebook Standards

- Cell 1: imports and seed
- Cell 2: data loading with source comment
- Markdown cells before every major analysis step explaining *why*, not just *what*
- Notebooks must execute top-to-bottom without error before committing
- Use `nbstripout` to strip outputs before committing (reduces diff noise)

---

## 9. Recommended Stack

### Core Scientific
```
pandas>=2.1
numpy>=1.26
scipy>=1.11
statsmodels>=0.14
scikit-learn>=1.3
```

### NLP / Deep Learning
```
transformers>=4.35
sentence-transformers>=2.2
torch>=2.1
```

### Visualisation
```
matplotlib>=3.8
seaborn>=0.13
plotly>=5.18
```

### Teaching & Apps
```
streamlit>=1.28
gradio>=4.0
jupyter>=1.0
quarto  # installed separately
```

### Academic Writing
- Quarto (`.qmd` + `revealjs` / `pdf`)
- LaTeX (journal submissions via Overleaf)
- Zotero + Better BibTeX for references

---

## 10. Claude Behaviour Contract

When operating in this repository, Claude must:

**Always:**
- Prioritise correctness over brevity or speed
- Flag methodological weaknesses explicitly, not passively
- Suggest stronger alternative specifications when identification is weak
- Consider the pedagogical implication of every code choice in teaching contexts
- Ensure outputs can be reused across semesters with minimal editing

**In research contexts:**
- Never let a predictive claim slide as causal
- Always check: is there a confound? Is the identification credible?
- Propose robustness checks alongside main results
- Note when a result is sensitive to specification choice

**In teaching contexts:**
- Always add a plain-English interpretation after technical output
- Prefer interpretable models unless complexity is pedagogically justified
- Include comments that explain *why* a choice was made, not just *what* it does
- Write code a master's student with no prior Python experience can follow

**In ambiguous situations, default in this order:**
1. Interpretability
2. Reproducibility
3. Teaching utility
4. Engineering elegance

---

## 11. Semester Maintenance Protocol

At the start of each semester:

1. Create a new dated folder under `/teaching/` (e.g. `2026_fall/`)
2. Copy only materials being updated — do not delete previous semesters
3. Update module READMEs with current term, cohort size, and any changed datasets
4. Pin new dependency versions in `requirements.txt`
5. Update this `CLAUDE.md` if tooling or conventions change
6. Run all notebooks end-to-end to verify reproducibility before week 1

At the end of each semester:

1. Archive student-facing apps if no longer deployed
2. Commit final versions of all slides and lab notebooks
3. Document any known issues or improvements for next iteration

---

## 12. End Goal

Every output in this repository should ultimately serve one of these four purposes:

| Purpose | Standard |
|---|---|
| Publishable academic paper | Reproducible from raw data, causally defended, journal-ready |
| Teaching material | Clear, reusable, interpretable, accessible to target cohort |
| Interactive demonstration | Fast, explainable, student-facing, deployed via GitHub |
| Empirical pipeline | Modular, documented, version-controlled, portable |

If a piece of work does not clearly serve one of these purposes, it should not be in this repository.
