import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
from sklearn.model_selection import StratifiedKFold,KFold,GridSearchCV,GroupKFold,train_test_split,StratifiedShuffleSplit
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import roc_auc_score,accuracy_score ,confusion_matrix, f1_score, precision_score, recall_score
from catboost import CatBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_curve
from sklearn import tree
import lightgbm as lgb
import plotly.express as px


df_train = pd.read_csv('C:/Users/kulkarna4029/OneDrive - ARCADIS/Studies/Python/Plotly_Dash/Clustering_algos/data/Train.csv')
df_test = pd.read_csv('C:/Users/kulkarna4029/OneDrive - ARCADIS/Studies/Python/Plotly_Dash/Clustering_algos/data/Test.csv')
df_train_dummies = pd.get_dummies(df_train,columns=['Gender','Married','Education','Self_Employed','Property_Area'],drop_first=True)
df_test_dummies = pd.get_dummies(df_train,columns=['Gender','Married','Education','Self_Employed','Property_Area'],drop_first=True)



def fun_SKFold_Binary_ClassificationAll(df, target, slider):

    #target = 'Loan_Status'
    X = df_train_dummies.drop(['Loan_Status'], axis=1)
    y = df_train_dummies['Loan_Status']
    X_train, X_validation, y_train, y_validation = train_test_split(X, y, train_size=slider/100, random_state=1234)
    feats = [
            'Dependents', 'ApplicantIncome', 'CoapplicantIncome',
            'LoanAmount', 'Loan_Amount_Term', 'Credit_History',
            'Gender_Male', 'Married_Yes', 'Education_Not Graduate',
            'Self_Employed_Yes', 'Property_Area_Semiurban', 'Property_Area_Urban' 
    ]       

    splits = 2
    levels = df[target].nunique()
    folds =StratifiedKFold(n_splits=splits, random_state=22,shuffle=True)
    oof_preds = np.zeros((len(df_test_dummies), levels))
    #feature_importance_df = pd.DataFrame()
    #feature_importance_df['Feature'] = X_train.columns
    final_preds = []
    random_state = [22,44,66,77,88,99,101]
    counter = 0
    num_model = 7
    

    
    for fold_, (trn_idx, val_idx) in enumerate(folds.split(X_train.values,y_train)):
        #print("Fold {}".format(fold_))
        X_trn,y_trn = X_train[feats].iloc[trn_idx],y_train.iloc[trn_idx]
        X_val,y_val = X_train[feats].iloc[val_idx],y_train.iloc[val_idx]

        def fun_metrics(predictions, y_val):
            print("Confusion Matrix----------------------")
            cm = confusion_matrix(predictions,y_val)
            print(cm)
            #print(type(cm))
            f1Score = f1_score(y_val, predictions, average='weighted')
            print("F1 Score :",f1Score)
            f1Score = None
            precision = precision_score(y_val, predictions)
            print("Precision :", precision)
            recall = recall_score(y_val, predictions)
            print("Recall :", recall)
        

        def fun_metricsPlots(fpr, tpr,model):
            fpr, tpr, _ = roc_curve(y_val, predictions)
            plt.plot(fpr, tpr, linestyle='--', label= model)
            print("AUC :", metrics.auc(fpr, tpr))

        def fun_updateAccuracy(model, predictions):
            global oof_preds
            final_preds.append(accuracy_score(y_pred=predictions,y_true=y_val))
            modelAccuracy = accuracy_score(predictions,y_val)
            print("Model Accuracy: ", modelAccuracy)


        print("Executing lgbm for fold#:", fold_)
        clf = lgb.LGBMClassifier(n_estimators=1000,max_depth=4,random_state=22)
        clf.fit(X_trn,y_trn)
        predictions = clf.predict(X_val)
        fun_metrics(predictions, y_val)
        fpr, tpr, _ = roc_curve(y_val, predictions)
        fun_metricsPlots(fpr, tpr, "LGBM")
        fun_updateAccuracy(clf, predictions)
        print("==========================================")
        oof_preds += clf.predict_proba(df_test_dummies[feats])

        print("Executing rf for fold#:", fold_)
        clf = RandomForestClassifier()
        clf.fit(X_trn,y_trn)
        predictions = clf.predict(X_val)
        fun_metrics(predictions, y_val)     
        fpr, tpr, _ = roc_curve(y_val, predictions)
        fun_metricsPlots(fpr, tpr, "RF")
        fun_updateAccuracy(clf, predictions)
        print("==========================================")
        oof_preds += clf.predict_proba(df_test_dummies[feats])

    
        print("Executing KNN for fold#:", fold_)
        clf = KNeighborsClassifier(n_neighbors=4)
        clf.fit(X_trn,y_trn)
        predictions = clf.predict(X_val)
        fun_metrics(predictions, y_val)
        fpr, tpr, _ = roc_curve(y_val, predictions)
        fun_metricsPlots(fpr, tpr, "KNN")
        fun_updateAccuracy(clf, predictions)
        print("==========================================")
        oof_preds += clf.predict_proba(df_test_dummies[feats])


        print("Executing Gaussian Naive Bayes  for fold#:", fold_)
        clf = GaussianNB()
        clf.fit(X_trn,y_trn)
        predictions = clf.predict(X_val)
        fun_metrics(predictions, y_val)
        fpr, tpr, _ = roc_curve(y_val, predictions)
        fun_metricsPlots(fpr, tpr, "GNB")
        fun_updateAccuracy(clf, predictions)
        print("==========================================")
        oof_preds += clf.predict_proba(df_test_dummies[feats])


        print("Executing Decision Tree Classifier  for fold#:", fold_)
        clf = tree.DecisionTreeClassifier()
        clf.fit(X_trn,y_trn)
        predictions = clf.predict(X_val)
        fun_metrics(predictions, y_val)  
        fpr, tpr, _ = roc_curve(y_val, predictions)
        fun_metricsPlots(fpr, tpr, "DT")
        fun_updateAccuracy(clf, predictions)
        print("==========================================")
        oof_preds += clf.predict_proba(df_test_dummies[feats])
    

        print("Executing AdaBoost classifier for fold#:", fold_)
        clf = AdaBoostClassifier()
        clf.fit(X_trn,y_trn)
        predictions = clf.predict(X_val)
        fun_metrics(predictions, y_val)
        fpr, tpr, _ = roc_curve(y_val, predictions)
        fun_metricsPlots(fpr, tpr,"ADABOOST")
        fun_updateAccuracy(clf, predictions)
        print("==========================================")
        oof_preds += clf.predict_proba(df_test_dummies[feats])

        print("Executing GLM for fold#:", fold_)
        clf = LogisticRegression()
        clf.fit(X_trn,y_trn)
        predictions = clf.predict(X_val)
        fun_metrics(predictions, y_val)
        fpr, tpr, _ = roc_curve(y_val, predictions)
        fun_metricsPlots(fpr, tpr, "GLM")
        fun_updateAccuracy(clf, predictions)
        print("==========================================")
        oof_preds += clf.predict_proba(df_test_dummies[feats])

        final_preds.append(accuracy_score(y_pred=clf.predict(X_val),y_true=y_val))
        oof_preds += clf.predict_proba(df_test_dummies[feats])
                

        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.legend()
        #plt.show()
                
        oof_preds  = oof_preds/splits/num_model
        predictions_sub = [np.argmax(x) for x in oof_preds]
        ############print("Predictions for submission: ", predictions_sub )
        print("##################################")
        print("Average Accuracy :",sum(final_preds)/len(final_preds))
        print("All accuracy: ", final_preds)
        print("##################################")

        c1 = np.transpose(final_preds)
        d1 = np.array_split(c1,len(c1)/splits)
        d2 = pd.DataFrame(d1)

        #modelNames = pd.DataFrame(['CATBOOST','XGBOOST','LGBM','RF','KNN','GNB','DT','ADA','GLM'])
        modelNames = pd.DataFrame(['LGBM','RF','KNN','GNB','DT','ADA','GLM'])
        modelName1 = pd.concat([modelNames, d2], axis = 1)
        modelName1.columns = ['Model Name','Fold1', 'Fold2']
        modelName1['Avg Accuracy'] = modelName1.mean(axis=1)
        modelName1.sort_values(by = 'Avg Accuracy', ascending= False, inplace= True)
        modelName1.reset_index()
        #print(modelName1)
        print('---------------------==================--------------------===========')
        print(modelName1.columns)
    return modelName1



def getModels(target, independent, slider): 

    df_train_dummies1 = df_test_dummies[independent]   
    getModelResults = fun_SKFold_Binary_ClassificationAll(df_train_dummies1, 'Loan_Status', slider)         
    print(df_train_dummies1.columns)
    print(getModelResults)       
    fig_modelPerformance = px.bar(getModelResults, x= 'Avg Accuracy', y ='Model Name', title= 'Model Performance', orientation='h', color= 'Avg Accuracy')
    return fig_modelPerformance
    