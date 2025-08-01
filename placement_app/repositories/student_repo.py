from .base_repo import BaseRepo

class StudentRepo(BaseRepo):
    def fetch_with_programming_softskills(self, where_clause="", params=()):
        sql = f"""
        SELECT s.student_id, s.name, s.course_batch,
               AVG(p.problems_solved) AS avg_problems,
               ss.communication, ss.teamwork, ss.presentation,
               pl.placement_status, pl.mock_interview_score, pl.internships_completed
        FROM students s
        JOIN programming p ON s.student_id = p.student_id
        JOIN soft_skills ss ON s.student_id = ss.student_id
        JOIN placements pl ON s.student_id = pl.student_id
        {('WHERE ' + where_clause) if where_clause else ''}
        GROUP BY s.student_id
        ORDER BY avg_problems DESC;
        """
        return self.db.execute(sql, params, fetchall=True)
