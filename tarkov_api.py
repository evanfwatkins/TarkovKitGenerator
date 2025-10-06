import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import requests
import tarkov_api as api

def kit_generator():
    headers = {"Content-Type": "application/json"}
    all_items_query = """query MyQuery { itemCategories {name}}"""

    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': all_items_query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

result = run_query()
print(result)