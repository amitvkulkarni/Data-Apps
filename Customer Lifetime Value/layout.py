import dash
import dash_table
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pre_processing as pp

layout_all = html.Div([

    html.Div([
        html.Div([
            html.H1(children='CUSTOMER LIFETIME VALUE'),

            html.Br(),
            html.Br(),
            html.Br(),

            html.H3("Select Country"),
            dcc.Dropdown(
                id="id-country-dropdown",
                    options=[
                            {"label": i, "value": i} for i in list(pp.filtered_data.Country.unique())
                        ],
                    multi = False
                    
                )
            ]),
        html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
        
        
        html.Div(
            className="div-logo",
            children=html.Img(
                className="logo", src="./assets/logo-plotly.svg", style={'height':'75%', 'width':'75%'}
            ),
        ),

    ], className='side_bar'),


    html.Div([
        html.Div([

            html.Div([

                html.Div([

                    html.Div([
                        html.H2('Total Customers', style={
                            'font-weight': 'normal'}),
                        html.H2(id='id_total_customer', style = {'color': 'DarkSlateGray'}),
                    ], className='box_emissions'),

                    html.Div([
                        html.H2('Total Transactions', style={
                            'font-weight': 'normal'}),
                        html.H2(id='id_total_transactions', style = {'color': 'DarkSlateGray'}),
                    ], className='box_emissions'),

                    html.Div([
                        html.H2('Total Sales($)', style={
                            'font-weight': 'normal'}),
                        html.H2(id='id_total_sales', style = {'color': 'DarkSlateGray'}),
                    ], className='box_emissions'),

                    html.Div([
                        html.H2('Avg Order Value($)', style={
                            'font-weight': 'normal'}),
                        html.H2(id='id_order_value', style = {'color': 'DarkSlateGray'}),
                    ], className='box_emissions'),

                    # html.Div([
                    #     html.H2('Repeat Rate(%)', style={
                    #         'font-weight': 'normal'}),
                    #     html.H2(id='id_churn', style = {'color': 'DarkSlateGray'}),
                    # ], className='box_emissions'),


                ], style={'display': 'flex'}),

            ], className='box', style={'heigth': '25%'}),

            html.Div([
                html.Div([

                    html.Div([
                        html.Label(id='title_bar'),
                        dcc.Graph(id='fig-ProductPie'),

                    ], className='box', style={'padding-bottom': '15px'}),

                ], style={'width': '40%'}),

                html.Div([
                    html.Div([
                        # html.Label(id='title_bar1'),
                        dcc.Graph(id='fig-UnitPriceVsQuantity'),

                    ], className='box', style={'padding-bottom': '15px'}),

                ], style={'width': '60%'}),

            ], className='row'),

            html.Div([
                html.Div([
                    html.Div([
                        #  html.H2("RESULTS"),
                            dash_table.DataTable(

                                id='id-results',
                                columns=[
                                    {'name': 'CustomerID', 'id': 'CustomerID',
                                        'type': 'numeric'},
                                    {'name': 'Country', 'id': 'Country',
                                        },
                                    {'name': 'Tansactions', 'id': 'num_transactions',
                                        'type': 'numeric'},
                                    {'name': 'Money Spent($)', 'id': 'spent_money',
                                        'type': 'numeric'},
                                    {'name': 'Avg Order Value($)', 'id': 'avg_order_value',
                                        'type': 'numeric'},
                                    {'name': 'Profit Margin($)', 'id': 'profit_margin',
                                        'type': 'numeric'},
                                    {'name': 'CLV', 'id': 'CLV',
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

                             ]),

                ], style={'width': '100%'}),

            ], className='row'),



        ], className='main'),
    ]),
])

