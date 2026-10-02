from dash import Dash, html, dcc, page_container


# Instantiate Dash before any register_page() calls
app = Dash(__name__, use_pages=True)
server = app.server  # (optional, for deployment)


from data_loader import preload_kit_data

preload_kit_data()

# Shared navbar (persistent on all pages)
navbar = html.Div(
    className="navbar",
    children=[
        html.Img(
            src="https://www.escapefromtarkov.com/build-eft-site/_nuxt/logo.WO0wViWU.webp",
            className="title-logo",
            id="title-logo",
        ),
        html.Div(
            className="nav-links",
            children=[
                dcc.Link("Home", href="/", className="nav-link"),
                dcc.Link("Kit Generator", href="/kit", className="nav-link"),
                html.Span("Hideout (Unavailable)", className="nav-link nav-link-disabled")
            ],
        ),
    ],
)

# Main app layout
app.layout = html.Div(
    [
        navbar,
        html.Div(page_container, className="page-content"),  # Active page content
    ],
    className="main-layout",
)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)