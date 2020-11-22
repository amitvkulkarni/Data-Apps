# Import required libraries
import pickle
import copy
import pathlib
import urllib.request
import dash_table
import dash
import math
import pandas as pd
import numpy as np
import datetime as dt
import base64
import io
import os
import base64
import seaborn as sn
import matplotlib as plt
import pandas as pd
import dash_daq as daq
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
#from fileUpload import *
from models import *
from defintion import *
from multiModel import multiModel
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
from dash.dependencies import Input, Output, State, ClientsideFunction


models = ['LGBM', 'Random Forest', 'KNN', 'GNB', 'DT', 'ADABoost','Logistic']
FONTSIZE = 20
FONTCOLOR = "#F5FFFA"
BGCOLOR ="#3445DB"


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)


server = app.server

toast_datasplit = html.Div(
    [     
        dbc.Toast(
            html.Div([
                html.Div('Data set split completed', style={'color': 'green', 'fontSize': 18}),
            ], style={'marginBottom': 50, 'marginTop': 25}),    
            id="auto-toast",
            duration=3000,
            style={"position": "fixed", "top": 10, "right": 1, "width": 350},
        ),
    ]
)

toast_model = html.Div(
    [     
        dbc.Toast(
            html.Div([
                html.Div('Model needs optimization', style={'color': 'red', 'fontSize': 18}),
            ], style={'marginBottom': 50, 'marginTop': 25}),    
            id="auto-toast-model",
            duration=4000,
            style={"position": "fixed", "top": 30, "right": 1, "width": 350},
        ),
    ]
)

""" toast_fileUpload = html.Div(
    [     
        dbc.Toast(
            html.Div([
                html.Div('Files uploading completed', style={'color': 'green', 'fontSize': 18}),
            ], style={'marginBottom': 50, 'marginTop': 25}),    
            id="output-data-upload",
            duration=4000,
            style={"position": "fixed", "top": 30, "right": 1, "width": 350},
        ),
    ]
) """


upload_layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    
    
])



def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(dt.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])



