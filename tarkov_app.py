from dash import Dash, html, dcc, page_container

from data_loader import load_all_data

# Instantiate Dash before any register_page() calls
app = Dash(__name__, use_pages=True)
server = app.server  # (optional, for deployment)


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
                dcc.Link("Kit DEV Testing", href="/kitV2", className="nav-link"),
                dcc.Link("Hideout", href="/hideout", className="nav-link")
            ],
        ),
    ],
)

loaded = load_all_data()
if not loaded:
    print("Warning: initial Tarkov data load failed. App will continue with empty cache.")


# Main app layout
app.layout = html.Div(
    [
        navbar,
        html.Div(page_container, className="page-content"),  # Active page content
    ],
    className="main-layout",
)

if __name__ == "__main__":
    app.run(debug=True)