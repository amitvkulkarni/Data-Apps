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
import seaborn as sn
import matplotlib as plt
import pandas as pd
from datetime import datetime
import dash_daq as daq
import plotly.express as px
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from fileUpload import *
from models import *
from defintion import *
#from toasts import *


# df = pd.read_csv('C:/Users/kulkarna4029/OneDrive - ARCADIS/Studies/Python/Plotly_Dash/Clustering_algos/data/Train.csv')
# df_dummies = pd.get_dummies(df,columns=['Gender','Married','Education','Self_Employed','Property_Area'],drop_first=True)

models = ['Logistic', 'Random Forest', 'GBM','KNN','XGBoost','Catboost','GNB']
FONTSIZE = 20
FONTCOLOR = "#F5FFFA"
BGCOLOR ="#3445DB"

fig_featureImp = featureImportnace()

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


PAGE_SIZE = 10
# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                # daq.PowerButton(id = "power",
                #         on='True',
                #         size=50
                #     ),
                    
                                    
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
                        # html.P(
                        #     "Select Train & Test Split:",
                        #     className="control_label",
                        # ),
                        html.Div(id='slider-output-container'),
                       dcc.Slider(id = "slider",
                        min=0,
                        max=100,
                        value=70,
                        marks={
                            0: {'label': '0', 'style': {'color': '#77b0b1'}},
                            25: {'label': '25'},
                            50: {'label': '50'},
                            75: {'label': '75'},
                            100: {'label': '100', 'style': {'color': '#f50'}}
                        }
                    ),
                        # html.P("Show Data Summary", className="control_label"),
                        # dcc.RadioItems(
                        #     id="well_status_selector",
                        #     options=[
                        #         {"label": "Stats ", "value": "Stats"},
                        #         {"label": "Plots ", "value": "Plots"},
                        #         {"label": "Outliers ", "value": "Outliers"},
                        #     ],
                        #     value="Stats",
                        #     labelStyle={"display": "inline-block"},
                        #     className="dcc_control",
                        # ),
                        html.P("Select Target", className="control_label"),
                        dcc.Dropdown(
                            id="select_target",
                            options=[{'label':x, 'value':x} for x in df_dummies.columns],
                            multi=True,
                            value='Loan_Status',
                            clearable=False,
                            className="dcc_control",
                        ),
                         html.P("Select Variables", className="control_label"),
                        dcc.Dropdown(
                            id="select_independent",
                            options=[{'label':x, 'value':x} for x in df_dummies.columns],
                            value= list(df_dummies.columns),
                            multi=True,
                            className="dcc_control",
                        ),
                        html.P("Select Models", className="control_label"),
                        dcc.Dropdown(
                            id="select_models",
                            options = [{'label':x, 'value':x} for x in models],
                            value = models,
                            multi=True,
                            className="dcc_control",

                        ),
                      
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
                                value=6,
                                label = "Records",
                                size=FONTSIZE,
                                color = FONTCOLOR,
                                backgroundColor=BGCOLOR
                            )
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        daq.LEDDisplay(
                                            id='trainset',
                                            #label="Default",
                                            value=6,
                                            label = "Train",
                                            size=FONTSIZE,
                                            color = FONTCOLOR,
                                            backgroundColor=BGCOLOR
                                        ),
                                        daq.LEDDisplay(
                                            id='testset',
                                            #label="Default",
                                            value=6,
                                            label = "Test",
                                            size=FONTSIZE,
                                            color = FONTCOLOR,
                                            backgroundColor=BGCOLOR
                                        ),
                                    ],className="row flex-display",
                                )
                            ]
                        ),

                        html.Div([
                            html.Div(
                                [
                                    daq.LEDDisplay(
                                        id='numeric',
                                        #label="Default",
                                        value=6,
                                        label = "numeric",
                                        size=FONTSIZE,
                                        color = FONTCOLOR,
                                        backgroundColor=BGCOLOR
                                    ),
                                    daq.LEDDisplay(
                                        id='variables',
                                        #label="Default",
                                        value=6,
                                        label = "variables",
                                        size=FONTSIZE,
                                        color = FONTCOLOR,
                                        backgroundColor=BGCOLOR
                                    ),
                                    daq.LEDDisplay(
                                        id='categorical',
                                        #label="Default",
                                        value=6,
                                        label = "categorical",
                                        size=FONTSIZE,
                                        color = FONTCOLOR,
                                        backgroundColor=BGCOLOR
                                    )
                                ],className="row flex-display",
                            )
                        ]

                        ),
      
                        html.Div(
                            [
                                html.Div(
                                  [
                                        daq.LEDDisplay(
                                            id='precision',
                                            #label="Default",
                                            value=6,
                                            label = "Precision",
                                            size=FONTSIZE,
                                            color = FONTCOLOR,
                                            backgroundColor=BGCOLOR
                                        ),
                                        daq.LEDDisplay(
                                                id='recall',
                                                #label="Default",
                                                value=6,
                                                label = "Recall",
                                                size=FONTSIZE,
                                                color = FONTCOLOR,
                                                backgroundColor=BGCOLOR
                                        ),
                                        daq.LEDDisplay(
                                            id='accuracy',
                                            #label="Default",
                                            value=6,
                                            label = "Accuracy",
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
                                    className="pretty_container seven columns",
                                ),
                                html.Div(
                                    [dcc.Graph(id="aggregate_graph")],
                                    className="pretty_container eight columns",
                                ),                          

                            ],
                            className="row flex-display",
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
                                ) 
                            ],
                        ),
                        html.Div(
                            [
                                html.Div(id='my-output', style={'color': 'blue', 'fontSize': 15}),
                            ],className="pretty_container twelve columns",
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
                    [dcc.Graph(id="pie_graph", figure = corelationMatrix())],
                    className="pretty_container four columns",
                ),
                html.Div(
                    [dcc.Graph(id="individual_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="aggregate_graph1", figure = fig_featureImp)],
                    className="pretty_container four columns",
                ),
            ],
            className="row flex-display",
        ),
       

        html.Div(
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df_head.columns],
                data = df_head.to_dict('records'),
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


