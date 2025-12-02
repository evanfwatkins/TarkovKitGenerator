import dash
from dash import html, dcc, Input, Output, register_page
from pages import tarkov_api as api

register_page(__name__, path="/hideout", name="Hideout")

layout = html.Div(
    [
        html.Div(
            [
                dcc.Dropdown(
                    id="station-dropdown",
                    placeholder="Select Station",
                    options=[
                        {"label": s, "value": s}
                        for s in [
                            "Workbench",
                            "Intelligence Center",
                            "Medstation",
                            "Lavatory",
                            "Nutrition Unit",
                            "Security",
                            "Rest Space",
                            "Shooting Range",
                        ]
                    ],
                ),

                dcc.RadioItems(
                    id="hideout-mode",
                    options=[
                        {"label": "Upgrades", "value": "upgrade"},
                        {"label": "Crafts", "value": "craft"},
                    ],
                    value="upgrade",
                    inline=True,
                    className="hideout-mode",
                ),
            ],
            className="hideout-controls",
        ),

        html.Div(id="hideout-container", className="hideout-container"),
    ],
    className="pageLayout",
)

@dash.callback(
    Output("hideout-container", "children"),
    Input("station-dropdown", "value"),
    Input("hideout-mode", "value"),
)
def render_hideout(station, mode):
    if not station:
        return html.Div("", className="empty")

    cards = []

    # 🔧 UPGRADE VIEW
    if mode == "upgrade":
        all_stations_upgrades_query = """query MyQuery {hideoutStations(gameMode: pve) {name levels {itemRequirements {item {name inspectImageLink} count}}}}"""
        upgrades = api.get_hideout_upgrades(all_stations_upgrades_query, station)

        for lvl in upgrades:
            req_boxes = [
                html.Div(
                    [
                        html.Img(src=req[2], className="img"),
                        html.Div(req[0], className="name"),
                        html.Div(f"x{req[1]}", className="count"),
                    ],
                    className="item-box",
                )
                for req in lvl["requirements"]
            ]

            cards.append(
                html.Div(
                    [
                        html.Div(f"Level {lvl['level']}", className="headers"),
                        html.Div(req_boxes, className="item-grid"),
                    ],
                    className="hideout-card",
                )
            )

    # 🧪 CRAFT VIEW
    else:
        crafts = api.get_hideout_crafts(station)

        for craft in crafts:
            req_boxes = [
                html.Div(
                    [
                        html.Img(src=r[2], className="img"),
                        html.Div(r[0], className="name"),
                        html.Div(f"x{r[1]}", className="count"),
                    ],
                    className="item-box",
                )
                for r in craft["requirements"]
            ]

            cards.append(
                html.Div(
                    [
                        html.Div(craft["name"], className="headers"),
                        html.Div(req_boxes, className="item-grid"),
                        html.Div(
                            [
                                html.Span("Produces → "),
                                html.Img(src=craft["output"][1], className="img small"),
                                html.Span(craft["output"][0]),
                            ],
                            className="craft-output",
                        ),
                    ],
                    className="hideout-card",
                )
            )

    return cards
