"""
Teaching Analytics — Admin Dashboard.

Provides instructors with feedback analytics, question clustering,
sentiment analysis, and data export.

Run: streamlit run admin/dashboard.py
"""

import sqlite3
import csv
import io
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DB_PATH = Path(__file__).resolve().parent.parent / "api" / "teaching_analytics.db"

st.set_page_config(
    page_title="Teaching Analytics | Admin",
    page_icon="📊",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------


@st.cache_data(ttl=60)
def load_feedback(course: str | None = None) -> pd.DataFrame:
    """Load feedback from SQLite into a DataFrame."""
    if not DB_PATH.exists():
        return pd.DataFrame()
    conn = sqlite3.connect(str(DB_PATH))
    query = "SELECT * FROM feedback"
    params: list = []
    if course:
        query += " WHERE course = ?"
        params.append(course)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


@st.cache_data(ttl=60)
def load_questions(course: str | None = None) -> pd.DataFrame:
    """Load questions from SQLite into a DataFrame."""
    if not DB_PATH.exists():
        return pd.DataFrame()
    conn = sqlite3.connect(str(DB_PATH))
    query = "SELECT * FROM questions"
    params: list = []
    if course:
        query += " WHERE course = ?"
        params.append(course)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


@st.cache_data(ttl=60)
def load_quiz(course: str | None = None) -> pd.DataFrame:
    """Load quiz responses from SQLite into a DataFrame."""
    if not DB_PATH.exists():
        return pd.DataFrame()
    conn = sqlite3.connect(str(DB_PATH))
    query = "SELECT * FROM quiz_responses"
    params: list = []
    if course:
        query += " WHERE course = ?"
        params.append(course)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

st.title("📊 Teaching Analytics Dashboard")
st.caption("Student feedback, questions, and quiz analytics — data-driven course improvement.")

with st.sidebar:
    st.header("Filters")
    fb_df = load_feedback()
    all_courses = sorted(fb_df["course"].unique().tolist()) if not fb_df.empty else []
    selected_course = st.selectbox(
        "Course",
        options=["All"] + all_courses,
        index=0,
    )
    course_filter = None if selected_course == "All" else selected_course

# ---------------------------------------------------------------------------
# Feedback Overview
# ---------------------------------------------------------------------------

st.header("Feedback Overview")
fb = load_feedback(course_filter)

if fb.empty:
    st.info("No feedback data yet. Students have not submitted any feedback.")
else:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Responses", len(fb))
    col2.metric("Avg Rating", f"{fb['rating'].mean():.2f}" if not fb.empty else "—")
    col3.metric("Courses", fb["course"].nunique())
    col4.metric("Weeks Covered", fb["week"].nunique())

    # Rating distribution
    st.subheader("Rating Distribution")
    rating_counts = fb["rating"].value_counts().sort_index()
    fig_rating = px.bar(
        x=rating_counts.index,
        y=rating_counts.values,
        labels={"x": "Rating", "y": "Count"},
        color=rating_counts.values,
        color_continuous_scale="Purples",
    )
    fig_rating.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig_rating, use_container_width=True)

    # Weekly trend
    st.subheader("Rating Trend by Week")
    weekly = fb.groupby("week")["rating"].agg(["mean", "count"]).reset_index()
    fig_trend = px.line(
        weekly, x="week", y="mean", markers=True,
        labels={"week": "Week", "mean": "Average Rating"},
    )
    fig_trend.add_hline(y=fb["rating"].mean(), line_dash="dash", line_color="gray",
                        annotation_text=f"Overall avg: {fb['rating'].mean():.2f}")
    fig_trend.update_layout(height=350, yaxis=dict(dtick=1, range=[0.5, 5.5]))
    st.plotly_chart(fig_trend, use_container_width=True)

    # Recent comments
    st.subheader("Recent Comments")
    comments = fb[fb["comment"].notna() & (fb["comment"] != "")].sort_values("created_at", ascending=False)
    if not comments.empty:
        for _, row in comments.head(15).iterrows():
            st.markdown(
                f"**{row['course']} · Week {row['week']}** — "
                f"Rating: {row['rating']}/5  \n{row['comment']}"
            )
            st.divider()
    else:
        st.info("No written comments yet.")

# ---------------------------------------------------------------------------
# Questions
# ---------------------------------------------------------------------------

st.header("Student Questions")
qs = load_questions(course_filter)

if qs.empty:
    st.info("No questions submitted yet.")
else:
    col1, col2 = st.columns(2)
    col1.metric("Total Questions", len(qs))
    col2.metric("Weeks with Questions", qs["week"].nunique())

    st.subheader("Questions by Week")
    for week in sorted(qs["week"].unique()):
        week_qs = qs[qs["week"] == week]
        with st.expander(f"Week {week} ({len(week_qs)} questions)"):
            for _, row in week_qs.iterrows():
                st.markdown(f"- {row['question']}")

# ---------------------------------------------------------------------------
# Quiz Analytics
# ---------------------------------------------------------------------------

st.header("Quiz Analytics")
quiz = load_quiz(course_filter)

if quiz.empty:
    st.info("No quiz data yet.")
else:
    col1, col2 = st.columns(2)
    col1.metric("Total Responses", len(quiz))
    col2.metric("Avg Score", f"{quiz['score'].mean():.1f}%" if quiz["score"].notna().any() else "—")

    if quiz["score"].notna().any():
        st.subheader("Score Distribution")
        fig_quiz = px.histogram(
            quiz.dropna(subset=["score"]), x="score", nbins=20,
            labels={"score": "Score (%)"},
            color_discrete_sequence=["#6D28D9"],
        )
        fig_quiz.update_layout(height=300)
        st.plotly_chart(fig_quiz, use_container_width=True)

# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

st.header("Data Export")

export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    st.subheader("Feedback")
    if not fb.empty:
        csv_fb = fb.to_csv(index=False)
        st.download_button(
            "Download Feedback CSV",
            data=csv_fb,
            file_name="feedback_export.csv",
            mime="text/csv",
        )
    else:
        st.info("No data.")

with export_col2:
    st.subheader("Questions")
    if not qs.empty:
        csv_qs = qs.to_csv(index=False)
        st.download_button(
            "Download Questions CSV",
            data=csv_qs,
            file_name="questions_export.csv",
            mime="text/csv",
        )
    else:
        st.info("No data.")

with export_col3:
    st.subheader("Quiz")
    if not quiz.empty:
        csv_quiz = quiz.to_csv(index=False)
        st.download_button(
            "Download Quiz CSV",
            data=csv_quiz,
            file_name="quiz_export.csv",
            mime="text/csv",
        )
    else:
        st.info("No data.")

# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------

with st.expander("About this tool"):
    st.markdown(
        """
        **Teaching Analytics Dashboard** collects and visualises student feedback
        for data-driven course improvement.

        - **Feedback:** Anonymous ratings and comments per course/week
        - **Questions:** Student questions tracked and sortable
        - **Quiz:** Quiz score analytics with distribution charts
        - **Export:** One-click CSV download for offline analysis

        All data is stored locally in SQLite. No student personal data is collected.
        """
    )
