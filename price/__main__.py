import aiven
import cachedb
from report import console
#from piccolo.engine.sqlite import SQLiteEngine
from tables import Plan

print("Initiating cache...")
db = cachedb.init(path='/tmp/cache.db')         # pure sqlite
# Piccolo version
Plan.create_table().run_sync()


aiven.dump_settings()

print("Loading data...")
aiven.get_billing_groups(db)
aiven.get_projects(db)
for (project, billing_group_id, ) in db.get_projects():
    print(f"Project : {project}...")
    aiven.get_prices(db=db, project=project)
    aiven.get_services(db=db, project=project)
    aiven.get_invoices(db=db, project=project, billing_group_id=billing_group_id)
    for invoice in db.get_project_invoices(project_id=project):
        aiven.get_invoice_line_items(
            db=db,
            project=project,
            billing_group_id=invoice['billing_group_id'],
            invoice_id=invoice['invoice_id']
        )
print("Data loaded")

console.print_summary(db)
