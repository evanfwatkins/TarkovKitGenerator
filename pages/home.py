import dash
from dash import html, dcc, Input, Output, register_page

register_page(__name__, path="/", className="homescreen")

layout = html.Div(
    [
        html.Div(className="upcoming-features",
            children=[
                html.H3("Known Bugs", className="features-title"),
                html.Ul(
                    className="features-list",
                    children=[
                        html.Li("Helmets, masks, and headsets may block eachother. Decide what gear to wear - Work in progress"),
                        html.Li("Armor and armored vests get returned. Decide what gear to wear - Work in progress"),
                        html.Li("Gun customizations are non-functional - Work in progress")
                    ],
                ),
            ],
        ),
        html.Div(className="upcoming-features",
            children=[
                html.H3("Upcoming Changes (Updated: 10/26)", className="features-title"),
                html.Ul(
                    className="features-list",
                    children=[
                        html.Li("Weapon attachment randomizer"),
                        html.Ul(
                            className="sub-features-list",
                            children=[
                                html.Li("Customize straight from the kit gerenator screen"),
                                html.Li("Pick a gun to customize from the gun customizer page"),
                            ]
                        ),
                        html.Li("Optimize kit generator response time"),
                        html.Li("Fill the page with adds and viruses"),
                        html.Li("Add required annaul subscription")
                    ]
                ),
            ],
        ),
    ], className="header", id="header"
)