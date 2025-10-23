import dash
from dash import html, dcc, Input, Output, register_page
import random
from pages import tarkov_api as api  # import your logic

register_page(__name__, path="/kit")

layout = html.Div([
    html.Div(
        [
            html.H2("Randomize Map"),
            dcc.Dropdown(
                id='map-dropdown',
                options=[
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'}
                ],
                value='no'
            ),
            html.Button("Submit", id="btn"),
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

        # Conditional Customized Weapon display

        if customized_weapon == "Yes":
            gun_name = new_request_list[7][1]
            gun_image = new_request_list[7][2]
            # print(gun_name)
            weapon_div = html.Div(
                [
                    html.Span("Customized Weapon: Yes", className="name"),
                    html.Span(" | "),
                    dcc.Link(
                        "Gun Customizer",
                        href=f"/gun_customizer?gun={gun_name}&img={gun_image}",
                        className="gun_cust-link"
                    )
                ],
                style={"textAlign": "center", "marginTop": "10px"}
            )
        else:
            # comment me back in!!!!!!!!! 
            # weapon_div = html.Div(
            #     html.Span(f"Customized Weapon: {customized_weapon}", className="name"),
            #     style={"textAlign": "center", "marginTop": "10px"}
            # )\
            gun_name = new_request_list[7][1]
            # print(gun_name)
            weapon_div = html.Div(
                [
                    html.Span("Customized Weapon: Yes", className="name"),
                    html.Span(" | "),
                    dcc.Link(
                        "Gun Customizer",
                        href=f"/gun_customizer?gun={gun_name}",
                        className="gun_cust-link"
                    )
                ],
                style={"textAlign": "center", "marginTop": "10px"}
            )

        data = html.Div([
            html.Div(boxes, className="my-div-style"),
            weapon_div
        ])

        return data

    except Exception as e:
        print(e)
        return [html.Div(f"Error: {e}", className="box") for _ in range(10)]