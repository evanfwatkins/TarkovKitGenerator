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
                            "Water Collector",
                            "Heating",
                            "Intelligence Center",
                            "Medstation",
                            "Lavatory",
                            "Nutrition Unit",
                            "Security",
                            "Rest Space",
                            "Shooting Range",
                            "Bitcoin Farm",
                            "Vents"
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
            html.Button("Reset", className="reset", id="clear")
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
    Input("clear", "n_clicks")
)

# Define the utility function for the Tarkov-themed info block
def tarkov_info_tip(tip_text, class_name="tarkov-info-tip"):
    """Creates a Tarkov-themed text block for tips or info."""
    return html.Div(
        tip_text,
        className=class_name
    )

def render_hideout(station, mode, n_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return html.Div("", className="empty") 
        
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'clear' and n_clicks:
        return html.Div("", className="empty")
    cards = []

    # 🔧 UPGRADE VIEW
    if mode == "UPGRADES" or mode == "upgrade":
        return render_upgrades(station)
    
    # 🧪 CRAFT VIEW
    else:
        return render_crafts(station)

    
def render_upgrades(station):
    query = """query MyQuery {hideoutStations(gameMode: pve) {name levels {itemRequirements {item {name inspectImageLink} count}}}}"""
    upgrades = api.get_hideout_upgrades(query,station)

    if not upgrades:
        return html.Div("", className="empty")

    cards = []

    for lvl in upgrades:
        upgrade_items = [
            html.Div(
                [
                    # Index 2 of the TUPLE is the Image URL
                    html.Div(
                        # Index 0 is the Name, Index 1 is the Count
                        f"{item[0]} x{item[1]}", 
                        className="name_and_count"
                    ),
                    html.Img(src=item[2], className="img")
                ],
                className="upgrade-item"
            )
            # Loop over the list of tuples
            for item in lvl['requirements'] 
        ]      

        cards.append(
            html.Div(
                [
                    html.Div(f"Level {lvl['level']}", className="headers"),
                    html.Div(upgrade_items, className="upgrade-card")
                ],
                className="upgrade-card"
            )
        )

    return cards

def render_crafts(station):
    query = """query MyQuery {hideoutStations(gameMode: pve) {name crafts {duration requiredItems {item {name inspectImageLink} count} level rewardItems {item {name inspectImageLink}}} imageLink}}"""
    crafts = api.get_hideout_crafts(query,station)

    if not crafts:
        return html.Div("Select a hideout station", className="empty-crafts")

    note = tarkov_info_tip("HINT: Use Ctrl + F to quickly search for an item", class_name="tarkov-info-tip craft-note")

    cards = []
    for craft in crafts:
        cards.append(
            html.Div(
                [
                    html.Div(
                        f"{station} Level {craft['level']} • {craft['duration']//3600}H",
                        className="craft-headers",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Img(src=img, className="item-img"),
                                            html.Div(name, f' x{count}'),
                                        ],
                                        className="item-box",
                                    )
                                    for name, count, img in craft["requirements"]
                                ],
                                className="item-grid",
                            ),

                            html.Div("→", className="craft-arrow"),

                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Img(src=img, className="item-img"),
                                            html.Div(name, f"x{count}"),
                                        ],
                                        className="item-box",
                                    )
                                    for name, count, img in craft["outputs"]
                                ],
                                className="item-grid",
                            ),
                        ],
                        className="craft-row",
                    ),
                ],
                className="craft-card",  # ✅ different class
            )
        )

    return [note] + cards