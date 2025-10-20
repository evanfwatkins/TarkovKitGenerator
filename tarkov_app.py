import dash
from dash import html, dcc

# Initialize Dash app with multipage support
# app = dash.Dash(__name__, use_pages=True)
app = dash.Dash(__name__, use_pages=True)

server = app.server  # For deployment

app.layout = html.Div([
    html.Img(
        src="https://www.escapefromtarkov.com/build-eft-site/_nuxt/logo.WO0wViWU.webp",
        className="title", id="title"
    ),
    html.H1("Escape From Tarkov Tools", className="title", style={"textAlign": "center"}),

    # Simple navigation bar
    html.Div([
        dcc.Link("Kit Generator", href="/kit"),
        html.Span(" | "),
        dcc.Link("Stats", href="/stats")
    ], style={"textAlign": "center", "marginBottom": "20px"}),

    # This dynamically displays whichever page is active
    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=True)
