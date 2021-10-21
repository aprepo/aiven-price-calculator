import secrets

import requests
import json


def dump_settings():
    print(f"API TOKEN: ***{secrets.API_TOKEN[:4]}")


def _get_headers():
    return {
        'content-type': "application/json",
        'authorization': f"aivenv1 {secrets.API_TOKEN}"
    }


def get_projects(db):
    response = requests.get("https://api.aiven.io/v1/project", headers=_get_headers())
    #print(json.dumps(response.json(), indent=4))


def get_prices(project, db):
    response = requests.get(f"https://api.aiven.io/v1/project/{project}/service_types", headers=_get_headers())
    data = response.json()
    for service_type in data["service_types"]:
        for plan in data["service_types"][service_type]['service_plans']:
            for region in plan['regions']:
                print(f"PLAN: {plan['service_type']} : {plan['service_plan']} : {plan['regions'][region]['price_usd']} usd per hour")
                db.insert_plan(
                    service_type=plan['service_type'],
                    plan=plan['service_plan'],
                    region=region,
                    price=plan['regions'][region]['price_usd']
                )
    #print(json.dumps(response.json(), indent=4))

