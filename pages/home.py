import dash
from dash import html, dcc, Input, Output, register_page

register_page(__name__, path="/", className="homescreen")

layout = html.Div(
    [
        html.Div(className="upcoming-features",
            children=[
                html.H3("Patch notes  (updated: 12/13)", className="features-title"),
                html.H5("version 1.0.12", className="version-title"),

                html.Ul(
                    className="features-list",
                    children=[
                        html.Li("Refactor code base to preload data and improve response times"),
                        html.Li("Refined helmet/headset/mask & vest/armor logic to reduce conflicting gear combinations"),
                    ]
                ),
                html.Div(
                    [
                        html.H3("Upcoming Changes", className="features-title"),
                        html.Ul(
                            className="features-list",
                            children=[
                                html.Li("Improve weapon attachment selection"),
                                html.Li("Continue imrpovements to gear combinations"),
                            ]
                        ),
                    ]
                )
            ],
        ),
    ], className="header", id="header"
)