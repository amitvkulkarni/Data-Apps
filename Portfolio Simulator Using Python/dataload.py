import pandas as pd
import numpy as np
import datetime
from datetime import date
from nsepy import get_history as gh



##################################################################
# Data Loading
##################################################################
def load_stock_data(start_date, end_date, ticker):
    """_summary_

    Args:
        start_date (Date): Start data for stock selection
        end_date (Date): End date for stock selection
        ticker (List): List of stocks

    Returns:
        Dataframe: price data for selected stock for a selected period
    """
    try:
        df = pd.DataFrame()
        
        for i in range(len(ticker)):
            data = gh(symbol=ticker[i],start= start_date, end=end_date)[['Symbol','Close']]
            data.rename(columns={'Close':data['Symbol'][0]},inplace=True)
            data.drop(['Symbol'], axis=1,inplace=True)
            if i == 0:
                df = data
                
            if i != 0:
                df = df.join(data)
                
        
        return df
    except Exception as e:
                print(f'An exception occurred while executing data load: {e}')
                
                
                

##################################################################
# Data Loading
##################################################################

def sim_portfolio(weights, dd_returns):
    """_summary_

    Args:
        weights (List): Weights for each of the stock

    Returns:
        Float: Returns the risk at 95% percentile
    """
    try:
        tmp_pp = (weights * dd_returns.values).sum(axis=1)
        var_sim_port = np.percentile(tmp_pp, 5, interpolation = 'lower')
        return var_sim_port
    except Exception as e:
        print(f'An exception occurred while executing sim_portfolio: {e}')


def sim_bootstrap(dd_returns, company):
    """_summary_

    Args:
        dd_returns (Dataframe): the dataframe which has stock returns.
        company (List): List of stocks

    Returns:
        int: returns various metrics
    """
    
    try:

        port_returns = []
        port_volatility = []
        port_weights = []

        num_assets = len(company)
        num_portfolios = 100
        np.random.seed(1357)
        for port in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights = weights/sum(weights)
            port_weights.append(weights)
            df_wts_returns = dd_returns.mean().dot(weights)
            port_returns.append(df_wts_returns*100)
            
            var_port_95 = sim_portfolio(weights, dd_returns)
            port_volatility.append(var_port_95)
            
            
        port_weights = [wt for wt  in port_weights]
        dff = {'Returns': port_returns, 'Risk': port_volatility, 'Weights': port_weights}
        df_risk = pd.DataFrame(dff)

        min_risk = df_risk.iloc[df_risk['Risk'].idxmax()]

        # low_risk_return = f'{round(abs(min_risk[0]),4)*100:.2f}'
        # low_risk_volatility = f'{round(abs(min_risk[1]),4)*100:.2f}'
        low_risk_return = f'{round((min_risk[0]),4)*100:.2f}'
        low_risk_volatility = f'{round((min_risk[1]),4)*100:.2f}'
        low_risk_wts = min_risk[2]

        print(f'{low_risk_volatility} and {low_risk_return}')


        max_risk = df_risk.iloc[df_risk['Risk'].idxmin()]
        # high_risk_return = f'{round(abs(max_risk[0]),4)*100:.2f}'
        # high_risk_volatility = f'{round(abs(max_risk[1]),4)*100:.2f}'
        high_risk_return = f'{round((max_risk[0]),4)*100:.2f}'
        high_risk_volatility = f'{round((max_risk[1]),4)*100:.2f}'
        high_risk_wts = max_risk[2]

        print(f'{high_risk_volatility} and {high_risk_return}')
        
        return low_risk_wts, high_risk_wts, low_risk_return,low_risk_volatility, high_risk_return, high_risk_volatility, df_risk
    
    except Exception as e:
                print(f'An exception occurred while executing sim_bootstrap: {e}')