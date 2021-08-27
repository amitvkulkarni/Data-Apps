import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import datetime as dt
import numpy as np
import plotly.express as px
# pd.options.display.float_format = '${:,.2f}'.format



# Load the data
data = pd.read_excel("./data/Online_Retail.xlsx")

# remove duplicate rows
filtered_data = data.drop_duplicates()

filtered_data.columns

# Plot the bar chart of countries
filtered_data.Country.value_counts()[:10].plot(kind='bar')

# Filter all quantities that are greater than zero
filtered_data = filtered_data[(filtered_data['Quantity']>0)]

# list(filtered_data.Country.unique())

filtered_data = filtered_data [['CustomerID','Description','InvoiceDate','InvoiceNo','Quantity','UnitPrice', 'Country']]

# Calculate total purchase
filtered_data['TotalPurchase'] = filtered_data['Quantity'] * filtered_data['UnitPrice']

filtered_data_group = filtered_data.groupby(['CustomerID','Country']).agg({'InvoiceDate': lambda date: (date.max() - date.min()).days,
                                        'InvoiceNo': lambda num: len(num),
                                        'Quantity': lambda quant: quant.sum(),
                                        'TotalPurchase': lambda price: price.sum()})


# Change the name of columns
filtered_data_group.columns=['num_days','num_transactions','num_units','spent_money']

# Average Order Value
filtered_data_group['avg_order_value'] = filtered_data_group['spent_money']/filtered_data_group['num_transactions']

# Calculate purchase frequency
purchase_frequency = sum(filtered_data_group['num_transactions'])/filtered_data_group.shape[0]

# Repeat rate
repeat_rate = round(filtered_data_group[filtered_data_group.num_transactions > 1].shape[0]/filtered_data_group.shape[0],2)

# Churn Percentage
churn_rate = round(1-repeat_rate,2)

filtered_data_group.reset_index()

filtered_data_group['profit_margin'] = filtered_data_group['spent_money']*0.05

# Customer Value
filtered_data_group['CLV'] = (filtered_data_group['avg_order_value']*purchase_frequency)/churn_rate

# Resetting the index
filtered_data_group.reset_index(inplace = True)

# Formatting the currency fields
# filtered_data_group['spent_money', 'avg_order_value','profit_margin'] = filtered_data_group.spent_money.apply(lambda x : "{:,}".format(x))

df_plot = filtered_data.groupby(['Country','Description','UnitPrice','Quantity']).agg({'TotalPurchase': 'sum'},{'Quantity':'sum'}).reset_index()
# df2 = df1.loc[df1['Country'] == 'USA']
# px.scatter(df_plot[:25000], x="UnitPrice", y="TotalPurchase", color = 'Quantity', size='Quantity',  title="Product Sales", size_max=20, log_y= True, log_x= True)
fig_UnitPriceVsQuantity = px.scatter(df_plot[:25000], x="UnitPrice", y="Quantity", color = 'Country', 
        size='TotalPurchase',  size_max=20, log_y= True, log_x= True, title= "PURCHASE TREND ACROSS COUNTRIES")



# formating the float fields
var_float_filtered_group = [i for i in filtered_data_group.columns if filtered_data_group.dtypes[i]=='float64']
for i in var_float_filtered_group:
        filtered_data_group[i] = filtered_data_group[i].round(2)
        filtered_data_group[i].apply(lambda x : "{:,}".format(x))


var_float_filtered = [i for i in filtered_data.columns if filtered_data.dtypes[i]=='float64']
for i in var_float_filtered:
        filtered_data[i] = filtered_data[i].round(2)
        filtered_data[i].apply(lambda x : "{:,}".format(x))





