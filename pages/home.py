import dash
from dash import html, dcc, Input, Output, register_page

register_page(__name__, path="/", className="homescreen")

layout = html.Div(
    [
        html.Img(
            src="https://www.escapefromtarkov.com/build-eft-site/_nuxt/logo.WO0wViWU.webp",
            className="title",
            id="title",
        ),
        html.Div(
            className="upcoming-features",
            children=[
                html.H3("Upcoming Changes", className="features-title"),
                html.Ul(
                    className="features-list",
                    children=[
                        html.Li("Weapon mod customization and attachment previews"),
                        html.Li("Dynamic armor durability and repair simulation"),
                        html.Li("Randomized PMC loadouts by faction or playstyle"),
                        html.Li("Integrated flea market price balance calculator"),
                        html.Li("Offline kit sharing and QR code export"),
                        html.Li("Favorite builds and quick re-roll options"),
                    ],
                ),
            ],
        ),
    ],
    className="header",
    id="header",
)