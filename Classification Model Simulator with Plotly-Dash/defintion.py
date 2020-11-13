import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv('C:/Users/kulkarna4029/OneDrive - ARCADIS/Studies/Python/Plotly_Dash/Clustering_algos/data/Train.csv')
df_dummies = pd.get_dummies(df,columns=['Gender','Married','Education','Self_Employed','Property_Area'],drop_first=True)


def corelationMatrix():
        #fig= plt.figure()
        corr_matrix = df.corr()
        fig = px.imshow(corr_matrix, title= "Corelation Matrix")
        return fig
        
def missingVal():
    df_missing = pd.DataFrame(df.isnull().sum())
    df_missing.rename(columns={0:'missing'},inplace=True)
    df_missing.sort_values('missing', ascending= True, inplace = True)
    fig = px.bar(df_missing, orientation= 'h', title= "Missing Values")
    return fig

df_describe = df.describe()
df_describe.reset_index(inplace= True)
df_head = df.head(15)


