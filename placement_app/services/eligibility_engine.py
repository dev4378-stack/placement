class EligibilityEngine:
    FIELD_MAP = {
        'min_problems': ('p.problems_solved', '>='),
        'min_soft_comm': ('ss.communication', '>='),
        'min_soft_team': ('ss.teamwork', '>='),
        'min_mock': ('pl.mock_interview_score', '>='),
        'min_internships': ('pl.internships_completed', '>=')
    }

    def build(self, criteria: dict):
        clauses, params = [], []
        for key, val in criteria.items():
            if val is None or val == '':
                continue
            if key in self.FIELD_MAP:
                col, op = self.FIELD_MAP[key]
                clauses.append(f"{col} {op} ?")
                params.append(val)
            elif key == 'status' and val:
                clauses.append("pl.placement_status = ?")
                params.append(val)
            elif key == 'batch' and val:
                clauses.append("s.course_batch = ?")
                params.append(val)
        return ' AND '.join(clauses), params
