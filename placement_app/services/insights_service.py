class InsightsService:
    def __init__(self, db):
        self.db = db

    def run(self, sql: str, params=()):
        return self.db.execute(sql, params, fetchall=True)
