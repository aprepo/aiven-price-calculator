import sqlite3
import errors


class CacheDB(object):
    def __init__(self):
        self.db = sqlite3.connect(':memory:')
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                project_name TEXT,
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
                service_name TEXT,
                service_type TEXT,
                plan TEXT,
                cloud TEXT,
                price REAL
            );
            """)

    def insert_plan(self, project_name, service_type, plan, region, price):
        self.db.execute(
            """INSERT INTO plans (project_name, service_type,plan,region,price) VALUES(?,?,?,?,?)""",
            (
                project_name,
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

    def insert_service(self, project_name, service_name, service_type, plan, cloud, price):
        self.db.execute(
            """
            INSERT INTO services (project_name, service_name, service_type, plan, cloud, price)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                project_name,
                service_name,
                service_type,
                plan,
                cloud,
                price,
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
        curr = self.db.cursor()
        curr.execute("SELECT count(*) FROM services;")
        count = curr.fetchone()
        return count[0]

    def get_projects(self):
        curr = self.db.cursor()
        try:
            curr.execute("SELECT project_name FROM projects")
            result = curr.fetchall()
        finally:
            curr.close()
        return result

    def get_price_for_service(self, project_name, service_type, plan, region):
        curr = self.db.cursor()
        try:
            curr.execute(
                "SELECT price FROM plans WHERE project_name=? AND service_type=? AND plan=? AND region=?",
                (
                    project_name,
                    service_type,
                    plan,
                    region,
                )
            )
            result = curr.fetchone()
            if result:
                return result[0]
            else:
                raise errors.NoPriceForPlanError(f"No price for service: {project_name}:{service_type}:{plan}:{region}")
        finally:
            curr.close()

    def get_total_spend(self):
        curr = self.db.cursor()
        curr.execute(
            """
            SELECT project_name, sum(price) as hourly, sum(price) * 730 as monthly FROM services GROUP BY project_name;
            """
        )
        return curr.fetchall()


def init() -> CacheDB:
    return CacheDB()
