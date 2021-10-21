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


def get_projects(db):
    response = _get("https://api.aiven.io/v1/project").json()
    for project in response['projects']:
        #print(json.dumps(project, indent=4))
        #print(f"Project: {project['project_name']}")
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
