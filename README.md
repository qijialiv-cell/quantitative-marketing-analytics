# Quantitative Marketing & Marketing Analytics — Research & Teaching Workspace
**University of Liverpool | Marketing Department**

A long-term academic workspace for teaching, research, and interactive demonstrations
in quantitative marketing, marketing analytics, NLP, and applied machine learning.

Maintained by [Qijia Liao](https://scholar.google.com/citations?user=s2lwLxMAAAAJ) —
PhD in Marketing, University of Liverpool Management School.

---

## Repository Structure

```
/
├── teaching/                    Semester-organised lecture slides, labs, assignments
│   └── 2026_spring/             Current semester (never overwrite previous)
├── research/                    Paper-level empirical pipelines
│   ├── paper_brand_activism/
│   ├── paper_influencer_ml/
│   └── paper_causal_nlp/
├── apps/                        Interactive teaching tools and ML demos
│   ├── churn_predictor/         Streamlit app (Render)
│   ├── embedding_explorer/      Gradio app (Hugging Face Spaces)
│   ├── teaching_analytics/      FastAPI backend + Streamlit admin (Render)
│   └── hct-ml-marketing-lab.html    HCT Digital Marketing lab (Cloudflare Pages)
├── quarto/                      Academic website and shared Quarto assets
├── scripts/                     Shared utility functions
└── .github/workflows/           CI/CD deployment pipelines
```

## Quick Start

```bash
# Clone
git clone <repo-url>
cd academic_repo

# Install dependencies
pip install -r requirements.txt

# Run a teaching app
cd apps/churn_predictor
streamlit run app.py

# Run the Teaching Analytics backend
cd apps/teaching_analytics
uvicorn api.main:app --reload

# Run the admin dashboard
cd apps/teaching_analytics
streamlit run admin/dashboard.py

# Build the Quarto site locally
cd quarto/website
quarto preview
```

---

## Deployment Architecture

This repository uses a **four-platform stack** — each platform chosen for its
strength, all on **free tiers**. Every deployment is GitHub-driven: push to `main`
and the correct platform picks up the change.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│              UNIFIED ACADEMIC SITE                                          │
│              qijialiao.com (Cloudflare)                                     │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  LAYER 1 — ACADEMIC PORTAL (Cloudflare Pages)                         │  │
│  │                                                                        │  │
│  │  qijialiao.com                                                        │  │
│  │  ├── /                   → Quarto academic homepage                   │  │
│  │  │                          (Google Scholar, ORCID, publications)      │  │
│  │  ├── /slides/             → Teaching slide decks                      │  │
│  │  ├── /labs/               → Static HTML labs                          │  │
│  │  │   └── /hct-ml-lab/    → 🔒 Cloudflare Access                      │  │
│  │  └── /feedback/           → Student feedback form → Layer 4 API      │  │
│  │                                                                        │  │
│  │  Legacy: qijialiv-cell.github.io/me/ → 301 redirect to qijialiao.com │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                     │                                       │
│                                     │ API calls                             │
│                                     ▼                                       │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  LAYER 2 — FRONTEND DASHBOARDS (Vercel)                               │  │
│  │                                                                        │  │
│  │  dash.qijialiao.com                                                   │  │
│  │  ├── Student Dashboard      → React interactive visualisation tools   │  │
│  │  └── Teaching Analytics     → 📊 Instructor analytics dashboard       │  │
│  │       ├── Student feedback sentiment analysis (NLP)                    │  │
│  │       ├── Weekly/session feedback trends                               │  │
│  │       ├── FAQ clustering (auto-grouped by topic)                      │  │
│  │       └── One-click CSV / JSON export                                  │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  LAYER 3 — ML DEMOS (Hugging Face Spaces)                             │  │
│  │  hf.space/qijialiao/*                                                 │  │
│  │  → Gradio research prototypes, embedded via iframe                    │  │
│  │  → Churn predictor, embedding explorer, model demos                   │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  LAYER 4 — BACKEND + TEACHING ANALYTICS (Render)                      │  │
│  │                                                                        │  │
│  │  api.qijialiao.com                                                    │  │
│  │  ├── FastAPI backend                                                  │  │
│  │  │   ├── POST /feedback        ← Student feedback/questions           │  │
│  │  │   ├── GET  /feedback/stats  → Dashboard statistics                 │  │
│  │  │   ├── GET  /feedback/export → CSV/JSON download                    │  │
│  │  │   ├── POST /quiz-response  ← Quiz result collection               │  │
│  │  │   └── GET  /analytics/...   → NLP analysis endpoints               │  │
│  │  │                                                                    │  │
│  │  ├── SQLite database (Render free disk)                               │  │
│  │  │   ├── feedback:   course, week, rating, comment, timestamp         │  │
│  │  │   ├── questions:  course, week, question, category (auto)          │  │
│  │  │   ├── quiz:       course, week, student_id, answers, score         │  │
│  │  │   └── students:   anonymous_id, course, engagement_score           │  │
│  │  │                                                                    │  │
│  │  └── Streamlit Admin Panel (🔒 Cloudflare Access)                     │  │
│  │      ├── Feedback overview + sentiment analysis                        │  │
│  │      ├── Question clustering + keyword clouds                         │  │
│  │      ├── Data-driven course adjustment suggestions                     │  │
│  │      └── One-click data export (CSV / JSON)                           │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Student Data Flow

```
HTML Lab / Course Page  →  Feedback Form  →  FastAPI (Render)  →  SQLite DB
                                                                        │
Admin Dashboard  ←  Analytics API  ←  NLP Analysis  ←  ─────────────────┘
```

### Access Control

- **Public:** academic homepage, publications, Google Scholar
- **🔒 Cloudflare Access** (free, up to 50 users): unpublished courses,
  internal labs, admin dashboard
- Students authenticate via email — no LMS dependency, no JS password hacks

### Platform Decision Rules

| Platform | Use when | Free tier |
|----------|----------|-----------|
| **Cloudflare Pages** | Static Quarto site, slides, HTML labs | Unlimited bandwidth, 500 builds/mo |
| **Vercel** | React/Next.js dashboards with non-trivial frontend logic | 100 GB bandwidth/mo |
| **Hugging Face Spaces** | Gradio ML model demos, embedding explorers | Free CPU instances |
| **Render** | Python backends (FastAPI, Streamlit), scheduled jobs, persistent storage | 750 hrs/mo (cold start on idle) |

### Asset → Platform Mapping

| Asset | Platform | Trigger |
|-------|----------|---------|
| Academic website (`quarto/website/`) | Cloudflare Pages | push to `main` |
| Lecture slides (`teaching/*/slides/`) | Cloudflare Pages | push to `main` |
| HCT ML Lab (`apps/hct-ml-marketing-lab.html`) | Cloudflare Pages | push to `main` |
| Student feedback form | Cloudflare Pages | push to `main` |
| Student dashboard (React) | Vercel | push to `main` |
| Teaching analytics dashboard | Vercel | push to `main` |
| Churn predictor demo (Gradio) | Hugging Face Spaces | GitHub Action |
| Embedding explorer (Gradio) | Hugging Face Spaces | GitHub Action |
| Teaching Analytics API (FastAPI) | Render | push to `main` |
| Admin dashboard (Streamlit) | Render | push to `main` |
| Sentiment classifier API (FastAPI) | Render | push to `main` |

### Required GitHub Secrets

```
# Cloudflare Pages
CLOUDFLARE_API_TOKEN
CLOUDFLARE_ACCOUNT_ID

# Vercel
VERCEL_TOKEN
VERCEL_ORG_ID
VERCEL_PROJECT_ID

# Hugging Face Spaces
HF_TOKEN

# Render
RENDER_API_KEY
```

---

## Teaching Analytics System

The Teaching Analytics system collects student feedback, questions, and quiz responses,
then provides NLP-powered analysis to help instructors adjust course content in real time.

### Features

- **Feedback collection:** rating + free-text comments per course/week
- **Question tracking:** student questions auto-categorised by topic
- **Quiz analytics:** quiz scores aggregated by question and topic
- **Sentiment analysis:** automated NLP on feedback text
- **Question clustering:** frequent topics surfaced automatically
- **Data export:** CSV/JSON download for offline analysis

### Data Schema

```sql
-- Student feedback
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    course TEXT NOT NULL,
    week INTEGER NOT NULL,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    comment TEXT,
    sentiment_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Student questions
CREATE TABLE questions (
    id INTEGER PRIMARY KEY,
    course TEXT NOT NULL,
    week INTEGER NOT NULL,
    question TEXT NOT NULL,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quiz responses
CREATE TABLE quiz_responses (
    id INTEGER PRIMARY KEY,
    course TEXT NOT NULL,
    week INTEGER NOT NULL,
    anonymous_id TEXT NOT NULL,
    answers JSON NOT NULL,
    score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Academic Identity

| Platform | URL |
|----------|-----|
| Academic site | `qijialiao.com` (Cloudflare Pages) |
| Google Scholar | [Qijia Liao](https://scholar.google.com/citations?user=s2lwLxMAAAAJ) |
| GitHub | [qijialiv-cell](https://github.com/qijialiv-cell) |
| Legacy site | `qijialiv-cell.github.io/me/` → redirects to `qijialiao.com` |

---

## Semester Maintenance

See `CLAUDE.md` for the full operating contract and maintenance protocol.

- **Start of term:** create a new dated folder under `/teaching/`, pin dependencies,
  run all notebooks end-to-end before week 1
- **End of term:** commit final versions, archive deployed apps, document improvements
- **Never overwrite previous semesters** — always version forward

## Coding Standards

- Python 3.10+, pinned dependencies in `requirements.txt`
- Reproducibility seed (`SEED = 42`) at the top of every script and notebook
- Google-style docstrings on all functions
- `nbstripout` before committing notebooks
