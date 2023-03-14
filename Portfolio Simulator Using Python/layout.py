import dash
import dash_daq as daq
import plotly.graph_objs as go
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output, State
import datetime
from datetime import date


box_bound = {'box-shadow': '0px -1px 1px 2px LightGray', "text-align": "center", 'font-size': 12, 'font-weight': 'bold'}

FA_button = html.Div(
    [
        dbc.Button(
            " CREATE ", id="id-btn-create", className="me-2", n_clicks=0, style={'backgroundColor' : "blue", 
                                                                                 'font-size': 14, 
                                                                                 'font-weight': 'bold',
                                                                                 'color':'white'}
        ),
        html.Span(id="example-output", style={"verticalAlign": "middle"}),
    ]
)

##################################################################
# Specs for plots
##################################################################
def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.add_annotation(text="Select stocks to generate portfolio", font= {"size": 15, "color": 'LightGray'})
    
    return fig


Financial_Portfolio_Layout = dbc.Container([
    
    dbc.Row([
        dbc.Col([
                html.H1("VALUE AT RISK(VaR) SIMULATOR", 
                        style={"text-align": "left", 'font-size': 30, 'font-weight': 'bold', 'color': '#f8f9fa'}),
                 html.Div(
                    className="div-logo",
                    children=html.Img(
                        className="logo", src= "./assets/dash-logo-new.png"
                    ),
                ),

        ])
    
    ], className="study-browser-banner row"),
    
    
    
    html.Br(),
    
    dbc.Row([
        dbc.Col([
            
            dcc.Dropdown(
                id="id-company-dropdown",
                options = ['TATAMOTORS','DABUR', 'ICICIBANK','WIPRO','INFY','ADANIPORTS','ASIANPAINT','AXISBANK','BAJAJ-AUTO','BAJFINANCE','BAJAJFINSV','BPCL',	'BHARTIARTL','INFRATEL','CIPLA','COALINDIA','DRREDDY','EICHERMOT','GAIL','GRASIM','HCLTECH','HDFCBANK',	'HEROMOTOCO','HINDALCO','HINDPETRO','HINDUNILVR','HDFC','ITC','ICICIBANK','IBULHSGFIN',	'IOC','INDUSINDBK','INFY','JSWSTEEL','KOTAKBANK','LT','M&M','MARUTI','NTPC','ONGC','POWERGRID','RELIANCE','SBIN','SUNPHARMA','TCS','TATAMOTORS','TATASTEEL','TECHM','TITAN','UPL','ULTRACEMCO','VEDL','WIPRO','YESBANK','ZEEL'],
                value = ['TATAMOTORS','DABUR', 'ICICIBANK','WIPRO','INFY'],
                multi=True
            ),
        ], width = 6, style = box_bound),
        dbc.Col([
           dcc.DatePickerSingle(
                id = 'id-start-date',
                month_format='YYYY, MM, DD',
                placeholder='START DATE',
                date=datetime.date(2022, 2, 2),
                style = {"text-align": "center"}
            ), 
            
        ], width = 2, style = box_bound),
        dbc.Col([
           dcc.DatePickerSingle(
                id = 'id-end-date',
                month_format='YYYY, MM, DD',
                placeholder='END DATE',
                date=datetime.date(2023, 2, 2),
                style = {"text-align": "center"}
            )
            
        ], width = 2, style = box_bound),
        dbc.Col([
            FA_button
            
        ], width = 2)
        
        
    ]),
    html.Br(),  
        
    dbc.Row([
        dbc.Col([
                # html.H1("MAX LOSS FOR LOW RISK PORTFOLIO ALLOCATION @ 95% CONFIDENCE"),
                html.H1("VaR @ 95% CONFIDENCE FOR MIN PORTFOLIO RISK"),
                dcc.Loading(
                    dcc.Graph(id = 'fig_allocation_low', figure = blank_fig())
                )
            ], width = 6, style = box_bound),           
        dbc.Col([
                # html.H1("PORTFOLIO VOLATILITY FOR HGH RISK"),
                html.H1("VaR @ 95% CONFIDENCE FOR MAX PORTFOLIO RISK"),
                dcc.Loading(
                    dcc.Graph(id = 'fig_allocation_high', figure = blank_fig())
                )
            ], width = 6 ,style = box_bound)           
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(id="id-info_low")
        ], width = 6),
        dbc.Col([
            html.Div(id="id-info_high")
        ], width = 6)
        
    ]),    
    html.Br(),
    
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    daq.LEDDisplay(
                        id = 'id_low_risk',
                        label="Volatility (%)",
                        color="#FF5E5E",
                        labelPosition='top',
                        backgroundColor="#f2f2f2"
                        # value='05'
                    )   
                ])
                # dbc.Col([
                #     daq.LEDDisplay(
                #         id = 'id_lowrisk_returns',
                #         label="Returns (%)",
                #         color="#FF5E5E",
                #         labelPosition='top',
                #         backgroundColor="#f2f2f2"
                #         # value='1.2'
                #     )   
                # ])
            ])
        ], width = 6,style = box_bound),     
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    daq.LEDDisplay(
                        id = 'id_high_risk',
                        label="Volatility (%)",
                        color="#FF5E5E",
                        labelPosition='top',
                        backgroundColor="#f2f2f2"
                        # value='05'
                    )   
                ])
                # dbc.Col([
                #     daq.LEDDisplay(
                #         id = 'id_highrisk_returns',
                #         label="Returns (%)",
                #         color="#FF5E5E",
                #         labelPosition='top',
                #         backgroundColor="#f2f2f2"
                #         # value='1.2'
                #     )   
                # ])
            ])
        ], width = 6,style = box_bound),
     
    ]),
    
    
    html.Br(),

    dbc.Row([      
        dbc.Col([
                html.H1("STOCK ANALYSIS"),
                dcc.RadioItems(
                            id="id-analysis-options",
                            options=[
                                {"label": 'STOCK PRICE TRENDS',
                                    "value": 'STOCK PRICE TRENDS'},
                                {"label": 'STOCK RETURNS TRENDS',
                                    "value": 'STOCK RETURNS TRENDS'},
                                {"label": 'CUMULATIVE RETURNS',
                                    "value": 'CUMULATIVE RETURNS'},
                                {"label": 'VOLATILITY IN RETURNS',
                                    "value": 'VOLATILITY IN RETURNS'},

                            ], value= 'STOCK PRICE TRENDS',inline = True, style = {"margin-left": 2, "text-align": "left"}
                          
                        ),

            ], width = 3 ,style = box_bound),  
        dbc.Col([
                dcc.Loading(
                    dcc.Graph(id = 'fig_trends', figure = blank_fig())
                )            
        ], width = 9, style = box_bound)           
        

    ]),
    
    dbc.Row([
        html.Div(
            dbc.Alert(
                "The portfolio is successfully generated",
                id="alert-wip",
                is_open=False,
                duration=10000,
                style={"position": "fixed", "top": 50,"right": 10, "width": 250, 'backgroundColor': 'LightGray', 'color' : 'Black' },
            ),
        ),
        
    ]),
    
        
    dbc.Row([
        html.Div(
            dbc.Alert(
                "Please wait... Data is loading",
                id="alert-wip-data",
                is_open=True,
                duration=5000,
                style={"position": "fixed", "top": 50,"right": 10, "width": 250, 'backgroundColor': 'LightGray', 'color' : 'Black' },
            ),
        ),
        
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Br()
        ])
    
    ], className="study-browser-banner row"),
    
    html.Br(),
    
    dcc.Store(id='store-data', data=[], storage_type='memory')
    
        
])