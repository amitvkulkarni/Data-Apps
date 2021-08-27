import dash
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
# pd.options.display.float_format = '${:,.2f}'.format


app = dash.Dash(__name__)

server = app.server

app.layout = layout.layout_all


@app.callback(
    [
        Output("id_total_customer", 'children'),
        Output("id_total_transactions", 'children'),
        Output("id_total_sales", 'children'),
        Output("id_order_value", 'children'), 
        # Output("id_churn", 'children'), 
        Output("id-results", 'data'), 
        Output("fig-UnitPriceVsQuantity", 'figure'),
        Output("fig-ProductPie", 'figure'), 
    ],
    [
        Input("id-country-dropdown", "value")
    ]
)
def update_output_All(country_selected):

    try:
        if (country_selected != 'All' and country_selected != None):
            df_selectedCountry = pp.filtered_data.loc[pp.filtered_data['Country'] == country_selected]
            df_selectedCountry_p = pp.filtered_data_group.loc[pp.filtered_data_group['Country'] == country_selected]

            cnt_transactions = df_selectedCountry.Country.shape[0]
            cnt_customers = len(df_selectedCountry.CustomerID.unique())
            cnt_sales = round(df_selectedCountry.groupby('Country').agg({'TotalPurchase':'sum'})['TotalPurchase'].sum(),2)
            
            cnt_avgsales = round(df_selectedCountry_p.groupby('Country').agg({'avg_order_value': 'mean'})['avg_order_value'].mean())

            
            repeat_rate = round(df_selectedCountry_p[df_selectedCountry_p.num_transactions > 1].shape[0]/df_selectedCountry_p.shape[0],2)
            churn_rate = round(1-repeat_rate,2)
            

            # scatter plot for purchase trend
            df2 = pp.df_plot.loc[pp.df_plot['Country'] == country_selected]
            fig_UnitPriceVsQuantity_country = px.scatter(df2[:25000], x="UnitPrice", y="TotalPurchase", color = 'Quantity', 
                    size='Quantity',  size_max=20, log_y= True, log_x= True, title= "PURCHASE TRENDS FOR SELECTED COUNTRY")
            
            # Pie chart listing top products
            df_plot_bar = df_selectedCountry.groupby('Description').agg({'TotalPurchase':'sum'}).sort_values(by = 'TotalPurchase', ascending=False).reset_index().head(5)
            df_plot_bar['percent'] = round((df_plot_bar['TotalPurchase'] / df_plot_bar['TotalPurchase'].sum()) * 100,2)

            fir_plotbar = px.bar(df_plot_bar, y='percent', x='Description', title='Top selling products', 
                    text='percent', color='percent')
            fir_plotbar.update_traces(texttemplate='%{text:.2s}', textposition='inside')
            fir_plotbar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',showlegend=False)                
            
            return [cnt_customers, cnt_transactions, cnt_sales, cnt_avgsales,  df_selectedCountry_p.drop(['num_days','num_units'], axis = 1).to_dict('records'),
                    fig_UnitPriceVsQuantity_country, fir_plotbar]

        else:
            
            cnt_transactions = pp.filtered_data.shape[0]
            cnt_customers = len(pp.filtered_data.CustomerID.unique())
            cnt_sales = round(pp.filtered_data.groupby('Country').agg({'TotalPurchase':'sum'})['TotalPurchase'].sum(),2)
            cnt_avgsales = round(pp.filtered_data_group.groupby('Country').agg({'avg_order_value': 'mean'})['avg_order_value'].mean())


            repeat_rate = round(pp.filtered_data_group[pp.filtered_data_group.num_transactions > 1].shape[0]/pp.filtered_data_group.shape[0],2)
            churn_rate = round(1-repeat_rate,2)

            # Bar chart listing top products
            df_plot_bar = pp.filtered_data.groupby('Description').agg({'TotalPurchase':'sum'}).sort_values(by = 'TotalPurchase', ascending=False).reset_index().head(5)
            df_plot_bar['percent'] = round((df_plot_bar['TotalPurchase'] / df_plot_bar['TotalPurchase'].sum()) * 100,2).apply(lambda x : "{:,}".format(x))

            fir_plotbar = px.bar(df_plot_bar, y='percent', x='Description', title='TOP SELLING PRODUCTS', text='percent', color='percent',)
            fir_plotbar.update_traces(texttemplate='%{text:.2s}', textposition='inside')
            fir_plotbar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', showlegend=False)
            
            return [cnt_customers, cnt_transactions, cnt_sales,cnt_avgsales,  pp.filtered_data_group.drop(['num_days','num_units'], axis = 1).to_dict('records'),
                    pp.fig_UnitPriceVsQuantity, fir_plotbar]

    
    
    except Exception as e:
        logging.exception('Something went wrong with interaction logic:', e)




if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, dev_tools_ui=False)