# @app.callback(
#     [
#         Output("records", "children"),        
#         Output("variables", "children"),
#         Output("numeric", "children"),
#         Output("categorical", "children")
#        # Output("describe", "children"),
#     ],
#     [Input("aggregate_data", "data")]
# )
# def update_text(data):
#     numeric_var = len([i for i in list(df.columns) if df.dtypes[i] in ['float64','int64']])
#     cat_features = len([i for i in list(df.columns) if df.dtypes[i] in ['float64']])
#     return str(df.shape[0]) + " Records", str(df.shape[1]) + " Variables", str(numeric_var) + " Numeric", str(cat_features) + " Categorical"


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
    numeric_var = len([i for i in list(df.columns) if df.dtypes[i] in ['float64','int64']])
    cat_features = len([i for i in list(df.columns) if df.dtypes[i] in ['float64']])
    return str(df.shape[0]), str(df.shape[1]), str(numeric_var), str(cat_features)


@app.callback(
    [
     Output("main_graph", 'figure'),
     Output("individual_graph", 'figure'),
     Output("aggregate_graph", 'figure'),
     Output("slider-output-container", 'children'),
     Output("precision", 'value'),
     Output("recall", 'value'),
     Output("accuracy", 'value'),
     Output("trainset", 'value'),
     Output("testset", 'value')
    ],
    [
     Input("select_target", "value"),
     Input("select_independent", "value"),
     Input("slider", "value")
    ]
)
def variableSelection(target, independent, slider):
    fig_ROC, Fig_Precision, fig_Threshold, precision, recall, accuracy, trainX, testX, auc = glm(target,independent, slider)
    #return fig_ROC, Fig_Precision, fig_Threshold, 'Train / Test split size: {} / {}'.format(slider, 100-slider),'Precision:{}'.format(precision),'Recall: {}'.format(recall),'Accuracy: {}'.format(accuracy)
    return fig_ROC, Fig_Precision, fig_Threshold, 'Train / Test split size: {} / {}'.format(slider, 100-slider), precision, recall, accuracy,trainX,testX 

# @app.callback(
#     dash.dependencies.Output('my-LED-display', 'value'),
#     [dash.dependencies.Input('slider', 'value')]
# )
# def update_output(value):
#     return str(value)


@app.callback(
    Output('auto-toast', 'is_open'),
    [Input('slider', 'value')]
)
def open_toast(value):
    return True

@app.callback(
    Output('auto-toast-model', 'is_open'),
    [
     Input("select_target", "value"),
     Input("select_independent", "value"),
     Input("slider", "value")
    ]
)
def open_toast_model(target, independent, slider):
    fig_ROC, Fig_Precision, fig_Threshold, precision, recall, accuracy, trainX, testX, auc = glm(target,independent, slider)
    if auc < 0.7:
        return True
    else:
        return False

@app.callback(
    dash.dependencies.Output('model-graduated-bar', 'value'),
    [
     Input("select_target", "value"),
     Input("select_independent", "value"),
     Input("slider", "value")
    ]
)
def update_graduatedBar(target, independent, slider):
    fig_ROC, Fig_Precision, fig_Threshold, precision, recall, accuracy, trainX, testX, auc = glm(target,independent, slider)
    return auc*100



@app.callback(
    Output('my-output', 'children'),
    Input("slider", "value")
    
)
def update_graduatedBar(value):
    return "The factors considered  | The factors considered  | The factors considered  | The factors considered  | The factors considered  | The factors considered  | The factors considered  | The factors considered  | The factors considered  | The factors considered  | The factors considered  | The factors considered  | The factors considered  | The factors considered  | The factors considered  | The factors considered  |  "




if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)


