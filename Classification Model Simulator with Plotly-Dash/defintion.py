import pandas as pd
import numpy as np
import os
import plotly.express as px

class Data:
    def __init__(self):     
            
        self.df_train = pd.read_csv('Classification Model Simulator with Plotly-Dash/Data/Train.csv')
        self.df_test = pd.read_csv('Classification Model Simulator with Plotly-Dash//Data/Test.csv')
        self.df_train_dummies = pd.get_dummies(self.df_train,columns=['Gender','Married','Education','Self_Employed','Property_Area'],drop_first=True)
        self.df_test_dummies = pd.get_dummies(self.df_train,columns=['Gender','Married','Education','Self_Employed','Property_Area'],drop_first=True)
        self.df = pd.read_csv('Classification Model Simulator with Plotly-Dash//Data/Train.csv')


# creating data object
obj_Data = Data()


