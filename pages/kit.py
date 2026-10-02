import dash
import json
from dash import html, dcc, Input, Output, register_page
import random
from pages import tarkov_api as api  # import your logic

register_page(__name__, path="/kit", name="Tarkov Kit Generator")


layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(id='map-dropdown',
                            options=[
                                {'label': 'Random Map: Yes', 'value': 'yes'},
                                {'label': 'Random Map: No', 'value': 'no'}
                        ],value='no'),
                    ], className="map-dropdown-div"
                ),
                html.Button("Generate Kit", id="btn"),
                html.Div(id="box-container", className="box-container"),
                html.Div(id="gun-container", className="gun-container"),
                html.Details(
                    [
                        html.Summary("Generated kit JSON"),
                        html.Button(
                            "Clear",
                            id="clear-kit-json",
                            className="terminal-clear-button",
                            n_clicks=0,
                        ),
                        html.Pre(
                            "Generate a kit to inspect its final item data.",
                            id="kit-json-output",
                        ),
                    ],
                    className="debug-terminal",
                ),

            ],
        className="pageLayout"
    )
])

@dash.callback(
    Output("box-container", "children"),
    Output("gun-container", "children"),
    Output("kit-json-output", "children"),
    Input("btn", "n_clicks"),
    Input("map-dropdown", "value"),
    Input("clear-kit-json", "n_clicks"),
)
def update_boxes(n_clicks, map_choice, clear_clicks=0):
    if dash.ctx.triggered_id == "clear-kit-json":
        return dash.no_update, dash.no_update, ""

    if not n_clicks:
        return [html.Div("", className="empty")], [], "Generate a kit to inspect its final item data."

    items, customized_weapon = api.kit_generator()
    if map_choice == "yes":
        maps = [
            "Customs", "Woods", "Shoreline", "Interchange", "Labs",
            "Reserve", "Lighthouse", "Streets", "Factory", "Labrynth", "Ground_Zero",
        ]
        selected_map = random.choice(maps)
        items.append(
            {
                "slot": "Map",
                "name": selected_map,
                "image": f"/assets/images/{selected_map.lower()}_image.png",
                "types": ["map"],
                "blocksHeadphones": False,
            }
        )

    boxes = [
        html.Div(
            [
                html.Div(item["slot"], className="headers"),
                html.Div(item["name"], className="name"),
                html.Div(
                    [html.Img(src=item["image"], className="img kit-item-image")],
                    className="divImg",
                ),
            ],
            className="box",
        )
        for item in items
    ]

    if customized_weapon == "Yes":
        attachments = api.weapon_customizer(items[7]["name"])
        weapon_div = [
            html.Div(
                [
                    html.Div(attachment[0], className="headers"),
                    html.Div(attachment[1], className="name"),
                ],
                className="gun-box",
            )
            for attachment in attachments
        ]
    else:
        weapon_div = html.Div(
            [html.Span("Customized Weapon: No", className="name")]
        )

    return boxes, weapon_div, json.dumps(items, indent=2)