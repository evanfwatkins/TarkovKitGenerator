import dash
from dash import html, dcc, Input, Output, register_page

register_page(__name__, path="/", className="homescreen")

layout = html.Div(
    [
        html.Div(className="upcoming-features",
            children=[
                html.Div(
                    [
                        html.H3("Known Bugs (Updated: 12/10)", className="features-title"),
                        dcc.Link("GitHub Repo", href="https://github.com/evanfwatkins/TarkovKitGenerator", className="github-link"),
                    ], className="features-title"
                ),
                html.Ul(
                    className="features-list",
                    children=[
                        html.Li("Helmets, masks, and headsets can’t always be worn together. Choose which combination you want to use. (Work in progress)"),
                        html.Li("Some armor pieces and armored vests may not be compatible. Choose the armor setup you prefer. (Work in progress)"),
                        html.Li("Kit generator and Hideout crafts response times may be slow. Refresh and retry (Work in progress)")
                    ],
                ),
            ],
        ),
        html.Div(className="upcoming-features",
            children=[
                html.H3("Upcoming Changes", className="features-title"),
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