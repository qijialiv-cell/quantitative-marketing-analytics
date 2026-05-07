# Computational Marketing Research & Teaching Repository
**University of Liverpool — Marketing Department**

A semester-maintained academic workspace for teaching, research, and interactive demonstrations
in computational marketing.

---

## Structure

```
/teaching/          Semester-organised lecture slides, labs, assignments
/research/          Paper-level empirical pipelines
/apps/              Streamlit and Gradio interactive tools
/quarto/            Academic website and shared Quarto assets
/scripts/           Shared utility functions
/outputs/           Shared figures and tables
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

# Build the Quarto site locally
cd quarto/website
quarto preview
```

## Deployment Map

| Asset | Platform | Trigger |
|---|---|---|
| Academic website | Cloudflare Pages | push to `main` |
| Lecture slides | Cloudflare Pages | push to `main` |
| Streamlit apps | Render | push to `main` |
| Gradio ML demos | Hugging Face Spaces | GitHub Action |
| React dashboards | Vercel | push to `main` |

## Semester Maintenance

See `CLAUDE.md` §11 for the full maintenance protocol.
At the start of each term: create a new dated folder under `/teaching/`, pin dependencies, run all notebooks end-to-end.
