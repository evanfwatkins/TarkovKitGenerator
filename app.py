import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import html
import tarkov_api as api

# Initialize app
app = dash.Dash(__name__)
server = app.server  # If you want to deploy later

# Layout
app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Tarkov Loadout Generator", className="title", id="title"),
                html.Div([html.Button("Submit", id="submit-btn")], className="input-row"),
                html.Div(id="box-container", className="box-container") 
            ], className="my-div-style"
        )
    ]
)


@app.callback(
    Output("box-container", "children"),
    Input("submit-btn", "n_clicks"),
)
def update_boxes(n_clicks):
    if not n_clicks:
        return [html.Div("", className="box")]

    try:
        request = api.kit_generator()
        data = [
            html.Div([
                html.P(item[0],className="name"), 
                html.Img(src=item[1], style={'ali':'50px', 'margin-left':'10px'})  # Item icon
            ], className="box") 
            for item in request 
        ]
        return data
    
    except Exception as e:
        return [html.Div(f"Error: {e}", className="box") for _ in range(10)]


if __name__ == "__main__":
    app.run(debug=True)
