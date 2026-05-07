"""
Teaching Analytics API — FastAPI backend for collecting and analysing
student feedback, questions, and quiz responses.

Run: uvicorn api.main:app --reload
"""

import json
import csv
import io
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import sqlite3

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

DB_PATH = Path(__file__).resolve().parent / "teaching_analytics.db"


def get_db():
    """Return a sqlite3 connection with row factory."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they do not exist."""
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT NOT NULL,
            week INTEGER NOT NULL,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            comment TEXT,
            sentiment_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT NOT NULL,
            week INTEGER NOT NULL,
            question TEXT NOT NULL,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS quiz_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT NOT NULL,
            week INTEGER NOT NULL,
            anonymous_id TEXT NOT NULL,
            answers TEXT NOT NULL,
            score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class FeedbackCreate(BaseModel):
    course: str = Field(..., description="Course code, e.g. MKIB340")
    week: int = Field(..., ge=1, le=20, description="Teaching week number")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 (poor) to 5 (excellent)")
    comment: str | None = Field(None, description="Optional free-text comment")


class QuestionCreate(BaseModel):
    course: str = Field(..., description="Course code")
    week: int = Field(..., ge=1, le=20, description="Teaching week number")
    question: str = Field(..., description="Student question text")


class QuizResponseCreate(BaseModel):
    course: str = Field(..., description="Course code")
    week: int = Field(..., ge=1, le=20, description="Teaching week number")
    anonymous_id: str = Field(..., description="Anonymous student identifier")
    answers: dict = Field(..., description="Question-answer mapping, e.g. {\"q1\": \"a\", \"q2\": \"c\"}")
    score: float | None = Field(None, ge=0, le=100, description="Percentage score")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

# Initialise database eagerly so tables exist before any request
init_db()

app = FastAPI(
    title="Teaching Analytics API",
    description="Collect and analyse student feedback for data-driven course improvement.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ---------------------------------------------------------------------------
# Feedback endpoints
# ---------------------------------------------------------------------------


@app.post("/feedback", status_code=201)
def submit_feedback(payload: FeedbackCreate):
    """Submit student feedback for a course session."""
    conn = get_db()
    conn.execute(
        "INSERT INTO feedback (course, week, rating, comment) VALUES (?, ?, ?, ?)",
        (payload.course, payload.week, payload.rating, payload.comment),
    )
    conn.commit()
    conn.close()
    return {"status": "ok", "message": "Feedback recorded."}


@app.get("/feedback/stats")
def feedback_stats(
    course: str | None = Query(None, description="Filter by course code"),
    week: int | None = Query(None, description="Filter by week number"),
):
    """Return aggregated feedback statistics."""
    conn = get_db()
    query = "SELECT rating, comment, week, course, created_at FROM feedback WHERE 1=1"
    params: list = []
    if course:
        query += " AND course = ?"
        params.append(course)
    if week:
        query += " AND week = ?"
        params.append(week)

    rows = conn.execute(query, params).fetchall()
    conn.close()

    if not rows:
        return {"total": 0, "avg_rating": None, "by_week": {}, "recent_comments": []}

    ratings = [r["rating"] for r in rows if r["rating"] is not None]
    by_week: dict[str, list] = {}
    for r in rows:
        key = str(r["week"])
        by_week.setdefault(key, []).append(r["rating"])

    week_avgs = {k: round(sum(v) / len(v), 2) for k, v in by_week.items()}

    recent = [
        {"comment": r["comment"], "rating": r["rating"], "week": r["week"], "date": r["created_at"]}
        for r in rows[-20:]
        if r["comment"]
    ]

    return {
        "total": len(rows),
        "avg_rating": round(sum(ratings) / len(ratings), 2) if ratings else None,
        "by_week": week_avgs,
        "recent_comments": recent,
    }


@app.get("/feedback/export")
def export_feedback(
    course: str | None = Query(None),
    week: int | None = Query(None),
    format: str = Query("json", regex="^(json|csv)$"),
):
    """Export feedback data as JSON or CSV."""
    conn = get_db()
    query = "SELECT * FROM feedback WHERE 1=1"
    params: list = []
    if course:
        query += " AND course = ?"
        params.append(course)
    if week:
        query += " AND week = ?"
        params.append(week)

    rows = conn.execute(query, params).fetchall()
    conn.close()

    data = [dict(r) for r in rows]

    if format == "csv":
        if not data:
            raise HTTPException(status_code=404, detail="No data to export.")
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return {"format": "csv", "data": output.getvalue()}

    return {"format": "json", "data": data}


# ---------------------------------------------------------------------------
# Question endpoints
# ---------------------------------------------------------------------------


@app.post("/questions", status_code=201)
def submit_question(payload: QuestionCreate):
    """Submit a student question."""
    conn = get_db()
    conn.execute(
        "INSERT INTO questions (course, week, question) VALUES (?, ?, ?)",
        (payload.course, payload.week, payload.question),
    )
    conn.commit()
    conn.close()
    return {"status": "ok", "message": "Question recorded."}


@app.get("/questions")
def list_questions(
    course: str | None = Query(None),
    week: int | None = Query(None),
):
    """List submitted questions, optionally filtered."""
    conn = get_db()
    query = "SELECT * FROM questions WHERE 1=1"
    params: list = []
    if course:
        query += " AND course = ?"
        params.append(course)
    if week:
        query += " AND week = ?"
        params.append(week)

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return {"questions": [dict(r) for r in rows]}


# ---------------------------------------------------------------------------
# Quiz endpoints
# ---------------------------------------------------------------------------


@app.post("/quiz", status_code=201)
def submit_quiz(payload: QuizResponseCreate):
    """Submit a quiz response."""
    conn = get_db()
    conn.execute(
        "INSERT INTO quiz_responses (course, week, anonymous_id, answers, score) VALUES (?, ?, ?, ?, ?)",
        (payload.course, payload.week, payload.anonymous_id, json.dumps(payload.answers), payload.score),
    )
    conn.commit()
    conn.close()
    return {"status": "ok", "message": "Quiz response recorded."}


@app.get("/quiz/stats")
def quiz_stats(
    course: str | None = Query(None),
    week: int | None = Query(None),
):
    """Return aggregated quiz statistics."""
    conn = get_db()
    query = "SELECT * FROM quiz_responses WHERE 1=1"
    params: list = []
    if course:
        query += " AND course = ?"
        params.append(course)
    if week:
        query += " AND week = ?"
        params.append(week)

    rows = conn.execute(query, params).fetchall()
    conn.close()

    if not rows:
        return {"total": 0, "avg_score": None, "by_week": {}}

    scores = [r["score"] for r in rows if r["score"] is not None]
    by_week: dict[str, list] = {}
    for r in rows:
        key = str(r["week"])
        by_week.setdefault(key, []).append(r["score"])

    week_avgs = {k: round(sum(v) / len(v), 2) for k, v in by_week.items()}

    return {
        "total": len(rows),
        "avg_score": round(sum(scores) / len(scores), 2) if scores else None,
        "by_week": week_avgs,
    }


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
