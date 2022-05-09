import dash
import dash_table
# from dash import dash_table
import dash_daq as daq
import dash_core_components as dcc
# from dash import dcc
import dash_html_components as html
# from dash import html,Input, Output, State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pre_processing as pp



gray_button_style = {'marginLeft': '20%', 
                    'width': '50%',
                    'height':'80%',
                    "fontSize": "1rem",
                    "paddingLeft": "1px",
                    "paddingRight": "1px",
                    'background-color': '#007bff',
                    'color': 'white',
                    'border-radius': '10px'}

cornflower_blue_button_style = {'width': '50%', 
                                'height':'50%',
                                'background-color': 'Bright Blue',
                                'color': 'gray',
                                'margin-top': '20px',
                                'border-radius': '10px',
                                "margin-left": "100px"}

title_style = {'margin-top': '20px',
               'margin-left': '20px'}

# footer_style = {'background-color': 'Gray',}


layout_all = html.Div([


    html.Div(
        className="study-browser-banner row",
        children=[
            # html.Div(
            #     className="div-logo",
            #     children=html.Img(
            #         className="logo", src="./assets/dash-logo.png"
            #     ),
            # ),
                        
            html.H2(className="title", 
                    children="Monte Carlo Simulation For Pipe Failure", style = title_style),

            # html.A(                            
            #     html.Button("CODE", id="learn-more-button", style = cornflower_blue_button_style),
            #     href="https://github.com/amitvkulkarni/Data-Apps/tree/main/Classification%20Model%20Simulator%20with%20Plotly-Dash", target = "_blank"
            # ),
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
                        value=65,
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
                        value=7,
                        handleLabel={
                            "showCurrentValue": True, "label": "Value"},
                        step=1
                    ),
                ], className='box', style={'height': '25%', 'width': '95%'}),
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
                        value=7,
                        handleLabel={
                            "showCurrentValue": True, "label": "Value"},
                        step=1
                    ),
                ], className='box', style={'height': '25%', 'width': '95%'}),
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
                        value=7,
                        handleLabel={
                            "showCurrentValue": True, "label": "Value"},
                        step=1
                    ),
                ], className='box', style={'height': '25%', 'width': '95%'}),
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
                
                ], className='box', style={'height': '25%', 'width': '95%'}),
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
                    html.Div(id='textarea-description', style={'whiteSpace': 'pre-line'}),
                    html.Img(className="logo1", src="./assets/hoopstress.jpg"),
                    html.Img(className="logo1", src="./assets/equation.png", style={'height':'20%', 'width':'50%', 'marginLeft': '10%'})
               
            ]),
                
            ],className='boxImage', style={'padding-bottom': '15px'}),

        ], style={'width': '73%'}),

    ], className='row'),
    
    html.Div(
        className="footer-banner row",
        children=[
            html.Div(
                className="div-logo",
                children=html.Img(
                    className="logo", src="./assets/dash-logo.png"
                ),
            ),
                        
            # html.H2(className="title", 
            #         children="Monte Carlo Simulation For Pipe Failure", style = title_style),

            html.A(                            
                html.Button("CODE", id="learn-more-button", style = cornflower_blue_button_style),
                href="https://github.com/amitvkulkarni/Data-Apps/tree/main/Monte%20Carlo%20Simulation%20for%20Pipe%20Failure", target = "_blank"
            ),
        ],
       
    ),
    
])
