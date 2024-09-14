import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import pulp
from dash import dash_table
from dash import dcc

# import dash_html_components as html
from dash import html


title_style = {"margin-top": "20px", "margin-left": "20px"}

cornflower_blue_button_style = {
    "width": "50%",
    "height": "50%",
    "background-color": "Bright Blue",
    "color": "gray",
    "margin-top": "20px",
    "border-radius": "10px",
    "margin-left": "100px",
}

gray_button_style = {
    "marginLeft": "20%",
    "width": "50%",
    "height": "80%",
    "fontSize": "1rem",
    "paddingLeft": "1px",
    "paddingRight": "1px",
    "background-color": "#007bff",
    "color": "white",
    "border-radius": "10px",
}


Layout = html.Div(
    [
        html.Div(
            className="study-browser-banner row",
            children=[
                html.H2(
                    className="title",
                    children="Shopping Optimizer and Recommender",
                    style=title_style,
                ),
            ],
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label("Product Name"),
                                        dcc.Input(
                                            id="product_name",
                                            type="text",
                                            placeholder="Enter product name",
                                        ),
                                        html.Br(),
                                        html.Br(),
                                        html.Label("Min Quantity"),
                                        dcc.Input(
                                            id="min_qty",
                                            type="number",
                                            placeholder="Enter minimum quantity",
                                        ),
                                        html.Br(),
                                        html.Br(),
                                        html.Label("Max Quantity"),
                                        dcc.Input(
                                            id="max_qty",
                                            type="number",
                                            placeholder="Enter maximum quantity",
                                        ),
                                        html.Br(),
                                        html.Br(),
                                        html.Label("Unit Price"),
                                        dcc.Input(
                                            id="unit_price",
                                            type="number",
                                            placeholder="Enter unit price",
                                        ),
                                        html.Br(),
                                        html.Br(),
                                        html.Label("Discount Rate (%)"),
                                        dcc.Input(
                                            id="discount_rate",
                                            type="number",
                                            placeholder="Enter discount rate",
                                        ),
                                        html.Br(),
                                        html.Br(),
                                        html.Div(
                                            [
                                                html.Button(
                                                    "ADD ITEM",
                                                    id="add_button",
                                                    n_clicks=0,
                                                    style=gray_button_style,
                                                )
                                            ]
                                        ),
                                        html.Br(),
                                        html.Div(id="total_cost_initial"),
                                    ],
                                    className="box",
                                    style={"height": "25%", "width": "95%"},
                                ),
                                html.Br(),
                                html.Br(),
                                html.Label("Shopping Budget"),
                                dcc.Input(
                                    id="budget",
                                    type="number",
                                    placeholder="Enter your budget",
                                ),
                                html.Br(),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Button(
                                            "OPTIMIZE",
                                            id="optimize_button",
                                            n_clicks=0,
                                            style=gray_button_style,
                                        )
                                    ]
                                ),
                                html.Br(),
                                html.Div(id="total_cost_optimized"),
                            ],
                            className="box",
                            style={"padding-bottom": "12px"},
                        ),
                    ],
                    style={"width": "27%"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    # style={"width": "75%", "padding": "5px"},
                                    children=[
                                        html.H2("Your Shopping List"),
                                        html.H6(
                                            "The total cost is calculate based on maximum quantity and discount rate"
                                        ),
                                        dcc.Graph(id="shopping_table"),
                                        # html.Hr(),
                                        html.H2("Optimized Shopping List"),
                                        html.H6(
                                            "The recommended quantities are calculated based on the budget stated"
                                        ),
                                        dcc.Loading(
                                            id="loading",
                                            type="circle",
                                            children=[
                                                dcc.Graph(id="optimization_results"),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                            className="box",
                            style={"padding-bottom": "15px"},
                        ),
                    ],
                    style={"width": "73%"},
                ),
            ],
            className="row",
        ),
    ]
)
