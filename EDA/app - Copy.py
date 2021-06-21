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


data = pd.read_csv("Vet Buddy Sales.csv")

obj = []
int_float = []
for i in data.columns:
    clas = data[i].dtypes
    if clas == 'object':
        obj.append(i)
    else:
        int_float.append(i)

#print(obj)
#print(int_float)

#############################################   1. Correlation   ##########################################################
        
##############  Finding correlation between numeric variables
print("Select any two variables from below list")
print(int_float)
cor_num_var1 = input("Variable1: ")
cor_num_var2 = input("Variable2: ")

fig = px.scatter(data, x=cor_num_var1, y=cor_num_var2)
print(fig)

##############  Finding correlation between Categorical variables
print("Select any two variables from below list")
print(obj)
cor_obj_var1 = input("Variable1: ")
cor_obj_var2 = input("Variable2: ")

CrosstabResult=pd.crosstab(index=data[cor_obj_var1],columns=data[cor_obj_var2])
stacked = CrosstabResult.stack().reset_index().rename(columns={0:'value'})
columns = stacked.columns
fig1 = px.bar(stacked, x=columns[0], y=columns[2], color=columns[1], barmode='group', height=400)
fig1


#########################################  2. Handling Null Values (Relacing null values with mean and mode)  ###############################

##### Finding no.of values by each column
lis = []
for i in data.columns:
    dd = sum(pd.isnull(data[i]))
    lis.append(dd)
Print("No.of null values before replacing")
print(lis)
for i in data.columns:
    clas = data[i].dtypes
    if clas == 'object':
        data[i].fillna(data[i].mode()[0], inplace=True)
    else:
        data[i].fillna(data[i].mean(), inplace=True)
                


########################################  3. Different types of Variable transformation  ##############################

#####  Note: Before tranforming data we should replace null values with mean and mode (or) remove null values. if data contains null values while transforming we will get an erro

##########  3.A Standard Scalar  Transformation
int_data = data[int_float]
scaler = StandardScaler()
scaler.fit(int_data)
StandardScalar_trans = scaler.transform(int_data)
StandardScalar_trans = pd.DataFrame(StandardScalar_trans)
StandardScalar_trans.columns = int_float
print(StandardScalar_trans.head())

#########  3.B Min-Max Scale Transfromation
scaler = MinMaxScaler()
scaler.fit(int_data)
MinMax_trans = scaler.transform(int_data)
MinMax_trans = pd.DataFrame(MinMax_trans)
MinMax_trans.columns = int_float
print(MinMax_trans.head())

########  3.C Logarthmic Transformation
log_trans = np.log(int_data)
log_trans = pd.DataFrame(log_trans)
log_trans.columns = int_float
print(log_trans.head())



####################################################  4. Outlier detection using box plot   ############################################

#######################  4.A box plot for single numeric variable
print("Select Variable names from below list")
print(int_float)
box_int_var1 = input("Variable1: ")
fig3 = px.box(data, y=box_int_var1)

#######################  4.B box plot for single two variables (Combination of numeric and categorical)
print("Select numeric Variable name from below list")
print(int_float)
box_int_var2 = input("Variable1: ")
print("Select Categorical Variable name from below list")
print(obj)
box_obg_var1 = input("Variable2: ")
fig4 = px.box(data, y=box_int_var2, x = box_obg_var1)



###############################################   5. Multicollinearity  ###############################################

#####  Note: Before Checking multicollinearity data we should replace null values with mean and mode (or) remove null values. if data contains null values we will get an erro

#####  Applying Label encoder for coverting categorical variables to numeric

le = preprocessing.LabelEncoder()
data1 = data.copy()
for i in data1.columns:
    cls = data1[i].dtypes
    if cls == 'object':
        data1[i] = data1[[i]].astype(str).apply(le.fit_transform)
    else:
        data1[i] = data1[i]


def calc_vif(X):
    vif = pd.DataFrame()
    vif["variables"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return(vif)

MultiColinearity_Table = calc_vif(data1)
