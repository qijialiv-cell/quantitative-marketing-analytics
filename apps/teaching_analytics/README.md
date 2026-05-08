# Teaching Analytics

Feedback collection and analytics system for data-driven course improvement.

## Components

| Component | Tech | Description |
|-----------|------|-------------|
| `api/main.py` | FastAPI | REST API backend for collecting feedback, questions, quiz responses |
| `feedback_form.html` | Static HTML | Student-facing feedback form (deploy to Cloudflare Pages) |
| `admin/dashboard.py` | Streamlit | Instructor analytics dashboard with export |

## Local Development

```bash
# Install dependencies
pip install fastapi uvicorn sqlite3 pandas streamlit plotly

# Run API backend
cd apps/teaching_analytics
uvicorn api.main:app --reload

# Run admin dashboard (separate terminal)
cd apps/teaching_analytics
streamlit run admin/dashboard.py
```

## Deployment

- **API backend** → Render web service (`uvicorn api.main:app`)
- **Admin dashboard** → Render web service separate deployment (`streamlit run admin/dashboard.py`)
- **Feedback form** → Cloudflare Pages (static HTML)

### Render Deployment Notes

⚠️ **Python Version:** Set to 3.11 to ensure pandas wheels are pre-built (avoids compilation timeouts)

The `requirements.txt` in this directory includes only necessary dependencies:
- FastAPI, Uvicorn (API)
- Streamlit, Plotly, Pandas (Admin dashboard)
- No heavy ML libraries (torch, transformers, etc.)

This ensures faster builds and avoids timeouts on Render's free tier.
- **Feedback Form** → Cloudflare Pages (static HTML)

## Data Schema

SQLite database with three tables:

- `feedback` — course, week, rating (1-5), comment, timestamp
- `questions` — course, week, question text, auto-category, timestamp
- `quiz_responses` — course, week, anonymous_id, answers (JSON), score, timestamp
