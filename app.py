import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import requests
import tarkov_api as api

# Initialize app
app = dash.Dash(__name__)
server = app.server  # If you want to deploy later

# Layout
app.layout = html.Div([
    html.H1("Tarkov Loadout Generator", className="title", id="title"),
    
    html.Div([
        dcc.Input(id="api-input", type="text", placeholder="Enter query..."),
        html.Button("Submit", id="submit-btn"),
    ], className="input-row"),
    
    html.Div(id="box-container", className="box-container")
])



# Callback to fetch API and populate boxes
@app.callback(
    Output("box-container", "children"),
    Input("submit-btn", "n_clicks"),
    State("api-input", "value")
)
def update_boxes(n_clicks, query):
    if not n_clicks or not query:
        return [html.Div("Waiting...", className="box") for _ in range(10)]

    try:
        request = new_query(result)
        print(request)
        
        # Mock data for demo
        data = [f"Item {i+1} for {request}" for i in range(10)]
        
        # Fill 10 boxes with API response (truncate or pad)
        return [html.Div(data[i], className="box") for i in range(10)]
    
    except Exception as e:
        return [html.Div(f"Error: {e}", className="box") for _ in range(10)]


if __name__ == "__main__":
    app.run(debug=True)
