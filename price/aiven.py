import secrets
import json
import requests


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
        print(json.dumps(project, indent=4))
        print(f"Project: {project['project_name']}")
        db.insert_project(
            project_name=project['project_name']
        )


def get_prices(project, db):
    response = _get(f"https://api.aiven.io/v1/project/{project}/service_types")
    data = response.json()
    for service_type in data["service_types"]:
        for plan in data["service_types"][service_type]['service_plans']:
            for region in plan['regions']:
                #print(f"PLAN: {plan['service_type']} : {plan['service_plan']} : {plan['regions'][region]['price_usd']} usd per hour")
                db.insert_plan(
                    service_type=plan['service_type'],
                    plan=plan['service_plan'],
                    region=region,
                    price=plan['regions'][region]['price_usd']
                )
    #print(json.dumps(response.json(), indent=4))

