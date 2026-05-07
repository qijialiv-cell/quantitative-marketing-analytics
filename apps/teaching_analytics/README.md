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

- **API + Admin Dashboard** → Render (free tier)
- **Feedback Form** → Cloudflare Pages (static HTML)

## Data Schema

SQLite database with three tables:

- `feedback` — course, week, rating (1-5), comment, timestamp
- `questions` — course, week, question text, auto-category, timestamp
- `quiz_responses` — course, week, anonymous_id, answers (JSON), score, timestamp
