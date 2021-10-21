import aiven
import cachedb

print("Initiating cache...")
db = cachedb.init()

aiven.dump_settings()

print("Loading data...")
aiven.get_projects(db)
aiven.get_prices("dev-sandbox", db)
print("Data loaded")

print(f"Projects: {db.get_project_count()}")
print(f"Plans:    {db.get_plan_count()}")
