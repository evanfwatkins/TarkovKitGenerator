import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import assets.tarkov_api as api

# Initialize app
app = dash.Dash(__name__)
server = app.server  # If you want to deploy later

# Layout
app.layout = html.Div([
    html.Div(
        [
            html.Img(src="https://www.escapefromtarkov.com/build-eft-site/_nuxt/logo.WO0wViWU.webp", className="title", id="title"),
            html.Div([html.Button("Submit", id="btn")]),
            html.Div(id="box-container", className="box-container") 
        ], 
        className="pageLayout"
    )
])

@app.callback(
    Output("box-container", "children"),
    Input("btn", "n_clicks"),
)
def update_boxes(n_clicks):
    if not n_clicks:
        return [html.Div("", className="empty")]
    try:
        request = api.kit_generator()
        cusomize_weapon = request[7]
        new_request = request[:-1]
        print(new_request)
        boxes = [
            html.Div(
                [
                    html.Div(item[0], className="headers"),
                    html.Div(item[2], className="name"),
                    html.Div([html.Img(src=item[3], className="img")], className="divImg"),
                ],
                className="box",
            )
            for item in new_request
        ]

        data = html.Div(
            [
                html.Div(boxes, className="my-div-style"),
                html.Div([html.Div("Customized Weapon: " + cusomize_weapon, className="name")]),
            ]
        )

        return data
    
    except Exception as e:
        return [html.Div(f"Error: {e}", className="box") for _ in range(10)]

if __name__ == "__main__":
    app.run(debug=True)