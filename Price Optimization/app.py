import dash
import pandas as pd
import numpy as np
import dash_table
import logging
import plotly.graph_objs as go
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import Python.optimize_price
import Python.optimize_quantity
import dash_daq as daq

group_colors = {"control": "light blue", "reference": "red"}

app = dash.Dash(
    __name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width"}],
)

server = app.server

# Load the data
df = pd.read_csv('Data/price.csv')
df.head(10)

# App Layout
app.layout = html.Div(
    children=[
        # Error Message
        html.Div(id="error-message"),
        # Top Banner
        html.Div(
            className="study-browser-banner row",
            children=[
                html.H2(className="h2-title",
                        children="PRODUCT PRICE OPTIMIZATION"),

                html.Div(
                    className="div-logo",
                    children=html.Img(
                        className="logo", src=app.get_asset_url("dash-logo-new.png")
                    ),
                ),

            ],
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            className="padding-top-bot",
                            children=[
                                html.H6("OPTIMIZE"),
                                dcc.RadioItems(
                                    id="selected-var-opt",
                                    options=[
                                        {
                                            "label": "Price",
                                            "value": "price"
                                        },
                                        {
                                            "label": "Quantity",
                                            "value": "quantity"
                                        },

                                    ],
                                    value="price",
                                    labelStyle={
                                        "display": "inline-block",
                                        "padding": "12px 12px 12px 12px",
                                    },
                                ),
                            ],
                        ),
                        html.Br(),
                        html.Div(
                            className="padding-top-bot",
                            children=[

                                html.H6("OPTIMIZATION RANGE"),
                                html.Div(
                                    id='output-container-range-slider'),
                                dcc.RangeSlider(
                                    id='my-range-slider',
                                    min=0,
                                    max=500,
                                    step=1,
                                    marks={
                                        0: '0',
                                        500: '500'
                                    },
                                    value=[200, 400]
                                ),



                            ],
                        ),


                        html.Br(),
                        html.Div(
                            className="padding-top-bot",
                            children=[
                                html.H6("FIXED COST"),
                                daq.NumericInput(
                                    id='selected-cost-opt',
                                    min=0,
                                    max=10000,
                                    value=80
                                )
                                # dcc.Input(
                                #     id = "selected-cost-opt",
                                #     placeholder='Enter fixed cost...',
                                #     type='text',
                                #     value='80'
                                # ),

                            ],
                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        
                        html.H6("RECOMMENDATION:"),
                        html.Div(
                            id = 'id-insights', style={'color': 'DarkCyan', 'fontSize': 15} 
                        ),
                        html.Br(),                    
                        html.Div(dbc.Button("GET CODE", color="primary", className="mr-1", href="https://github.com/amitvkulkarni/Data-Apps/tree/main/Price%20Optimization",target='_blank')),



                    ],
                    className="pretty_container two columns",
                    id="cross-filter-options",
                ),

            ],
        ),


        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            className="twelve columns card-left",
                            children=[
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("PRICE VS QUANTITY"),
                                        dcc.Graph(id="lineChart2"),
                                    ],
                                )
                            ],
                        ),


                    ],
                    className="pretty_container four columns",

                ),
                html.Div(
                    [
                        html.Div(
                            className="twelve columns card-left",
                            children=[
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("MAXIMIZING REVENUE"),
                                        dcc.Graph(id="lineChart1"),
                                    ],
                                )
                            ],
                        ),


                    ],
                    className="pretty_container four columns",

                ),


                html.Div(
                    [
                        html.Div(
                            className="twelve columns card-left",
                            children=[
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        # html.Div(id="table1"),
                                        html.H6("SIMULATED RESULT"),
                                        dash_table.DataTable(

                                            id='heatmap',
                                            columns=[
                                                {'name': 'Price', 'id': 'Price',
                                                    'type': 'numeric'},
                                                {'name': 'Revenue', 'id': 'Revenue',
                                                    'type': 'numeric'},
                                                {'name': 'Quantity', 'id': 'Quantity',
                                                    'type': 'numeric'},
                                            ],
                                            style_data_conditional=[
                                                {
                                                    'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                },
                                                {
                                                    'if': {
                                                        'row_index': 0,  # number | 'odd' | 'even'
                                                        'column_id': 'Revenue'
                                                    },
                                                    'backgroundColor': 'dodgerblue',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'row_index': 0,  # number | 'odd' | 'even'
                                                        'column_id': 'Price'
                                                    },
                                                    'backgroundColor': 'dodgerblue',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'row_index': 0,  # number | 'odd' | 'even'
                                                        'column_id': 'Quantity'
                                                    },
                                                    'backgroundColor': 'dodgerblue',
                                                    'color': 'white'
                                                },
                                            ],
                                            style_header={
                                                'backgroundColor': 'rgb(230, 230, 230)',
                                                'fontWeight': 'bold',
                                                # 'border': '1px solid black'
                                            },
                                            style_data={
                                                'whiteSpace': 'normal',
                                                'height': 'auto',
                                            },
                                            editable=True,
                                            filter_action="native",
                                            sort_action="native",
                                            page_size=10,

                                        ),
                                    ],
                                )
                            ],
                        ),

                    ],
                    className="pretty_container two columns",

                ),
            ],
        ),
    ]
)


@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_output(value):
    return "{}".format(value)


@app.callback(
    [
        Output("heatmap", 'data'),
        Output("lineChart1", 'figure'),
        Output("lineChart2", 'figure'),
        Output("id-insights", 'children'), 
    ],
    [
        Input("selected-var-opt", "value"),
        Input("my-range-slider", "value"),
        Input("selected-cost-opt", "value")
    ]

)
def update_output_All(var_opt, var_range, var_cost):

    try:
        if var_opt == 'price':
            res, fig_PriceVsRevenue, fig_PriceVsQuantity, opt_Price, opt_Revenue = Python.optimize_price.fun_optimize(
                var_opt, var_range, var_cost, df)
            res = np.round(res.sort_values(
                'Revenue', ascending=False), decimals=2)

            if opt_Revenue > 0:
                return [res.to_dict('records'), fig_PriceVsRevenue, fig_PriceVsQuantity, 
                    f'The maximum revenue of {opt_Revenue} is achieved by optimizing {var_opt} of {opt_Price}, fixed cost of {var_cost} and optimization was carried for {var_opt} range between {var_range}']
            else:
                return [res.to_dict('records'), fig_PriceVsRevenue, fig_PriceVsQuantity, 
                    f'For the fixed cost of {var_cost} and {var_opt} range between {var_range}, you will incur loss in revenue']

        else:
            res, fig_QuantityVsRevenue, fig_PriceVsQuantity, opt_Quantity,opt_Revenue  = Python.optimize_quantity.fun_optimize(
                var_opt, var_range, var_cost, df)
            res = np.round(res.sort_values(
                'Revenue', ascending=False), decimals=2)
            

            if opt_Revenue  > 0:
                return [res.to_dict('records'), fig_QuantityVsRevenue, fig_PriceVsQuantity, 
                    f'The maximum revenue of {opt_Revenue} is achieved by optimizing {var_opt} of {opt_Quantity}, fixed cost of {var_cost} and optimization was carried for {var_opt} range between {var_range}']
            else:
                return [res.to_dict('records'), fig_QuantityVsRevenue, fig_PriceVsQuantity, 
                    f'For the fixed cost of {var_cost} and {var_opt} range between {var_range}, you will incur loss in revenue']
    
    
    except Exception as e:
        logging.exception('Something went wrong with interaction logic:', e)


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False, dev_tools_ui=False)
