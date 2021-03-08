# -*- coding: utf-8 -*-
import base64
import io
import dash
import pandas as pd
import numpy as np
import pathlib
import dash_table
import logging
import dash_daq as daq
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from datetime import timedelta
import layout 
import dataPreprocess


group_colors = {"control": "light blue", "reference": "red"}

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

server = app.server

tmp_df = dataPreprocess.data_load()

tmp_layout = layout.tbl_layout()
tbl_score = tmp_layout[0]
tbl_RFMVal = tmp_layout[1]
tbl_RFMAggregate = tmp_layout[2]

df9 = tmp_df[3][['CustomerID', 'Country']]
df11 = tmp_df[1][['CustomerID', 'RFM_Score', 'RFM_Level','Recency','Frequency','MonetaryValue']]
df9.drop_duplicates(subset = ['CustomerID'], inplace=True)
df12 = pd.merge(df11, df9, on='CustomerID', how='left')


"""
[data preparation for piechart generation]
"""
df_pieChart = df12[['Country','RFM_Level']].copy()
df_pieChart['RFM_Level_cnt'] = df_pieChart.groupby(['Country','RFM_Level'])['Country'].transform('count')
df_pieChart.drop_duplicates(['Country', 'RFM_Level','RFM_Level_cnt'], inplace=True)
df_pieChart.sort_values(by = ['Country'], inplace=True)
df_pieChart.reset_index()



