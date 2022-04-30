import dash
import time
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import logging
import plotly.graph_objs as go
import plotly.express as px
import layout
import pre_processing as pp
import dash_daq as daq


app = dash.Dash(__name__,)

server = app.server

app.layout = layout.layout_all


@app.callback(    
        Output("plt-failure", 'figure'),           
        
        [Input('btn-run-simulation', 'n_clicks')],
        state = [State("val-diameter", "value"),
                State("val-diameter-cov", "value"),
                State("val-thickness", "value"),
                State("val-thickness-cov", "value"),
                State("val-strength", "value"),
                State("val-strength-cov", "value"),
                State("val-internal-pressure", "value")]
    
)
def updatechart(n_clicks, diameter, diameter_cov, thickness, thickness_cov, strength, strength_cov, internal_pressue):
    
    print(f'Received values of diameter: {diameter} and {diameter_cov}')
    print(f'Received values of thickness: {thickness} and {thickness_cov}')
    print(f'Received values of strength: {strength} and {strength_cov} and internal pressue: {internal_pressue}')
    
    fig_linechart = pp.initiate_simulation(diameter, diameter_cov, thickness, thickness_cov, strength, strength_cov, internal_pressue)    
    return fig_linechart


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, dev_tools_ui=False)
