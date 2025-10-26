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
    # Output("gun-container", "children"),
    Input("btn", "n_clicks"),
    Input("map-dropdown", "value")
)
def update_boxes(n_clicks, map_choice):
    if not n_clicks:
        return [html.Div("", className="empty")]

    try:
        request = api.kit_generator()\
        # comment me back in!!!!!!!!!!!!!!
        # customized_weapon = request[8]
        customized_weapon = "Yes"
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

        # Conditional Customized Weapon display

        if customized_weapon == "Yes":
            gun_name = new_request_list[7][1]
            gun_image = new_request_list[7][2]
            # Example additional boxes for attachments, mods, etc.
            attatchment_randomizer = api.weapon_customizer(gun_name)

            
            # print(attatchments)
            weapon_div = html.Div(
                [
                    # html.Div("Customized Weapon", className="headers"),
                    # html.Div([html.Div(gun_name, className="name"),
                    # html.Img(src=gun_image, className="img")], className="divImg"),
                    # for i in response
                    html.Div(
                        [
                            html.Div("Muzzle", className="headers"),
                            html.Div("Name", className="name"),
                            html.Div("img", className="img"),
                        ], className="box"
                    ),
                    html.Div(
                        [
                            html.Div("Grip", className="headers"),
                            html.Div("Name", className="name"),
                            html.Div("img", className="img"),
                        ],
                        className="box"
                    ),
                    html.Div(
                        [
                            html.Div("Optic", className="headers"),
                            html.Div("Name", className="name"),
                            html.Div("img", className="img"),

                        ],
                        className="box"
                    ),
                    html.Div(
                        [
                            html.Div("Stock", className="headers"),
                            html.Div("Name", className="name"),
                            html.Div("img", className="img"),

                        ],
                        className="box"
                    ),
                    html.Div(
                        [
                            html.Div("Magazine", className="headers"),
                            html.Div("Name", className="name"),
                            html.Div("img", className="img"),

                        ],
                        className="box"
                    ),
                    html.Div(
                        [
                            html.Div("Flashlight/Lazer", className="headers"),
                            html.Div("Name", className="name"),
                            html.Div("img", className="img"),

                        ],
                        className="box"
                    ),
                ],
                className="gun-boxes"
            )
                
        else: 
            weapon_div = html.Div(
                html.Span(f"Customized Weapon: {customized_weapon}", className="name"),
                style={"textAlign": "center", "marginTop": "10px"}
            )
            # gun_name = new_request_list[7][1]
            # # print(gun_name)
            # weapon_div = html.Div(
            #     [
            #         html.Span("Customized Weapon: Yes", className="name"),
            #         html.Span(" | "),
            #         dcc.Link(
            #             "Gun Customizer",
            #             href=f"/gun_customizer?gun={gun_name}",
            #             className="gun_cust-link"
            #         )
            #     ],
            #     style={"textAlign": "center", "marginTop": "10px"}
            # )

        data = html.Div([
            html.Div(boxes, className="my-div-style"),
            weapon_div
        ])

        return data

    except Exception as e:
        print(e)
        return [html.Div(f"Error: {e}", className="box") for _ in range(10)]