def print_summary(db):
    print(f"-------------------------------------------------------")
    print(f"Projects........: {db.get_project_count()}")
    print(f"Services........: {db.get_service_count()}")
    print(f"Plans...........: {db.get_plan_count()}")
    print(f"Billing groups..: {db.get_billing_groups_count()}")
    print(f"Invoices........: {db.get_invoice_count()}")
    print(f"Invoice lines...: {db.get_line_items_count()}")
    print(f"-------------------------------------------------------")
    print(f"Total spend: ")
    for (project, hourly, monthly) in db.get_total_spend():
        print(f"{project} : {hourly:.2f} per hour : {monthly:.2f} per month")
