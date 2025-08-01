import streamlit as st
import pandas as pd
import os

from db.database import DatabaseManager
from db import seed_data
from repositories.student_repo import StudentRepo
from services.eligibility_engine import EligibilityEngine
from services.insights_service import InsightsService

DB_PATH = 'students.db'

# Initialize database if not exists
def init_db():
    if not os.path.exists(DB_PATH):
        db = DatabaseManager(DB_PATH)
        with open('db/schema.sql') as f:
            sql_script = f.read()
            db.execute_script(sql_script)  # ✅ fixed: use executescript()
        seed_data.seed(DB_PATH, 300)  # Generate 300 fake student records

# Create the DB and seed data
init_db()

# Streamlit UI setup
st.set_page_config(page_title="Placement Eligibility", layout="wide")
st.title("🎓 Placement Eligibility Dashboard")

# Sidebar Filters
st.sidebar.header("Eligibility Criteria")
criteria = {
    'min_problems': st.sidebar.number_input("Min Problems Solved (any language)", 0, 400, 100),
    'min_soft_comm': st.sidebar.number_input("Min Communication Score", 0, 100, 60),
    'min_soft_team': st.sidebar.number_input("Min Teamwork Score", 0, 100, 60),
    'min_mock': st.sidebar.number_input("Min Mock Interview Score", 0, 100, 50),
    'min_internships': st.sidebar.number_input("Min Internships", 0, 5, 0),
    'status': st.sidebar.selectbox("Placement Status", ['', 'Ready', 'Placed', 'Not Ready']),
    'batch': st.sidebar.text_input("Batch (e.g. DS-2023A)")
}

if st.sidebar.button("Apply Filters"):
    applied = True
else:
    applied = False

# Connect DB + Fetch Data
col1, col2 = st.columns([3, 2])
with col1:
    st.subheader("Eligible Students")
    db = DatabaseManager(DB_PATH)
    repo = StudentRepo(db)
    engine = EligibilityEngine()
    where, params = engine.build(criteria if applied else {})
    rows = repo.fetch_with_programming_softskills(where, params)

    df = pd.DataFrame(rows, columns=[
        "ID", "Name", "Batch", "Avg Problems", "Comm", "Team", "Presentation", "Status", "Mock Score", "Internships"
    ])
    
    st.dataframe(df, use_container_width=True)
    st.download_button("Download CSV", df.to_csv(index=False), "eligible_students.csv", "text/csv")

with col2:
    st.subheader("KPIs")
    if len(rows):
        st.metric("Eligible Count", len(rows))
        st.metric("Avg Problems (Eligible)", round(df["Avg Problems"].mean(), 1))
        st.metric("Avg Mock Score", round(df["Mock Score"].mean(), 1))
    else:
        st.info("No students match the selected criteria.")

# Insights Section
st.markdown("---")
st.header("📊 Insights")

ins = InsightsService(DatabaseManager(DB_PATH))
INSIGHT_QUERIES = {
    "Avg Problems by Batch":
        "SELECT s.course_batch, ROUND(AVG(p.problems_solved),2) FROM students s JOIN programming p ON s.student_id=p.student_id GROUP BY s.course_batch",
    "Placement Status Breakdown":
        "SELECT placement_status, COUNT(*) FROM placements GROUP BY placement_status",
    "Top 5 Placement Ready":
        "SELECT s.name, (pl.mock_interview_score + AVG(p.problems_solved)/4) AS score FROM students s JOIN programming p ON s.student_id=p.student_id JOIN placements pl ON s.student_id=pl.student_id GROUP BY s.student_id ORDER BY score DESC LIMIT 5"
}

choice = st.selectbox("Select Insight", list(INSIGHT_QUERIES.keys()))
res = ins.run(INSIGHT_QUERIES[choice])
if res:
    df_ins = pd.DataFrame(res)
    st.dataframe(df_ins, use_container_width=True)
else:
    st.warning("No data available.")

