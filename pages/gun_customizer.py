from dash import html, dcc, Input, Output, register_page, callback_context
from dash import ctx
from dash import page_registry, page_container

import dash

register_page(__name__, path="/gun_customizer")

layout = html.Div([
    html.H2("Gun Customizer"),
    html.Div(id="gun-name-container")
])

@dash.callback(
    Output("gun-name-container", "children"),
    Input("url", "search")  # dcc.Location component must exist in main layout
)
def display_gun_name(search):
    if search:
        from urllib.parse import parse_qs
        params = parse_qs(search.lstrip("?"))
        print(f"params: {params}")
        gun = params.get("gun", ["Unknown"])[0]
        return f"Selected Gun: {gun}"
    return "No gun selected yet."