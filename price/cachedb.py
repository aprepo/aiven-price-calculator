import sqlite3
import errors
import tables


class CacheDB(object):
    def __init__(self, path=":memory:"):
        self.path = path
        self.db = sqlite3.connect(self.path)
        #self.db.execute("""
        #    CREATE TABLE IF NOT EXISTS plans (
        #        project_name TEXT,
        #        service_type TEXT,
        #        plan TEXT,
        #        region TEXT,
        #        price REAL
        #    );
        #    """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                project_name TEXT PRIMARY KEY,
                billing_group_id TEXT
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
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                billing_group_id TEXT,
                billing_group_name TEXT,
                project_id TEXT,
                invoice_id TEXT,
                period_start TEXT,
                period_end TEXT,
                state TEXT,
                total_inc_vat REAL,
                total_vat_zero REAL,
                currency TEXT
            )
            """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS line_items (
                billing_group_id TEXT,
                invoice_id TEXT,
                project TEXT,
                service_name TEXT,
                service_type TEXT,
                plan TEXT,
                cloud TEXT,
                description TEXT,
                total_usd REAL,
                total_local REAL,
                currency TEXT,
                period_start TEXT,
                period_end TEXT
            )
            """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS billing_groups(
                id TEXT,
                name TEXT,
                account_id TEXT,
                account_name TEXT,
                currency TEXT,
                payment_method TEXT,
                estimated_balance_local REAL,
                estimated_balance_usd REAL
            )
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

    def insert_project(self, project_name, billing_group_id):
        print(f"PROJECT: {project_name}: {billing_group_id}")
        self.db.execute(
            """INSERT INTO projects (project_name, billing_group_id) VALUES(?, ?)""",
            (
                project_name,
                billing_group_id
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

    def insert_invoice(self, billing_group_id, billing_group_name, project_id, invoice_id, period_start, period_end,
                       state, total_inc_vat, total_vat_zero, currency):
        self.db.execute(
            """
            INSERT INTO invoices (billing_group_id, billing_group_name, project_id, invoice_id, period_start, period_end, state, total_inc_vat, 
                total_vat_zero, currency)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
            """,
            (
                billing_group_id,
                billing_group_name,
                project_id,
                invoice_id,
                period_start,
                period_end,
                state,
                total_inc_vat,
                total_vat_zero,
                currency
            )
        )

    def insert_line_item(self, billing_group_id, invoice_id, project, service_name, service_type, plan, cloud,
                         description, total_usd, total_local, currency, period_start, period_end):
        self.db.execute(
            """
            INSERT INTO line_items (
                billing_group_id,
                invoice_id,
                project,
                service_name,
                service_type,
                plan,
                cloud,
                description,
                total_usd,
                total_local,
                currency,
                period_start,
                period_end
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                billing_group_id,
                invoice_id,
                project,
                service_name,
                service_type,
                plan,
                cloud,
                description,
                total_usd,
                total_local,
                currency,
                period_start,
                period_end
            )
        )

    def insert_billing_group(self, id, name, account_id, account_name, currency, payment_method,
                             estimated_balance_local, estimated_balance_usd):
        self.db.execute(
            """
            INSERT INTO billing_groups (
                id, name, account_id, account_name, currency, payment_method,
                estimated_balance_local, estimated_balance_usd
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                id,
                name,
                account_id,
                account_name,
                currency,
                payment_method,
                estimated_balance_local,
                estimated_balance_usd
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

    def get_invoice_count(self):
        curr = self.db.cursor()
        curr.execute("SELECT count(*) FROM invoices")
        count = curr.fetchone()
        return count[0]

    def get_billing_groups_count(self):
        curr = self.db.cursor()
        curr.execute("SELECT count(*) FROM billing_groups")
        count = curr.fetchone()
        return count[0]

    def get_line_items_count(self):
        curr = self.db.cursor()
        curr.execute("SELECT count(*) FROM line_items")
        count = curr.fetchone()
        return count[0]

    def get_projects(self):
        curr = self.db.cursor()
        try:
            curr.execute("SELECT project_name, billing_group_id FROM projects")
            result = curr.fetchall()
        finally:
            curr.close()
        return result

    def get_unknown_line_items(self):
        curr = self.db.cursor()
        curr.execute("SELECT count(*) FROM line_items WHERE service_name='UNKNOWN'")
        return curr.fetchone()[0]

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

    def get_project_invoices(self, project_id):
        curr = self.db.cursor()
        curr.execute("SELECT * from invoices WHERE project_id=?", (project_id,))
        # TODO use Row here
        return [_invoice_dict(invoice) for invoice in curr.fetchall()]


def _invoice_dict(invoice):
    return {
        "billing_group_id": invoice[0],
        "billing_group_name": invoice[1],
        "project_id": invoice[2],
        "invoice_id": invoice[3],
        "period_start": invoice[4],
        "period_end": invoice[5],
        "state": invoice[6],
        "total_inc_vat": invoice[7],
        "total_vat_zero": invoice[8],
        "currency": invoice[9]

    }


def init(path) -> CacheDB:
    return CacheDB(path=path)
