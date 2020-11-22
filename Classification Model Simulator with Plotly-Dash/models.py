import lightgbm as lgb
import logging
import pandas as pd
import numpy as np
import plotly.express as px
from defintion import *
from sklearn import tree
import plotly.figure_factory as ff
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier
from sklearn.metrics import roc_curve, roc_auc_score, recall_score, precision_score,accuracy_score

logging.basicConfig(filename= 'model_specific.log',  level = logging.DEBUG,format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s')

def buildModel(target, independent, slider, bestModel):

    """[This function builds a classification model with relavant metrics/plots to measure the performance of the model. The model to be built passed as argument from getModel method ]

    Returns:
        [type]: [Returns various metrics such as accuracy, precision, recall for chosen model along with plots]
    """

    try:
        X = pd.DataFrame(independent)
        y = pd.DataFrame(target)

        X = X.drop(['Loan_ID'], axis=1)
        trainX, testX, trainy, testy = train_test_split(X, y, train_size= slider/100, random_state=2)        
        
        if bestModel == 'GNB':
            model = GaussianNB()
        elif bestModel == 'LGBM':
            model = lgb.LGBMClassifier()
        elif bestModel == 'Logistic':
            model = LogisticRegression()
        elif bestModel == 'KNN':
            model = KNeighborsClassifier()
        elif bestModel == 'Raondom Forest':
            model = RandomForestClassifier()
        elif bestModel == 'DT':
            model = tree.DecisionTreeClassifier()
        else:
            model = AdaBoostClassifier()
        
        model.fit(trainX, trainy)
        
        lr_probs = model.predict_proba(testX)
        yhat = model.predict(testX)
        
        
        lr_probs = lr_probs[:, 1]
        #ns_fpr, ns_tpr, _ = roc_curve(testy, ns_probs)
        lr_fpr, lr_tpr, thresholds = roc_curve(testy, lr_probs)     
        
        lr_auc = round(roc_auc_score(testy, lr_probs),2)
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
        accuracy = round(accuracy_score(testy, yhat)*100,1)
        

        logging.debug(accuracy)
        logging.debug(precision)
        logging.debug(recall)
        logging.debug(lr_auc)
                
        return fig_ROC, fig_precision, fig_threshold, precision, recall, accuracy, trainX.shape[0], testX.shape[0],lr_auc
    
    except:
        logging.exception('Something went wrong with AUC curve and Precision/Recall plot')
        