PAGE_SIZE = 10
# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
    
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.PNG"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",

                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H1(
                                    "CLASSIFICATION MODELS",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Simulation Overview", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                                
                html.Div(
                    [
                        toast_datasplit,
                        toast_model,

                        html.A(
                            
                            html.Button("Code", id="learn-more-button"),
                            href="https://github.com/amitvkulkarni/Data-Apps/tree/main/Classification%20Model%20Simulator%20with%20Plotly-Dash",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "File Upload:",
                            className="control_label",
                        ),
                        upload_layout,
                        html.Div(id='slider-output-container'),
                        html.Br(),
   
                        daq.Slider(
                            id = 'slider',
                            min=0,
                            max=100,
                            value=70,
                            handleLabel={"showCurrentValue": True,"label": "SPLIT"},
                            step=10
                        ),

                        html.P("Select Target", className="control_label"),
                        dcc.Dropdown(
                            id="select_target",
                            options=[{'label':x, 'value':x} for x in obj_Data.df_train_dummies.columns],
                            multi=False,
                            value='Loan_Status',
                            clearable=False,
                            className="dcc_control",
                        ),
                         html.P("Select Variables", className="control_label"),
                        dcc.Dropdown(
                            id="select_independent",
                            options=[{'label':x, 'value':x} for x in obj_Data.df_train_dummies.columns],
                            value= list(obj_Data.df_train_dummies.columns),
                            multi=True,
                            className="dcc_control",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P("Select Number of KFOLD Splits", className="control_label"),

                                        daq.NumericInput(
                                            id='id-daq-splits',
                                            min=0,
                                            max=10,
                                            size = 75,
                                            value=2
                                        ),  
  
                                    ],className="row flex-display",
                                ),
     
                             ]
                        ),
                        html.P("Models", className="control_label"),
                        dcc.Dropdown(
                            id="select_models",
                            options = [{'label':x, 'value':x} for x in models],
                            value = models,
                            multi=True,
                            clearable=False,
                            className="dcc_control",

                        ),
                        html.Div(
                            id = 'best-model', style={'color': 'blue', 'fontSize': 15} 
                        ),html.Br(),
                        daq.PowerButton(
                            id = 'id-daq-switch-model',
                            on='True',
                            color='#1ABC9C', 
                            size = 75,
                            label = 'Initiate Model Buidling'
                        ) ,
                                                                                               
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                #--------------------------------------------------------------------------------------------------------------------
                html.Div(
                    [
                         html.Div(
                            daq.LEDDisplay(
                                id='records',
                                #label="Default",
                                value=0,
                                label = "Records",
                                size=FONTSIZE,
                                color = FONTCOLOR,
                                backgroundColor=BGCOLOR
                            )
                        ),html.Br(),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        daq.LEDDisplay(
                                            id='trainset',
                                            #label="Default",
                                            value=0,
                                            label = "Train",
                                            size=FONTSIZE,
                                            color = FONTCOLOR,
                                            backgroundColor=BGCOLOR
                                        ),
                                        daq.LEDDisplay(
                                            id='testset',
                                            #label="Default",
                                            value=0,
                                            label = "Test",
                                            size=FONTSIZE,
                                            color = FONTCOLOR,
                                            backgroundColor=BGCOLOR
                                        ),
                                    ],className="row flex-display",
                                )
                            ]
                        ),
                        html.Br(),
                        html.Div([
                            html.Div(
                                [
                                    daq.LEDDisplay(
                                        id='numeric',
                                        #label="Default",
                                        value=0,
                                        label = "numeric",
                                        size=FONTSIZE,
                                        color = FONTCOLOR,
                                        backgroundColor=BGCOLOR
                                    ),
                                    daq.LEDDisplay(
                                        id='variables',
                                        #label="Default",
                                        value=0,
                                        label = "variables",
                                        size=FONTSIZE,
                                        color = FONTCOLOR,
                                        backgroundColor=BGCOLOR
                                    ),
                                    daq.LEDDisplay(
                                        id='categorical',
                                        #label="Default",
                                        value=0,
                                        label = "categorical",
                                        size=FONTSIZE,
                                        color = FONTCOLOR,
                                        backgroundColor=BGCOLOR
                                    )
                                ],className="row flex-display",
                            )
                        ]

                        ),
                        html.Br(),
                        html.Div(
                            [
                                html.Div(
                                  [
                                        daq.LEDDisplay(
                                            id='precision',
                                            #label="Default",
                                            value=0,
                                            label = "Precision",
                                            size=FONTSIZE,
                                            color = FONTCOLOR,
                                            backgroundColor=BGCOLOR
                                        ),
                                        daq.LEDDisplay(
                                                id='recall',
                                                #label="Default",
                                                value=0,
                                                label = "Recall",
                                                size=FONTSIZE,
                                                color = FONTCOLOR,
                                                backgroundColor=BGCOLOR
                                        ),
                                         
                                    ],className="row flex-display",
                                )
  
                            ],className="row flex-display",
                        ),    
                        html.Br(),   
                        html.Div(
                            [
                                html.Div(
                                  [
                                        daq.LEDDisplay(
                                            id='accuracy',
                                            #label="Default",
                                            value=0,
                                            label = "Accuracy",
                                            size=FONTSIZE,
                                            color = FONTCOLOR,
                                            backgroundColor=BGCOLOR
                                        ),   
                                        daq.LEDDisplay(
                                            id='auc',
                                            #label="Default",
                                            value= 0,
                                            label = "AUC",
                                            size=FONTSIZE,
                                            color = FONTCOLOR,
                                            backgroundColor=BGCOLOR
                                        ),  
                                        
                                    ],className="row flex-display",
                                )
  
                            ],className="row flex-display",
                        ),                  
                     
                    ],
                    className="pretty_container two columns",
                    id="cross-filter-options1",
                ),
                #--------------------------------------------------------------------------------------------
                html.Div(
                    [                                                 
                        html.Div(
                            [
                                html.Div(
                                    [dcc.Graph(id="main_graph")],
                                    className="pretty_container six columns",
                                ),
                                html.Div(
                                    [dcc.Graph(id="aggregate_graph")],
                                    className="pretty_container six columns",
                                ),                         

                            ],
                            className="row flex-display",
                        ),

                        html.Div(
                            [     
                                html.Div(
                                    [dcc.Graph(id="pie_graph", figure = multiModel.corelationMatrix())],
                                    className="pretty_container six columns",
                                ),                                  
                                html.Div(
                                    [dcc.Graph(id="aggregate_graph1", figure = multiModel.featureImportance())],
                                    className="pretty_container six columns",
                                ),
                            ],
                        ),                        
                    ],
                    id="right-column",
                    className="eight columns",
                ),
               
            ],
            className="row flex-display",
        ),
         html.Div(
            [
                html.Div(
                        [dcc.Graph(id="model-graphs", figure={})],
                        className="pretty_container seven columns",
                ), 
                html.Div(
                    [dcc.Graph(id="individual_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [
                        daq.GraduatedBar(
                            id='model-graduated-bar',
                            label="Model Performance",
                            max = 100,
                            color={"ranges":{"green":[70,100],"yellow":[50,70],"red":[0,50]}},
                            showCurrentValue=True,
                            value=50
                        ) ,   
                        html.Br(),
                        html.Div(
                            #[
                                html.Div(
                                    id='id-insights', style={'color': 'blue', 'fontSize': 15}                     
                                )
                            
                            #],className="pretty_container six columns",
                        )
                    ],className="pretty_container six columns",
                ),

            
            ],
            className="row flex-display",
        ),
       

        html.Div(
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in multiModel.df_head.columns],
                data = multiModel.df_head.to_dict('records'),
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current= 0,
                page_size= 10,
            )
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

