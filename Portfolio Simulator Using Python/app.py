import dash
import pandas as pd
import numpy as np
import dash_daq as daq
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from datetime import date
import layout
import dataload




app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server


##################################################################
# The layout section
##################################################################

app.layout = layout.Financial_Portfolio_Layout


##################################################################
# The callback section
##################################################################
@app.callback(
    [
        Output('store-data', 'data'),
        Output("alert-wip-data", "is_open")
    ],
    [
        Input("id-company-dropdown","value"),
        Input("id-start-date","date"),
        Input("id-end-date","date") 
    ]    
   
)
def update_storeData(company, start_date, end_date):  
    """_summary_

    Args:
        company (List): Loads the data DCC data store with the stock data

    Returns:
        Dataframe: Returns a dataframe which has price data for selected companies
    """
    s_year = int(start_date[0:4])
    s_month = int(start_date[5:7])
    s_day = int(start_date[8:10])
    
    e_year = int(end_date[0:4])
    e_month = int(end_date[5:7])
    e_day = int(end_date[8:10])
    
    s_date = date(s_year,s_month,s_day)
    e_date = date(e_year,e_month,e_day)
    
    try:
        dataset = dataload.load_stock_data(s_date, e_date, company)
        
        dataset.reset_index(inplace = True)
        return dataset.to_dict('records'), True
    except Exception as e:
                print(f'An exception occurred while updating the data store: {e}')



@app.callback(

    [
        Output("id_low_risk", 'value'),
        # Output("id_lowrisk_returns", 'value'),
        Output("id_high_risk", 'value'), 
        # Output("id_highrisk_returns", 'value'), 
        Output("fig_allocation_low", 'figure'),
        Output("alert-wip", "is_open"),
        Output("fig_allocation_high", 'figure'),
        Output("id-info_low", 'children'),
        Output("id-info_high", 'children'),
    
    ],
    [
    Input('id-btn-create', 'n_clicks'),
    State('id-company-dropdown', 'value'),    
    State('store-data', 'data'),
    State("alert-wip", "is_open")
    

    ],
    prevent_initial_call = True
)
def update_allocation(btn_create, company, data, val_is_open):  
    """_summary_

    Args:
        company (List): Loads the data DCC data store with the stock data
        data (Dataframe): The DCC data store which has the stock data
        val_is_open (Boolean): A boolean value for displaying alert on successful generation of portfolio

    Returns:
        _type_: _description_
    """
    button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    global df_risk
    
    if button_id == 'id-btn-create':
    
        try:
            ddf = pd.DataFrame.from_records(data, index=['Date'])
            ddf = ddf[ddf.columns & company]
                
            ddf_returns = ddf.pct_change().dropna()
            dd_returns = ddf_returns.copy()
            
            ddf_cumulative = ddf_returns.copy()
            ddf.reset_index(inplace = True)
            ddf_returns.reset_index(inplace = True)
            
                    
            low_risk_wts, high_risk_wts, low_risk_return, low_risk_volatility, high_risk_return, high_risk_volatility, df_risk = dataload.sim_bootstrap(dd_returns, company)
            
            fig_allocation_low_risk = px.pie(values = low_risk_wts, names = company, hole= 0.3)
            fig_allocation_high_risk = px.pie(values = high_risk_wts, names = company, hole= 0.3)
            
            
            
            return [low_risk_volatility, 
                    # low_risk_return, 
                    high_risk_volatility, 
                    # high_risk_return, 
                    fig_allocation_low_risk, 
                    True, 
                    fig_allocation_high_risk,
                    html.Div(f'At 95% confidence, the maximum loss expected will be {low_risk_volatility} %', id="id-info_low",style={'display': 'block', 'color': 'blue', 'fontSize': 15, 'font-weight': 'bold', "text-align": "center"}),
                    html.Div(f'At 95% confidence,  the maximum loss expected will be {high_risk_volatility} %', id="id-info_low",style={'display': 'block', 'color': 'blue', 'fontSize': 15, 'font-weight': 'bold', "text-align": "center"}),
                ]
   
            
        except Exception as e:
                    print(f'An exception occurred while executing update_trendsChart(): {e}')           
            
    else:        
        return [None, 
                # None, 
                None, 
                # None,
                layout.blank_fig(), 
                None,
                layout.blank_fig(), 
                None, 
                None]
        
        
        
        

@app.callback(
    
    Output("fig_trends", 'figure'),    
    [
        Input('id-btn-create', 'n_clicks'),
        Input('id-analysis-options', 'value'),         
        State('id-company-dropdown', 'value'),       
        State('store-data', 'data')
        
        
    ],
    prevent_initial_call=True
    
        
)
def update_trends(btn_create, option_selected, company, data):
    
    """ Stock trends analysis

    Returns:
        String: The radio button selection value        
    """
    
       
    try:

        ddf = pd.DataFrame.from_records(data, index=['Date'])
        ddf = ddf[ddf.columns & company]
            
        ddf_returns = ddf.pct_change().dropna()
        dd_returns = ddf_returns.copy()
        
        ddf_cumulative = ddf_returns.copy()
        
        ddf.reset_index(inplace = True)
        ddf_returns.reset_index(inplace = True)
        
        # low_risk_wts, high_risk_wts, low_risk_return, low_risk_volatility, high_risk_return, high_risk_volatility, df_risk = dataload.sim_bootstrap(dd_returns, company)
        
        
        if option_selected ==  'STOCK PRICE TRENDS':
                    
            fig_price = px.line(ddf, x="Date", y = ddf.columns, template="simple_white")
            return fig_price
                
        elif option_selected == 'STOCK RETURNS TRENDS':
                
            fig_returns = px.line(ddf_returns, x="Date", y = ddf_returns.columns, template="simple_white")
            return fig_returns
                
        elif option_selected == 'CUMULATIVE RETURNS':
                
            df_cumulative = (ddf_cumulative+1).cumprod()
            df_cumulative.reset_index(inplace = True)
            
            fig_cumulative = px.line(df_cumulative, x="Date", y = df_cumulative.columns, template="simple_white")
            return fig_cumulative
                
        elif option_selected == 'VOLATILITY IN RETURNS':
            # df_risk['Risk'] = df_risk['Risk'].abs()
            df_risk['Risk'] = df_risk['Risk'] * 100
            fig_risk_returns = px.scatter(df_risk, x = 'Risk', y = 'Returns')        
            return fig_risk_returns
        
        else:
            return layout.blank_fig()
            
    except Exception as e:
                print(f'An exception occurred while executing update_trendsChart(): {e}')               
            
                
                
                    
        

if __name__ == "__main__":    
    app.run_server(debug=True, use_reloader=False)  
    
    
    