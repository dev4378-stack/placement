PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS students (
  student_id INTEGER PRIMARY KEY,
  name TEXT,
  age INTEGER,
  gender TEXT,
  email TEXT,
  phone TEXT,
  enrollment_year INTEGER,
  course_batch TEXT,
  city TEXT,
  graduation_year INTEGER
);

CREATE TABLE IF NOT EXISTS programming (
  programming_id INTEGER PRIMARY KEY,
  student_id INTEGER NOT NULL,
  language TEXT NOT NULL,
  problems_solved INTEGER,
  assessments_completed INTEGER,
  mini_projects INTEGER,
  certifications_earned INTEGER,
  latest_project_score REAL,
  FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS soft_skills (
  soft_skill_id INTEGER PRIMARY KEY,
  student_id INTEGER NOT NULL,
  communication INTEGER,
  teamwork INTEGER,
  presentation INTEGER,
  leadership INTEGER,
  critical_thinking INTEGER,
  interpersonal_skills INTEGER,
  FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS placements (
  placement_id INTEGER PRIMARY KEY,
  student_id INTEGER NOT NULL,
  mock_interview_score INTEGER,
  internships_completed INTEGER,
  placement_status TEXT,
  company_name TEXT,
  placement_package REAL,
  interview_rounds_cleared INTEGER,
  placement_date TEXT,
  FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
);