@app.callback(
    [
        Output("records", "value"),        
        Output("variables", "value"),
        Output("numeric", "value"),
        Output("categorical", "value")
       
    ],           
    Input("aggregate_data", "data")
)
def update_text(data):
    numeric_var = len([i for i in list(obj_Data.df.columns) if obj_Data.df.dtypes[i] in ['float64','int64']])
    cat_features = len([i for i in list(obj_Data.df.columns) if obj_Data.df.dtypes[i] in ['float64']])
    return str(obj_Data.df.shape[0]), str(obj_Data.df.shape[1]), str(numeric_var), str(cat_features)


@app.callback(
    Output('auto-toast', 'is_open'),
    [Input('slider', 'value')]
)
def open_toast(value):
    return True


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
        


@app.callback(
    [
        Output("main_graph", 'figure'),
        Output("individual_graph", 'figure'),
        Output("aggregate_graph", 'figure'),
        Output("slider-output-container", 'children'),
        Output("precision", 'value'),
        Output("recall", 'value'),
        Output("accuracy", 'value'),
        Output("auc", 'value'),
        Output("trainset", 'value'),
        Output("testset", 'value'),
        Output('model-graduated-bar', 'value'),
        Output('id-insights', 'children'),
        Output("model-graphs", 'figure'),     
        Output("best-model", 'children'), 
        Output("id-daq-switch-model", 'on'),
        Output('auto-toast-model', 'is_open')
        
    ],
    [
        Input("select_target", "value"),
        Input("select_independent", "value"),
        Input("slider", "value"),
        Input("id-daq-splits", "value"),
        Input("select_models", "value")        
    ]
)
def measurePerformance(target, independent, slider, splits, selected_models):
    fig_ROC, Fig_Precision, fig_Threshold,precision, recall, accuracy, trainX, testX, auc, fig_model, bestModel = multiModel.getModels(target,independent, slider, splits, selected_models)
    auc_toast = True if auc < 0.5 else False
    return fig_ROC, Fig_Precision, fig_Threshold, 'Train / Test split size: {} / {}'.format(slider, 100-slider), precision, recall, accuracy,auc, trainX, testX, auc*100, f'The best performing model is {bestModel} with accuracy of {accuracy}, precision of {precision} and recall of {recall} with Area under curve of {auc}. Try for various K FOLD values to explore further.' ,fig_model, f'The top performaing model is {bestModel}', True, auc_toast

     

@app.callback(
    Output('select_independent', 'value'),
    Input('select_target', 'value')    
)
def variablesPopulate(y):
    return  [x for x in obj_Data.df_train_dummies.columns if x != y]
    



if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)


