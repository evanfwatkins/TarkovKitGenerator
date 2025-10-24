import dash
from dash import html, dcc, Input, Output, register_page

# Initialize Dash app with multipage support
# app = dash.Dash(__name__, use_pages=True)
app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

server = app.server  # For deployment

register_page(__name__, path="/", className="homescreen")

app.layout = html.Div(
    [
    html.Img(
        src="https://www.escapefromtarkov.com/build-eft-site/_nuxt/logo.WO0wViWU.webp",
        className="title", id="title"
    ),
    html.Div(
        [
            html.Div(
                [
                    html.A("Tarkov Kit Generator", href="/kit", className="nav-link")
                ],
                className="nav-links"
            )
        ],
        className="navbar"
    )

    ,dash.page_container
    ], className="header", id="header"
)

if __name__ == "__main__":
    app.run(debug=True)
