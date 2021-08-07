import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.formula.api import ols
import plotly.express as px
import plotly.graph_objects as go


def fun_optimize(var_opt, var_range, var_cost, df):
    """[summary]

    Args:
        var_opt ([string]): [The value will be either price or quantity based on the selection made from UI]
        var_range ([int]): [The value will be maximum & minimum quantity based on selection made from range slider from UI]
        var_cost ([type]): [This is the fixed cost entered from UI]
        df ([type]): [The data set for our usecase]

    Returns:
        [list]: [Returns a dataframe for table, 
                chart for Price Vs Quantity, 
                chart for optimized quantity set for maximum revenue, 
                Optimized value of revenue]
    """

    fig_PriceVsQuantity = px.scatter(
        df, x="Price", y="Quantity", color="Year", trendline="ols")

    # fit OLS model
    model = ols("Price ~ Quantity ", data=df).fit()

    Quantity = list(range(var_range[0], var_range[1], 10))
    cost = int(var_cost)
    Price = []
    Revenue = []
    for i in Quantity:
        demand = model.params[0] + (model.params[1] * i)
        Price.append(demand)
        Revenue.append((i) * (demand - cost))

    # create data frame of price and revenue
    profit = pd.DataFrame(
        {"Price": Price, "Quantity": Quantity, "Revenue": Revenue})

    max_val = profit.loc[(profit['Revenue'] == profit['Revenue'].max())]
    

    fig_QuantityVsRevenue = go.Figure()
    fig_QuantityVsRevenue.add_trace(go.Scatter(
        x=profit['Quantity'], y=profit['Revenue']))
    fig_QuantityVsRevenue.add_annotation(x=int(max_val['Quantity']), y=int(max_val['Revenue']),
                                         text="Maximum Revenue",
                                         showarrow=True,
                                         arrowhead=1)

    fig_QuantityVsRevenue.update_layout(
        showlegend=False,
        xaxis_title="Quantity",
        yaxis_title="Revenue")

    fig_QuantityVsRevenue.add_vline(x=int(max_val['Quantity']), line_width=2, line_dash="dash",
                                    line_color="red", opacity=0.25)

    return [profit, fig_QuantityVsRevenue, fig_PriceVsQuantity, round(max_val['Quantity'].values[0],2), round(max_val['Revenue'].values[0],3)]
