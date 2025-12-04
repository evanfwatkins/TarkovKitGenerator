import dash
from dash import html, dcc, Input, Output, register_page

register_page(__name__, path="/", className="homescreen")

layout = html.Div(
    [
        html.Div(className="upcoming-features",
            children=[
                html.Div(
                    [
                        html.H3("Known Bugs", className="features-title"),
                        dcc.Link("GitHub Repo", href="https://github.com/evanfwatkins/TarkovKitGenerator", className="github-link"),
                    ], className="features-title"
                ),
                html.Ul(
                    className="features-list",
                    children=[
                        html.Li("Helmets, masks, and headsets conflict. Decide what gear to wear - Work in progress"),
                        html.Li("Armor and armored vests may conflict. Decide what armor to wear - Work in progress"),
                        html.Li("Gun customizations don't work one bit")
                    ],
                ),
            ],
        ),
        html.Div(className="upcoming-features",
            children=[
                html.H3("Upcoming Changes (Updated: 12/03)", className="features-title"),
                html.Ul(
                    className="features-list",
                    children=[
                        html.Li("Hideout functionality"),
                        html.Ul(
                            className="sub-features-list",
                            children=[
                                html.Li("Fix station upgrade/craft display"),
                                html.Li("Fix station selection style"),
                                html.Li("Optimize station upgrade/craft response time"),
                            ]
                        ),
                        html.Li("Seamless gear combinations"),
                        html.Li("Optimized kit generator response time"),
                        html.Li("Weapon attachment randomizer"),
                        html.Li("Fill the page with adds and viruses"),
                        html.Li("Add required annaul subscription for p2w features"),
                    ]
                ),
            ],
        ),
    ], className="header", id="header"
)