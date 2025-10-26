import dash
from dash import html, dcc, Input, Output, register_page
import random
from pages import tarkov_api as api  # import your logic

register_page(__name__, path="/kit", name="Tarkov Kit Generator")


layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(id='map-dropdown',
                            options=[
                                {'label': 'Randomize Map: Yes', 'value': 'yes'},
                                {'label': 'Randomize Map: No', 'value': 'no'}
                        ],value='no'),
                    ], className="map-dropdown-div"
                ),
                html.Button("Generate Kit", id="btn"),
                html.Div(id="box-container", className="box-container"),
                html.Div(id="gun-container", className="gun-container")

            ],
        className="pageLayout"
    )
])

@dash.callback(
    Output("box-container", "children"),
    Output("gun-container", "children"),
    Input("btn", "n_clicks"),
    Input("map-dropdown", "value")
)
def update_boxes(n_clicks, map_choice):
    if not n_clicks:
        return [html.Div("", className="empty")], []
    try:
        request = api.kit_generator()
        # comment me back in!!!!!!!!!!!!!!
        customized_weapon = request[8]
        # customized_weapon = "Yes"
        new_request = request[:-1]
        new_request_list = list(new_request)
        print(f"new_request_list: {new_request_list}")
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

        if customized_weapon == "Yes":
            gun_name = new_request_list[7][1]
            gun_image = new_request_list[7][2]
            attatchment_randomizer = api.weapon_customizer(gun_name)
            # print(f"attatchment_randomizer: {attatchment_randomizer}")
            new_attatchments_list = list(attatchment_randomizer)
            # print(f"new_attatchments_list: {new_attatchments_list}")
            # for item in attatchment_randomizer:
            #     print(f"item: {item}")
            #     print(f"item[0]: {item[0]}")
            #     print(f"item[1]: {item[1]}")
            weapon_div = [
                html.Div(
                    [
                        html.Div(a[0], className="headers"),
                        html.Div(a[1], className="name")
                    ],
                    className="gun-box",
                )
                for a in new_attatchments_list
            ]
            
        else: 
            # gun_name = new_request_list[7][1]
            weapon_div = html.Div(
                [
                    html.Span("Customized Weapon: No", className="name")
                ]
            )
            # return weapon_div
        
        return boxes, weapon_div

    except Exception as e:
        print(e)
        error_div = [html.Div(f"Error: {e}", className="box") for _ in range(10)]
        return error_div, []  # ← two outputs even on error