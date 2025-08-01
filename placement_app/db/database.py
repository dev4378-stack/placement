import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_conn(self):
        return sqlite3.connect(self.db_path)

    def execute(self, sql, params=(), fetchone=False, fetchall=False):
        con = self.get_conn()
        cur = con.cursor()
        cur.execute(sql, params)
        data = None
        if fetchone:
            data = cur.fetchone()
        if fetchall:
            data = cur.fetchall()
        con.commit()
        con.close()
        return data

    def execute_script(self, script: str):
        con = self.get_conn()
        cur = con.cursor()
        cur.executescript(script)  # <-- This handles multiple CREATE TABLEs at once
        con.commit()
        con.close()
