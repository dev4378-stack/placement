from faker import Faker
import random, sqlite3, datetime

BATCHES = ["DS-2023A", "DS-2024A"]
LANGUAGES = ["Python", "SQL"]
PLACEMENT_STATUSES = ["Not Ready", "Ready", "Placed"]

def seed(db_path: str, n_students: int = 300):
    fake = Faker()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    for sid in range(1, n_students + 1):
        name = fake.name()
        age = random.randint(20, 27)
        gender = random.choice(["Male", "Female", "Other"])
        email = f"student{sid}@example.com"
        phone = fake.msisdn()[:10]
        enroll_year = random.choice([2022, 2023])
        batch = random.choice(BATCHES)
        city = fake.city()
        grad_year = enroll_year + 4
        cur.execute("INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?)",
            (sid, name, age, gender, email, phone, enroll_year, batch, city, grad_year))

        for lang in LANGUAGES:
            cur.execute("""INSERT INTO programming (student_id, language, problems_solved, assessments_completed, mini_projects, certifications_earned, latest_project_score)
                VALUES (?,?,?,?,?,?,?)""",
                (sid, lang, random.randint(0, 400), random.randint(0, 12), random.randint(0, 6), random.randint(0, 3), random.uniform(30, 100)))

        cur.execute("""INSERT INTO soft_skills (student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills)
            VALUES (?,?,?,?,?,?,?)""",
            (sid, *(random.randint(30, 100) for _ in range(6))))

        status = random.choices(PLACEMENT_STATUSES, weights=[0.4, 0.4, 0.2])[0]
        company = fake.company() if status == "Placed" else None
        package = random.uniform(4, 30) if status == "Placed" else None
        rounds = random.randint(0, 5)
        date = (datetime.date.today() - datetime.timedelta(days=random.randint(0, 400))).isoformat() if status == "Placed" else None
        cur.execute("""INSERT INTO placements (student_id, mock_interview_score, internships_completed, placement_status, company_name, placement_package, interview_rounds_cleared, placement_date)
            VALUES (?,?,?,?,?,?,?,?)""",
            (sid, random.randint(0, 100), random.randint(0, 3), status, company, package, rounds, date))

    con.commit()
    con.close()
