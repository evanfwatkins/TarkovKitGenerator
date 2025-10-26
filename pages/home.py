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
                        html.Li("Armor and armored vests conflict. Decide what gear to wear - Work in progress"),
                        html.Li("Gun customizations don't work one bit")
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
                                html.Li("Simple Yes/No for suppressor, foregrip, optic, flashlight"),
                                html.Li("Randomized (compatible) attatchments straight from the kit gerenator screen"),
                                html.Li(f"Select a gun to customize from the Gun Customizer page"),
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