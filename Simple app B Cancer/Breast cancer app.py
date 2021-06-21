import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import auc
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_curve
from sklearn import preprocessing


#import base64
#import matplotlib.pyplot as plt
#import seaborn as sns
#import numpy as np
#from fbprophet import Prophet

st.title('Breast Cancer Prediction')

st.markdown("""
This app performs Breast Cancer Prediction
* **Python libraries:** streamlit, pandas, ......
* **Need to cantact: ** [SeaportAI.com](https://seaportai.com/contact-us/).
""")

file_bytes = st.file_uploader("Upload a file", type="csv")
# Web scraping of NBA player stats
#@st.cache

if file_bytes is not None:
    def load_data(path):
        data = pd.read_csv(path)
        data = data.drop("id", axis = 1)
        return data
    playerstats = load_data(file_bytes)
    ###  Cleaning Data
    def cleaning(data):
        le = preprocessing.LabelEncoder()
        data1 = data
        for i in data1.columns:
            cls = data1[i].dtypes
            if cls == 'object':
                data1[i] = data1[[i]].astype(str).apply(le.fit_transform)
            else:
                data1[i] = data1[i]
        return data1
    Cleaned_Data = cleaning(playerstats)

    st.sidebar.header('Select Output Variable')
    Columns_Names = list(playerstats.columns)
    Dependent_Var = st.sidebar.selectbox('Dependent Variables', Columns_Names)

    #st.write(Columns_Names)
    #st.write(Dependent_Var)

    Columns_Names.remove(Dependent_Var)
    st.sidebar.header('Un-Select Variables those are not important for analysis')
    Independent_Var = st.sidebar.multiselect('Independent Variables: ', Columns_Names, Columns_Names)

    X = Cleaned_Data[Independent_Var]  ## Defining X and Y variables
    y = Cleaned_Data[Dependent_Var]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/4, random_state=0)  ### Splitting train and test datasets

    classifier =  RandomForestClassifier()
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    y_predd = ["Not Affected" if i == 1 else "Affected" for i in y_pred]

    cm = confusion_matrix(y_test, y_pred)

    # predict probabilities
    lr_probs_RF = classifier.predict_proba(X_test)
    # keep probabilities for the positive outcome only
    lr_probs_RF = lr_probs_RF[:, 1]

    lr_precision_RF, lr_recall_RF, _ = precision_recall_curve(y_test, lr_probs_RF)
    lr_f1_RF, lr_auc_RF = f1_score(y_test, y_pred), auc(lr_recall_RF, lr_precision_RF)
    # summarize scores
    #return (y_pred, max(lr_probs_RF)

    X_test['Prediction'] = y_predd
    X_test['Actual'] = y_test
    
    st.write('Actual Data Dimension: ' + str(playerstats.shape[0]) + ' rows and ' + str(playerstats.shape[1]) + ' columns.')
    st.dataframe(playerstats)
    st.write('Test Data Dimension: ' + str(X_test.shape[0]) + ' rows and ' + str(X_test.shape[1]) + ' columns.')
    st.dataframe(X_test)
    st.write("confusion matrix: ")
    st.write(cm)
    st.write('Accuracy: ' + str(accuracy_score(y_test, y_pred)))
    st.write('Random Forest: f1=%.3f auc=%.3f' % (lr_f1_RF, lr_auc_RF))
    

