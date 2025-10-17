import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import assets.tarkov_api as api
import numpy as np
import pprint

# Initialize app
app = dash.Dash(__name__)
server = app.server  # If you want to deploy later

# Layout
app.layout = html.Div([
    html.Div(
        [
            html.Img(src="https://www.escapefromtarkov.com/build-eft-site/_nuxt/logo.WO0wViWU.webp", className="title", id="title"),
            html.Div([html.Button("Submit", id="btn")]),
            html.H2("Randomize Map"),
            dcc.Dropdown(
                id='map-dropdown',
                options=[
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'}
                ], value='no'
            ),
            html.Div(id="box-container", className="box-container")
        ], 
        className="pageLayout"
    )
])

@app.callback(
    Output("box-container", "children"),
    Input("btn", "n_clicks"),
    Input("map-dropdown", "value")
)
def update_boxes(n_clicks, map_choice):
    if not n_clicks:
        return [html.Div("", className="empty")]
    try:
        request = api.kit_generator()
        # print(request)
        cusomize_weapon = request[8]
        # print(f"cusomize_weapon: {cusomize_weapon}")
        new_request = request[:-1]
        # print('=---=')
        print(new_request)
        new_request_list = list(new_request)
        print(new_request_list)
        
        if map_choice == 'yes':
            maps = ['Customs', 'Woods', 'Shoreline', 'Interchange', 'Labs', 'Reserve', 'Lighthouse', 'Streets of Tarkov', "Factory", "The Labyrinth"] 
            selected_map = np.random.choice(maps)
            print(selected_map)
            map = ['Map', selected_map, f'/assets/images/{selected_map.lower()}_image.png']
            new_request_list.append(map)
            boxes = [
                html.Div(
                    [
                        html.Div(item[0], className="headers"),
                        html.Div(item[1], className="name"),
                        html.Div([html.Img(src=item[2], className="img")], className="divImg"),
                    ],
                    className="box",
                )
                for item in new_request_list
            ]

            data = html.Div(
                [
                    html.Div(boxes, className="my-div-style"),
                    html.Div([html.Div("Customized Weapon: " + cusomize_weapon, className="name")]),
                ]
            )

            return data

        else:
            boxes = [
                html.Div(
                    [
                        html.Div(item[0], className="headers"),
                        html.Div(item[1], className="name"),
                        html.Div([html.Img(src=item[2], className="img")], className="divImg"),
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
        print(e)
        return [html.Div(f"Error: {e}", className="box") for _ in range(10)]

if __name__ == "__main__":
    app.run(debug=True)