# App Layout
app.layout = html.Div(
    children=[
        # Error Message
        html.Div(id="error-message"),
        # Top Banner
        html.Div(
            className="study-browser-banner row",
            children=[
                html.H2(className="h2-title", children="CUSTOMER LOYALTY PROGRAM"),                         
                   
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
                                    
                                    children=[
                                        #html.H6("Upload File"),
                                        dcc.Upload(
                                            id="upload-data",
                                            className="upload",
                                            children=html.Div(
                                                children=[
                                                    html.P("Drag and Drop CSV or "),
                                                    html.A("Select Files"),
                                                ]
                                            ),
                                            accept=".csv",
                                        ),
                                    ],
                                ),
                                html.Br(),
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("Select Country"),
                                        dcc.Dropdown(
                                            id="country-dropdown",
                                            options=[
                                                {"label": i, "value": i} for i in tmp_df[0]['Country'].unique()
                                            ],
                                            value='Select...'
                                        ),
                                    ],
                                ),
                                html.Br(),
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("Customer Segment"),
                                        dcc.RadioItems(
                                            id="category-type",
                                            options=[
                                                {
                                                    "label": "Champions", 
                                                    "value": "Champions"
                                                },
                                                {
                                                    "label": "Require Activation", 
                                                    "value": "Require Activation"
                                                },
                                                {
                                                    "label": "Cant Loose Them", 
                                                    "value": "Cant Loose Them"
                                                },
                                                {
                                                    "label": "Potential", 
                                                    "value": "Potential"
                                                },
                                                {
                                                    "label": "Promising", 
                                                    "value": "Promising"
                                                },
                                                {
                                                    "label": "Loyal",
                                                    "value": "Loyal",
                                                },
                                                {
                                                    "label": "Needs Attention",
                                                    "value": "Needs Attention",
                                                },
                                            ],
                                            #value="Champions",
                                            labelStyle={
                                                "display": "inline-block",
                                                "padding": "12px 12px 12px 0px",
                                            },
                                        ),
                                    ],
                                ),
                                #html.P("Interactivity"),
                                html.Br(),
                                daq.BooleanSwitch(
                                    id='daq-toggle-interactivity',
                                    on=False,
                                    color = "#2E86C1"
                                ),
                                                                                                                       
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
                                    #className="bg-white",
                                    children=[
                                        html.H6("CUSTOMER SEGMENTATION"),
                                        dcc.Graph(id="heatmap"),
                                    ],
                                )
                            ],
                        ),
                                                                                                        
                    ],
                    className="pretty_container four columns",
                    #id="cross-filter-options1",
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
                                    #className="bg-white",
                                    children=[
                                        html.H6("RECENCY & FREQUENCY DISTRIBUTION"),
                                        dcc.Graph(id="dist"),
                            ],
                        )
                        ],
                    ),
                                                                                                        
                    ],
                    className="pretty_container six columns",
                    #id="cross-filter-options1",
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
                                    #className="bg-white",
                                    children=[
                                        html.H4("RECENCY VS MONETARY"),
                                        dcc.Graph(id="fig_mr"),
                                    ],
                                )
                            ],
                        ),
                                                                                                        
                    ],
                    className="pretty_container four columns",
                    #id="cross-filter-options1",
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
                                    #className="bg-white",
                                    children=[
                                        html.H4("FREQUENCY VS MONETARY"),
                                        dcc.Graph(id="fig_mf"),
                                    ],
                                )
                            ],
                        ),
                                                                                                        
                    ],
                    className="pretty_container four columns",
                    #id="cross-filter-options1",
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
                                    #className="bg-white",
                                    children=[
                                        html.H4("FREQUENCY VS RECENCY"),
                                        dcc.Graph(id="fig_rf"),
                                    ],
                                )
                            ],
                        ),
                                                                                                        
                    ],
                    className="pretty_container four columns",
                    #id="cross-filter-options1",
                ),
            ],
        ),
      
        html.Div(
            #className="row app-body",
            children=[
                html.Div(
                    className="five columns card-left",
                    children=[
                        html.Div(
                            #className="thead-dark",
                            children=[
                                html.H6("CUSTOMER SEGMENTATION"),
                                tbl_RFMVal,
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="four columns card-left",
                    children=[
                        html.Div(
                            #className="bg-white",
                            children=[
                                html.H6("RFM SCORES"),
                                tbl_RFMAggregate,
                            ],
                        )
                    ],
                ),
                            
                dcc.Store(id="error", storage_type="memory"),
            ],
        ),
    ]
)

@app.callback(   
    Output("id_RFMVal", 'data'),   
    [ 
        Input("category-type", "value"),
        Input("country-dropdown", "value"),
        Input("daq-toggle-interactivity", "on")  
    ]
   
)
def update_output(category, country, value):
    """[summary]

    Args:
        category ([value]): [category had value selected by user from the radio buttons]
        country ([value]): [country had the selected country from the dropdown]
        value ([Boolean]): [A DAQ toggle switch value which is either True or False]

    Returns:
        [table]: [returns a dataframe to populate the table]
    """

    try:
        
        if (value == True) and ((category != None) and (country == 'Select...' )):
            filtered = df12[(df12['RFM_Level'] == category)].to_dict('records')
            return filtered
        elif (value == True) and ((category == None) and (country != 'Select...' )):
            filtered = df12[(df12['Country'] == country)].to_dict('records')
            return filtered
        elif (value == True) and ((category != None) and (country != 'Select...' )):
            filtered = df12[(df12['Country'] == country) & (df12['RFM_Level'] == category)].to_dict('records')
            return filtered
        else:
            return df12.to_dict('records')
    
    except Exception as e:
        logging.exception('Something went wrong with interaction logic for RFM_Level table:', e)
 

@app.callback(   
    Output("heatmap", 'figure'),   
    [ 
        Input("category-type", "value"),
        Input("country-dropdown", "value")  
    ]
   
)
def update_pieChart(category, country):    
    """[summary]

    Args:
        category ([value]): [category had value selected by user from the radio buttons]
        country ([value]): [country had the selected country from the dropdown]

    Returns:
        [figure]: [return the fig object which is a pie chart]
    """
    try:
        if country == "Select...":
            #filtered = df_pieChart[df_pieChart['Country'] == country]
            fig = px.pie(df_pieChart, values='RFM_Level_cnt', names='RFM_Level', template="ggplot2")
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            fig.update_layout(legend=dict(
                orientation="h",
                # yanchor="bottom",
                # y=1.02,
                # xanchor="left",
                # x=1
            ))
            logging.debug('Piechart generated successful')  
            return fig
        else:
            filtered = df_pieChart[df_pieChart['Country'] == country]
            fig = px.pie(filtered, values='RFM_Level_cnt', names='RFM_Level')
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            fig.update_layout(legend=dict(
                orientation="h",
                # yanchor="bottom",
                # y=1.02,
                # xanchor="left",
                # x=1
            ))
            return fig

    except Exception as e:
        logging.exception('Something went wrong with pie chart: ', e)


    
@app.callback(   
    Output("dist", 'figure'),   
    [ 
        Input("category-type", "value"),
        Input("country-dropdown", "value")  
    ]
   
)
def update_distChart(category, country):    
    """[This callback if for generating the dist plot for recency and frequency]
    Args:
        category ([value]): [category had value selected by user from the radio buttons]
        country ([value]): [country had the selected country from the dropdown]

    Returns:
        [figure]: [return the fig object which is a distribution plot]
    """
    filtered = df12.copy()
  
    try:
        if (country != "Select..."):
            filtered = filtered[(filtered['Country'] == country)]            
            hist_data  = [np.log(filtered['Recency']), np.log(filtered['Frequency'])]
            group_labels = ['Recency', 'Frequency']
            fig = ff.create_distplot(hist_data, group_labels, bin_size=.2)
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            fig.update_layout(legend=dict(
                orientation="h"
            ))
            logging.debug('Distribution chart generated successful')  
            return fig
        else:
            hist_data  = [np.log(filtered['Recency']), np.log(filtered['Frequency'])]
            group_labels = ['Recency', 'Frequency']
            fig = ff.create_distplot(hist_data, group_labels, bin_size=.2)
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            fig.update_layout(legend=dict(
                orientation="h"
            ))
            logging.debug('Distribution chart generated successful')  
            return fig

    except Exception as e:
        logging.exception('Something went wrong with distribution chart: ', e)

@app.callback(   
    [
        Output("fig_mr", 'figure'),   
        Output("fig_mf", 'figure'),   
        Output("fig_rf", 'figure')
    ],
    Input("country-dropdown", "value")    
   
)
def update_rfmScatterPlot(country):  

    df_rfmScatterPlot = df12.copy()  
    df_rfmScatterPlot_filtered = df_rfmScatterPlot[df_rfmScatterPlot['Country'] == country]

    try:
        if country != "Select...":
            
            fig_mr = px.scatter(df_rfmScatterPlot_filtered, x="Recency", y="MonetaryValue", size="RFM_Score", color="RFM_Level",
                       hover_name="Country", log_x=True,  size_max=10)
            fig_mr.update_layout(showlegend=False)
            #fig_mr.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            # fig_mr.update_layout(legend=dict(
            #     orientation="h"
            # ))

            fig_mf = px.scatter(df_rfmScatterPlot_filtered, x="Frequency", y="MonetaryValue", size="RFM_Score", color="RFM_Level",
                       hover_name="Country", log_x=True,size_max=10)
            fig_mf.update_layout(showlegend=False)
            #fig_mf.update_layout(margin=dict(t=0, b=0, l=0, r=0))            
            # fig_mf.update_layout(legend=dict(
            #     orientation="h"
            # ))

            fig_rf =  px.scatter(df_rfmScatterPlot_filtered, x="Frequency", y="Recency", size="RFM_Score", color="RFM_Level",
                       hover_name="Country", log_x=True,  size_max=10)
            fig_rf.update_layout(showlegend=False)
            #fig_rf.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            # fig_rf.update_layout(legend=dict(
            #     orientation="h"
            # ))

            return [fig_mr, fig_mf, fig_rf]

            logging.debug('RFM scatter plots generated successfully')  
            
        else:

            # fig_mr = px.scatter(df_rfmScatterPlot, x="Recency", y="MonetaryValue", size="RFM_Score", color="RFM_Level",
            #            hover_name="Country", log_x=True,  size_max=10)
            # fig_mr.update_layout(showlegend=False)

            fig_mr = px.scatter(df_rfmScatterPlot, x="Recency", y="MonetaryValue", size="RFM_Score", color="RFM_Level",
                       hover_name="Country", log_x=True,  size_max=10)
            fig_mr.update_layout(showlegend=False)

            fig_mf = px.scatter(df_rfmScatterPlot, x="Frequency", y="MonetaryValue", size="RFM_Score", color="RFM_Level",
                       hover_name="Country", log_x=True,size_max=10)
            fig_mf.update_layout(showlegend=False)    

            fig_rf =  px.scatter(df_rfmScatterPlot, x="Frequency", y="Recency", size="RFM_Score", color="RFM_Level",
                       hover_name="Country", log_x=True,  size_max=10)
            fig_rf.update_layout(showlegend=False)


            return [fig_mr, fig_mf, fig_rf]

    except Exception as e:
        logging.exception('Something went wrong with pie chart: ', e)
        


if __name__ == "__main__":    
    app.run_server(debug=True, use_reloader=True)


