import sqlite3


class CacheDB(object):
    def __init__(self):
        self.db = sqlite3.connect(':memory:')
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                service_type TEXT,
                plan TEXT,
                region TEXT,
                price REAL 
            );
            """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                project_name TEXT PRIMARY KEY
            );
            """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS services (
                project_name TEXT,
                service_name,
                service_type,
                plan,
                region
            )
        """)

    def insert_plan(self, service_type, plan, region, price):
        self.db.execute(
            """INSERT INTO plans (service_type,plan,region,price) VALUES(?,?,?,?)""",
            (
                service_type,
                plan,
                region,
                price,
            )
        )

    def insert_project(self, project_name):
        self.db.execute(
            """INSERT INTO projects (project_name) VALUES(?)""",
            (
                project_name,
            )
        )

    def get_project_count(self):
        curr = self.db.cursor()
        curr.execute("SELECT count(*) FROM projects;")
        count = curr.fetchone()
        return count[0]

    def get_plan_count(self):
        curr = self.db.cursor()
        curr.execute("SELECT count(*) FROM plans;")
        count = curr.fetchone()
        return count[0]

    def get_service_count(self):
        return 0


def init() -> CacheDB:
    return CacheDB()
