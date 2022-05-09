import dash
import time
import dash_core_components as dcc
# from dash import dcc
import dash_html_components as html
# from dash import html,Input, Output, State
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import layout
import pre_processing as pp
import dash_daq as daq


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = layout.layout_all


@app.callback(    
        [
            Output("plt-failure", 'figure'), 
            Output('textarea-description', 'children')
        ],          
        
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
    """_summary_

    Args:
        n_clicks (_type_): _description_
        diameter (int): Diameter of the pipe
        diameter_cov (int): Covariance of the diameter
        thickness (int): Thickness of the pipe
        thickness_cov (int): Covariance of the thickness
        strength (int): Strength / Yield strength of the pipe
        strength_cov (int): Covariance of the yield strength
        internal_pressue (int): Inter Pressue in the pipe.

    Returns:
        Figure: Return a line chart fig 
        str: Returns the description of the hoop stress.
    """
    
    str_description = "The pipe will fail if the Hoop stress becomes greater than its yield strength. This app will help simulate this scenario hundreds or maybe a thousand times, and calculates the probability of failure for each iteration. Depending on the result, the decision can be made to either continue to the current design or to review and redesign the pipe. Here is the mathematical way to define the hoop stress."
    fig_linechart = pp.initiate_simulation(diameter, diameter_cov, thickness, thickness_cov, strength, strength_cov, internal_pressue)    
    return fig_linechart,str_description


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, dev_tools_ui=False)
