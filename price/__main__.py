import aiven
import cachedb

print("Initiating cache...")
db = cachedb.init()

aiven.dump_settings()

print("Loading data...")
aiven.get_projects(db)
for (project, ) in db.get_projects():
    print(f"Project : {project}...")
    aiven.get_prices(db=db, project=project)
    aiven.get_services(db=db, project=project)
    aiven.get_invoices(db=db, project=project)
print("Data loaded")

print(f"-------------------------------------------------------")
print(f"Projects: {db.get_project_count()}")
print(f"Services: {db.get_service_count()}")
print(f"Plans:    {db.get_plan_count()}")
print(f"Invoices: {db.get_invoice_count()}")
print(f"-------------------------------------------------------")
print(f"Total spend: ")
for (project, hourly, monthly) in db.get_total_spend():
    print(f"{project} : {hourly:.2f} per hour : {monthly:.2f} per month")
