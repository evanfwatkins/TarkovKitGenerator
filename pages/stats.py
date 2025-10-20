from dash import html, register_page

register_page(__name__, path="/stats", name="Stats")

layout = html.Div([
    html.H2("Stats Page"),
    html.P("This is your second page — you can add graphs, summaries, or history here."),
    html.A("Back to Kit Generator", href="/")
])