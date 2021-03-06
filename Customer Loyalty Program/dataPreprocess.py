import base64
import io
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import pathlib
import logging
import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from RFM import *
import dash_daq as daq
import plotly.figure_factory as ff


# Logging in DEBUG mode in the file RFM.log
logging.basicConfig(filename= 'RFM.log',  level = logging.DEBUG,format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s')


def data_load():

    try:
        # load dataset
        df = pd.read_csv('./data/data.csv', encoding = "ISO-8859-1")# Convert InvoiceDate from object to datetime format
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        df.dropna()
        

        # prepare dataset and create TotalSum column for df dataset
        df['TotalSum'] = df['Quantity'] * df['UnitPrice']# Create snapshot date
        snapshot_date = df['InvoiceDate'].max() + timedelta(days=1)
        #print(snapshot_date)# Grouping by CustomerID
        data_process = df.groupby(['CustomerID']).agg({
                'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
                'InvoiceNo': 'count',
                'TotalSum': 'sum'})# Rename the columns 
        data_process.rename(columns={'InvoiceDate': 'Recency',
                                'InvoiceNo': 'Frequency',
                                'TotalSum': 'MonetaryValue'}, inplace=True)
        


        # --Calculate R and F groups--# Create labels for Recency and Frequency
        r_labels = range(4, 0, -1); f_labels = range(1, 5)# Assign these labels to 4 equal percentile groups 
        r_groups = pd.qcut(data_process['Recency'], q=4, labels=r_labels)# Assign these labels to 4 equal percentile groups 
        f_groups = pd.qcut(data_process['Frequency'], q=4, labels=f_labels)# Create new columns R and F 
        data_process = data_process.assign(R = r_groups.values, F = f_groups.values)
        data_process.head()

        # Create labels for MonetaryValue
        m_labels = range(1, 5)# Assign these labels to three equal percentile groups 
        m_groups = pd.qcut(data_process['MonetaryValue'], q=4, labels=m_labels)# Create new column M
        data_process = data_process.assign(M = m_groups.values)


        # Concat RFM quartile values to create RFM Segments
        def join_rfm(x): return str(x['R']) + str(x['F']) + str(x['M'])
        data_process['RFM_Segment_Concat'] = data_process.apply(join_rfm, axis=1)
        rfm = data_process
        rfm.head()


        # Count num of unique segments
        rfm_count_unique = rfm.groupby('RFM_Segment_Concat')['RFM_Segment_Concat'].nunique()
        #print(rfm_count_unique.sum())


        # Calculate RFM_Score
        rfm['RFM_Score'] = rfm[['R','F','M']].sum(axis=1)
        #print(rfm['RFM_Score'].head())


        # Define rfm_level function
        def rfm_level(df):
            try:
                if df['RFM_Score'] >= 9:
                    return 'Cant Loose Them'
                elif ((df['RFM_Score'] >= 8) and (df['RFM_Score'] < 9)):
                    return 'Champions'
                elif ((df['RFM_Score'] >= 7) and (df['RFM_Score'] < 8)):
                    return 'Loyal'
                elif ((df['RFM_Score'] >= 6) and (df['RFM_Score'] < 7)):
                    return 'Potential'
                elif ((df['RFM_Score'] >= 5) and (df['RFM_Score'] < 6)):
                    return 'Promising'
                elif ((df['RFM_Score'] >= 4) and (df['RFM_Score'] < 5)):
                    return 'Needs Attention'
                else:
                    return 'Require Activation'# Create a new variable RFM_Level
            except:
                logging.exception('Something went wrong with rfm_level segmentation logic')

        rfm['RFM_Level'] = rfm.apply(rfm_level, axis=1)# Print the header with top 5 rows to the console
        rfm.reset_index(inplace=True)


        # Calculate average values for each RFM_Level, and return a size of each segment 
        rfm_level_agg = rfm.groupby('RFM_Level').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'MonetaryValue': 'mean'
            #'Monetary': 'count'
            
        }).round(1)# Print the aggregated dataset

        rfm_level_agg.reset_index(inplace = True)
        #rfm_level_agg.set_index('RFM_Level')

        df_head = df.head(1500)
        df_rfm = rfm

        return [df_head, df_rfm, rfm_level_agg, df]

    except Exception as e:
        logging.exception('Something went wrong with data preprocessing: ', e)
