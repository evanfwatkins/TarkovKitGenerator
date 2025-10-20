import dash
from dash import html, dcc, Input, Output, register_page
import random
from pages import tarkov_api as api  # import your logic

register_page(__name__, path="/kit")

layout = html.Div([
    html.Div(
        [
            html.H2("Kit Generator"),
            html.Button("Submit", id="btn"),
            html.H2("Randomize Map"),
            dcc.Dropdown(
                id='map-dropdown',
                options=[
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'}
                ],
                value='no'
            ),
            html.Div(id="box-container", className="box-container")
        ],
        className="pageLayout"
    )
])

@dash.callback(
    Output("box-container", "children"),
    Input("btn", "n_clicks"),
    Input("map-dropdown", "value")
)
def update_boxes(n_clicks, map_choice):
    if not n_clicks:
        return [html.Div("", className="empty")]

    try:
        request = api.kit_generator()
        customized_weapon = request[8]
        new_request = request[:-1]
        new_request_list = list(new_request)

        # If map randomization is selected
        if map_choice == 'yes':
            maps = ['Customs', 'Woods', 'Shoreline', 'Interchange', 'Labs',
                    'Reserve', 'Lighthouse', 'Streets', 'Factory', 'Labrynth', 'Ground_Zero']
            selected_map = random.choice(maps)
            map_item = ['Map', selected_map, f'/assets/images/{selected_map.lower()}_image.png']
            new_request_list.append(map_item)

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

        data = html.Div([
            html.Div(boxes, className="my-div-style"),
            html.Div([html.Div("Customized Weapon: " + customized_weapon, className="name")])
        ])

        return data

    except Exception as e:
        print(e)
        return [html.Div(f"Error: {e}", className="box") for _ in range(10)]
