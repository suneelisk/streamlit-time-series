import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import seaborn as sns
import base64
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import PowerTransformer
from sklearn import preprocessing
from statsmodels.stats.outliers_influence import variance_inflation_factor


st.title('Simple EDA App')

st.markdown("""
This app performs EDA
* **Python libraries:** streamlit, pandas, ......
* **Need to cantact: ** [SeaportAI.com](https://seaportai.com/contact-us/).
""")


file_bytes = st.file_uploader("Upload a file", type="csv")

if file_bytes is not None:
    data = pd.read_csv(file_bytes)
    obj = []
    int_float = []
    for i in data.columns:
        clas = data[i].dtypes
        if clas == 'object':
            obj.append(i)
        else:
            int_float.append(i)
    st.sidebar.header("Exploratory Data Analysis")
    Topics = ["Correlation", "Handling Null Values", "Variable Transformation", "Outliers Detection", "Multicolinearity"]
    Topicss = st.sidebar.selectbox('Select Topics from Dropdown Menu', Topics)

    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="Cleaned_Data.csv">Download CSV File</a>'
        return href
    
    ##################################  Correlation ################################################################
    
    if Topicss == "Correlation":
        st.sidebar.header("Select Data type for Correlation")
        corr = st.sidebar.selectbox("Select Type of Variable from Dropdown Menu", ["Correlation bw Numerical Variables", "Correlation bw Categorical Variables"])
        if corr == "Correlation bw Numerical Variables":
            st.sidebar.header("Correlation bw Numerical Variables")
            corr1 = st.sidebar.multiselect("Select Variables from Dropdown Menu", int_float)
            if len(corr1) == 2:
                st.markdown("**"+'Correlation between '+str(corr1[0])+'  Vs  '+str(corr1[1])+"**")
                fig = px.scatter(data, x=corr1[0], y=corr1[1])
                st.plotly_chart(fig)
            else:
                st.write("Select Two Variables")
        else:
            st.sidebar.header("Correlation bw Categorical Variables")
            corr1 = st.sidebar.multiselect("Select Variables from Dropdown Menu", obj)
            if len(corr1) == 2:
                st.markdown("**"+'Correlation between '+str(corr1[0])+'  Vs  '+str(corr1[1])+"**")
                CrosstabResult=pd.crosstab(index=data[corr1[0]],columns=data[corr1[1]])
                stacked = CrosstabResult.stack().reset_index().rename(columns={0:'value'})
                columns = stacked.columns
                fig = px.bar(stacked, x=columns[0], y=columns[2], color=columns[1], barmode='group', height=400)
                st.plotly_chart(fig)
            else:
                st.write("Select Two Variables")
                
    ########################################  Replacing Null Values with Mean and mode  ##################################################
                
    elif Topicss == "Handling Null Values":
        ##################   Adding Submit button  sidebar
        with st.form(key='my_form'):
            with st.sidebar:
                st.sidebar.header("To remove Null Values press below button")
                submit_button = st.form_submit_button(label='REMOVE NAS')
                
        ##############   if we click RM NAS button Null values will replace with mean and mode
        if submit_button:
            for i in data.columns:
              clas = data[i].dtypes
              if clas == 'object':
                data[i].fillna(data[i].mode()[0], inplace=True)
              else:
                data[i].fillna(data[i].mean(), inplace=True)

        #############  finding number of null values in each column
        lis = []
        for i in data.columns:
          dd = sum(pd.isnull(data[i]))
          lis.append(dd)

        ##########  if no of nul values are zero it will displat some text else it will display bar plot by each column
        if max(lis) == 0:
            st.markdown("**Total no.of Null Values:**  "+str(sum(lis)))
            st.markdown("**If you want to download cleaned data then click the download button**")
            st.markdown(filedownload(data), unsafe_allow_html=True)
        else:
            st.markdown("**Total no.of Null Values:**  "+str(sum(lis)))
            st.markdown("**Bar plot to know no.of Null values in each column**")
            fig2 = px.bar(x=data.columns, y=lis, labels={'x':"Column Names", 'y':"NA'S"})
            st.plotly_chart(fig2)

    ###########################################   Different types of Variable Transformation  ##############################
    elif Topicss == "Variable Transformation":
        for i in data.columns:
            clas = data[i].dtypes
            if clas == 'object':
                data[i].fillna(data[i].mode()[0], inplace=True)
            else:
                data[i].fillna(data[i].mean(), inplace=True)
        st.sidebar.header("Select Transfromation Methos from Dropdown Menu")
        trans_choices = st.sidebar.selectbox("Select Type of Transformation", ["Standardization", "Min-max scaling", "Logarithmic transformation"])
        int_data = data[int_float]  ######  taking only numeric variables from data
        int_data = int_data.round()   ####  converting [ex: 1.33 to 1 or 345.5465 to 356] float to integer

        #####  Standard scalar transformation
        if trans_choices == "Standardization":
            st.markdown("**Standard scalar transformation**")
            scaler = StandardScaler()
            scaler.fit(int_data)
            StandardScalar_trans = scaler.transform(int_data)
            StandardScalar_trans = pd.DataFrame(StandardScalar_trans)
            StandardScalar_trans.columns = int_float
            st.write(StandardScalar_trans)
            st.markdown(filedownload(StandardScalar_trans), unsafe_allow_html=True)
        #### Min-Max Scaling Transformation
        elif trans_choices == "Min-max scaling":
            st.markdown("**Min-Max Scaling Transformation**")
            scaler = MinMaxScaler()
            scaler.fit(int_data)
            MinMax_trans = scaler.transform(int_data)
            MinMax_trans = pd.DataFrame(MinMax_trans)
            MinMax_trans.columns = int_float
            st.write(MinMax_trans)
            st.markdown(filedownload(MinMax_trans), unsafe_allow_html=True)
        #### Logarithmic transformation
        elif trans_choices == "Logarithmic transformation":
            st.markdown("**Standard scalar transformation**")
            log_trans = np.log(int_data)
            log_trans = pd.DataFrame(log_trans)
            log_trans.columns = int_float
            st.write(log_trans)
            st.markdown(filedownload(log_trans), unsafe_allow_html=True)
        #### Box-Cox transformation
        #elif trans_choices == "Box-Cox transformation":
            #st.markdown("**Box-Cox transformation**")
            #scaler = PowerTransformer(method='box-cox')
            #scaler.fit(int_data)
            #BoxCox_trans = scaler.transform(int_data)
            #BoxCox_trans = pd.DataFrame(BoxCox_trans)
            #BoxCox_trans.columns = int_float
            #st.write(BoxCox_trans)
            #st.markdown(filedownload(BoxCox_trans), unsafe_allow_html=True)

    ##########################################  Outliers Detection  ######################################
    elif Topicss == "Outliers Detection":
        st.sidebar.header("Select Type of Box Plot")
        boxplot_type = st.sidebar.selectbox("Select Type", ["Single Variable", "Multi Variable"])

        ########################  Box plot with single variable
        if boxplot_type == "Single Variable":
            st.sidebar.header("Select Variable from the Dropdown Menu")
            box_sing_vars = st.sidebar.selectbox("Select Variable", int_float)
            st.markdown("**"+'Box plot with single variable (Numeric Variable) '+str(box_sing_vars)+"**")
            fig3 = px.box(data, y=box_sing_vars)
            st.plotly_chart(fig3)
        ##############  Box plot with two variables (Numeric and categorical variables)
        else:
            st.sidebar.header("Select Variable from the Dropdown Menu")
            box_mul_intvars = st.sidebar.selectbox("Select Numeical Variable", int_float)
            box_mul_catvars = st.sidebar.selectbox("Select Categorical Variable", obj)
            st.markdown("**"+'Box plot with two variables (Numeric and categorical variables) '+str(box_mul_intvars)+"  and  "+str(box_mul_catvars)+"**")
            fig3 = px.box(data, y=box_mul_intvars, x = box_mul_catvars)
            st.plotly_chart(fig3)


    elif Topicss == "Multicolinearity":
        for i in data.columns:
            clas = data[i].dtypes
            if clas == 'object':
                data[i].fillna(data[i].mode()[0], inplace=True)
            else:
                data[i].fillna(data[i].mean(), inplace=True)
        le = preprocessing.LabelEncoder()
        data1 = data.copy()
        for i in data1.columns:
          cls = data1[i].dtypes
          if cls == 'object':
            data1[i] = data1[[i]].astype(str).apply(le.fit_transform)
          else:
            data1[i] = data1[i]
        def calc_vif(X):
            # Calculating VIF
            vif = pd.DataFrame()
            vif["variables"] = X.columns
            vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
            return(vif)
        #X = data1.iloc[:,:-1]
        MultiColinearity_Table = calc_vif(data1)
        st.write(MultiColinearity_Table)
    
   
    



