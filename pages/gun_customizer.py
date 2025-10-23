import dash
from dash import html, dcc, callback, Input, Output, register_page
from urllib.parse import parse_qs
from dash import html, dcc, Input, Output, register_page
import random
from pages import tarkov_api as api  # import your logic
from dash import html, dcc, Input, Output, register_page, callback_context
from dash import ctx
from dash import page_registry, page_container

register_page(__name__, path="/gun_customizer", )

layout = html.Div(
    [
        dcc.Location(id="location", refresh=False),   # <-- gives us .pathname and .search
        html.H3("Gun Customizer"),
        html.Div(id="gun-name-display"),
        # ... other page content ...
    ]
)

@dash.callback(
    Output("gun-name-display", "children"),
    Input("location", "search"),
)

def show_gun_from_query(search: str):
    # search is like "?gun=Kalashnikov%20AKS-74%20...". Could be None or ""
    if not search:
        return "No gun parameter provided."
    attatchment_query = """query MyQuery {items(categoryNames: [WeaponMod]) {name image512pxLink types category {normalizedName}}}"""
    qs = search.lstrip("?")  # remove leading '?'
    params = parse_qs(qs)    # returns dict of lists, values are already URL-decoded
    
    params_list = list(params.items())
    result = [vals[0] for (_, vals) in params_list]

    gun_name = result[0]
    gun_image = result[1]

    print(gun_name)
    print(gun_image)

    # print(f"Parsed query params: {params}")
    gun = params.get("gun", [""])[0]  # get first value or empty string
    if not gun:
        return "gun param present but empty."
    return f"Selected gun: {gun}"