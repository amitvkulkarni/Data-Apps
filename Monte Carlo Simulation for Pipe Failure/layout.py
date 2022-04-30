import dash
import dash_table
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pre_processing as pp


gray_button_style = {'marginLeft': '20%', 'width': '50%', 'height':'40%',
                    "fontSize": "1rem",
                    "paddingLeft": "1px",
                    "paddingRight": "1px",
                    'background-color': 'Black',
                    'color': 'white',
                    'border-radius': '10px'}

cornflower_blue_button_style = {'width': '100%', 'height':'40%',
                    'background-color': 'Bright Blue',
                    'color': 'gray',
                    'border-radius': '10px'}


layout_all = html.Div([
    


    html.Div(
        className="study-browser-banner row",
        children=[
            html.Div(
                className="div-logo",
                children=html.Img(
                    className="logo", src="./assets/dash-logo.png"
                ),
            ),
            html.H2(className="h2-title",
                    children="Monte Carlo Simulation For Pipe Failure"),

            html.A(                            
                html.Button("CODE", id="learn-more-button", style = cornflower_blue_button_style),
                href="https://github.com/amitvkulkarni/Data-Apps/tree/main/Classification%20Model%20Simulator%20with%20Plotly-Dash", 
                target = "_blank"
            ),
        ],
    ),

    html.Div([
        html.Div([

            html.Div([

                html.Div([
                    html.H3('Diameter'),
                    daq.Slider(
                        id='val-diameter',
                        min=0,
                        max=100,
                        value=50,
                        handleLabel={
                            "showCurrentValue": True, "label": "Value"},
                        step=10
                    ),
                    html.Br(),
                    html.H3('Diameter Cov'),
                    daq.Slider(
                        id='val-diameter-cov',
                        min=0,
                        max=10,
                        value=5,
                        handleLabel={
                            "showCurrentValue": True, "label": "Value"},
                        step=1
                    ),
                ], className='box', style={'height': '25%', 'width': '80%'}),
                html.Div([
                    html.H3('Thickness'),
                    daq.Slider(
                        id='val-thickness',
                        min=0,
                        max=100,
                        value=65,
                        handleLabel={
                            "showCurrentValue": True, "label": "Value"},
                        step=10
                    ),
                    html.Br(),
                    html.H3('Thickness Cov'),
                    daq.Slider(
                        id='val-thickness-cov',
                        min=0,
                        max=10,
                        value=5,
                        handleLabel={
                            "showCurrentValue": True, "label": "Value"},
                        step=1
                    ),
                ], className='box', style={'height': '25%', 'width': '80%'}),
                html.Div([
                    html.H3('Yield Strength'),
                    daq.Slider(
                        id='val-strength',
                        min=0,
                        max=100,
                        value=65,
                        handleLabel={
                            "showCurrentValue": True, "label": "Value"},
                        step=10
                    ),
                    html.Br(),
                    html.H3('Yield Strength Cov'),
                    daq.Slider(
                        id='val-strength-cov',
                        min=0,
                        max=10,
                        value=5,
                        handleLabel={
                            "showCurrentValue": True, "label": "Value"},
                        step=1
                    ),
                ], className='box', style={'height': '25%', 'width': '80%'}),
                html.Div([
                    html.H3('Internal Pressure'),
                    daq.Slider(
                        id='val-internal-pressure',
                        min=0,
                        max=1000,
                        value=700,
                        handleLabel={
                            "showCurrentValue": True, "label": "Value"},
                        step=10
                    ),
                
                ], className='box', style={'height': '25%', 'width': '80%'}),
                html.Br(),
                                
                html.Div([
                    html.Button('RUN SIMULATION', id='btn-run-simulation', n_clicks=0, style = gray_button_style)  
                ]), 

            ], className='box', style={'padding-bottom': '12px'}),

        ], style={'width': '27%'}),
        
 
        
        html.Div([
            html.Div([
                html.Div([
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children = dcc.Graph(id='plt-failure')
                    ),
                 ]),
               
            ], className='box', style={'padding-bottom': '15px'}),
            
            html.Div([
                 html.Div([
                    html.Img(className="logo1", src="./assets/hoopstress.jpg")
            ])
                
            ],className='box', style={'padding-bottom': '15px'}),

        ], style={'width': '60%'}),

    ], className='row'),
    
])
