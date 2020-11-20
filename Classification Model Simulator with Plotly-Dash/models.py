from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score, recall_score, precision_score,accuracy_score
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from defintion import *
import logging

logging.basicConfig(filename= 'model.log',  level = logging.DEBUG,format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s')

def buildModel(target, independent, slider):

    try:
        X = obj_Data.df_train_dummies[independent]
        y = obj_Data.df_train_dummies[target]
        X = X.drop(['Loan_ID','Loan_Status'], axis=1)
        trainX, testX, trainy, testy = train_test_split(X, y, train_size= slider/100, random_state=2)
        
        
        model = LogisticRegression()
        model.fit(trainX, trainy)
        
        lr_probs = model.predict_proba(testX)
        yhat = model.predict(testX)
        # keep probabilities for the positive outcome only
        
        lr_probs = lr_probs[:, 1]
        #ns_fpr, ns_tpr, _ = roc_curve(testy, ns_probs)
        lr_fpr, lr_tpr, thresholds = roc_curve(testy, lr_probs)     
        
        lr_auc = roc_auc_score(testy, lr_probs)
        fig_ROC = px.area(
            x=lr_fpr, y=lr_tpr,
            title=f'ROC Curve (AUC={lr_auc:.4f})',
        
            labels=dict(x='False Positive Rate', y='True Positive Rate')
        
        )
        fig_ROC.add_shape(
            type='line', line=dict(dash='dash'),
            x0=0, x1=1, y0=0, y1=1
        )

        fig_ROC.update_yaxes(scaleanchor="x", scaleratio=1)
        fig_ROC.update_xaxes(constrain='domain')


        fig_precision = px.histogram(
            x = lr_probs, color=testy, nbins=50,
            labels=dict(color='True Labels', x='Score')
        )


        # Evaluating model performance at various thresholds
        df_threshold = pd.DataFrame({
            'False Positive Rate': lr_fpr,
            'True Positive Rate': lr_tpr
        }, index=thresholds)
        df_threshold.index.name = "Thresholds"
        df_threshold.columns.name = "Rate"

        fig_thresh = px.line(
            df_threshold, title='TPR and FPR at every threshold'
            
        )

        fig_thresh.update_yaxes(scaleanchor="x", scaleratio=1)
        fig_threshold = fig_thresh.update_xaxes(range=[0, 1], constrain='domain')

        # precision tp / (tp + fp)
        precision = round(precision_score(testy, yhat),2)
        # recall: tp / (tp + fn)
        recall = round(recall_score(testy, yhat),2)
        accuracy = round(accuracy_score(testy, yhat)*100,2)
        
                
        return fig_ROC, fig_precision, fig_threshold, precision, recall, accuracy, trainX.shape[0], testX.shape[0],lr_auc
    
    except:
        logging.exception('Something went wrong with AUC curve and Precision/Recall plot')
        
