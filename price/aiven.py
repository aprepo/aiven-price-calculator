import secrets
import json
import requests
import errors


def dump_settings():
    print(f"API TOKEN: {secrets.API_TOKEN[:4]}***")


def _get_headers():
    return {
        'content-type': "application/json",
        'authorization': f"aivenv1 {secrets.API_TOKEN}"
    }


def _get(url):
    response = requests.get(url, headers=_get_headers())
    if not response:
        raise Exception(f"ERROR: {response.status_code} : {response.content}")
    return response


def get_billing_groups(db):
    response = _get("https://api.aiven.io/v1/billing-group")
    data = response.json()
    for group in data['billing_groups']:
        db.insert_billing_group(
            id=group['billing_group_id'],
            name=group['billing_group_name'],
            account_id=group['account_id'],
            account_name=group['account_name'],
            currency=group['billing_currency'],
            payment_method=group['payment_method'],
            estimated_balance_usd=group['estimated_balance_usd'],
            estimated_balance_local=group['estimated_balance_local']
        )


def get_projects(db):
    response = _get("https://api.aiven.io/v1/project").json()
    for project in response['projects']:
        db.insert_project(
            project_name=project['project_name']
        )


def get_prices(db, project):
    response = _get(f"https://api.aiven.io/v1/project/{project}/service_types")
    data = response.json()
    for service_type in data["service_types"]:
        for plan in data["service_types"][service_type]['service_plans']:
            for region in plan['regions']:
                #print(f"PLAN: {plan['service_type']} : {plan['service_plan']} : {plan['regions'][region]['price_usd']} usd per hour")
                db.insert_plan(
                    project_name=project,
                    service_type=plan['service_type'],
                    plan=plan['service_plan'],
                    region=region,
                    price=plan['regions'][region]['price_usd']
                )
    #print(json.dumps(response.json(), indent=4))


def get_services(db, project):
    response = _get(f"https://api.aiven.io/v1/project/{project}/service")
    data = response.json()
    for service in data['services']:
        try:
            price = db.get_price_for_service(
                project_name=project,
                service_type=service['service_type'],
                plan=service['plan'],
                region=service['cloud_name']
            )
        except errors.NoPriceForPlanError as e:
            print(f"WARNING: No price found for {project}: "
                  f"{service['service_type']} {service['service_name']} {service['plan']} {service['cloud_name']}"
                  f", using zero price.")
            price = 0

        print(f"Service: {service['service_type']} : {service['service_name']} : {service['plan']} : {service['cloud_name']} : {price}")
        db.insert_service(
            project_name=project,
            service_name=service['service_name'],
            service_type=service['service_type'],
            plan=service['plan'],
            cloud=service['cloud_name'],
            price=price
        )


def get_invoices(db, project):
    response = _get(f"https://api.aiven.io/v1/project/{project}/invoice")
    data = response.json()
    for invoice in data['invoices']:
        print(f"INVOICE: {invoice['invoice_number']}: {invoice['period_begin']}-{invoice['period_end']} " 
              f"{invoice['total_inc_vat']} {invoice['currency']}")
        #print(json.dumps(invoice, indent=4))
        db.insert_invoice(
            billing_group=invoice['billing_group_name'],
            project_id=project,
            invoice_id=invoice['invoice_number'],
            period_start=invoice['period_begin'],
            period_end=invoice['period_end'],
            state=invoice['state'],
            total_inc_vat=invoice['total_inc_vat'],
            total_vat_zero=invoice['total_vat_zero'],
            currency=invoice['currency']
        )


def get_invoice_line_items(db, billing_group_id, project, invoice_id):
    db.insert_line_item(
        billing_group_id,
        invoice_id,
        project=project,
        service_name="",
        service_type="",
        plan="",
        cloud="",
        description="",
        total_usd="",
        total_local="",
        currency="",
        period_start="",
        period_end=""
    )