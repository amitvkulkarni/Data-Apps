from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.ensemble import RandomForestRegressor
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from defintion import *


def glm(target, independent, slider):

    X = df_dummies[independent]
    y = df_dummies[target]
    X = X.drop(['Loan_ID','Loan_Status'], axis=1)
    trainX, testX, trainy, testy = train_test_split(X, y, train_size= slider/100, random_state=2)
    
    
    model = LogisticRegression()
    model.fit(trainX, trainy)
    
    lr_probs = model.predict_proba(testX)
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
    

    
    # get importance
    # importance = model.coef_[0]
    # fig_Varimp = px.bar([x for x in range(len(importance))], importance, title= "Variable Importance")
        
    return fig_ROC, fig_precision, fig_threshold, '0.5','0.6','0.85', trainX.shape[0], testX.shape[0],lr_auc



def featureImportnace():

    X = df_dummies.drop(['Loan_ID','Loan_Status'], axis=1)
    y = df_dummies['Loan_Status']
    trainX, testX, trainy, testy = train_test_split(X, y, test_size=0.5, random_state=2)
    rf = RandomForestRegressor(n_estimators=100)
    rf.fit(trainX, trainy)
    
    sorted_idx = rf.feature_importances_.argsort()
    fig_featureImp = px.bar(df_dummies.columns[sorted_idx], rf.feature_importances_[sorted_idx],
                    title= 'Variable Importance')
    return fig_featureImp




