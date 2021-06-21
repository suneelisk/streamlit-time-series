import streamlit as st
import pandas as pd

st.title('Simple App')
st.header('Basic Operations')
st.subheader('ISK')
st.latex(r'''(a+b)^2=a^2+b^2+2 a b''')
x = st.slider('Select a number: X', 0, 100)
y = st.slider('Select a number: Y', 0, 100)
xy = x+y
st.write('X+Y = ', xy)
st.markdown("<h1 style='text-align: center; color: red;'>Value</h1>", unsafe_allow_html=True)
z = st.number_input("Value z: ")
st.write("Value z*X+Y")
st.write(z*xy)
data = pd.DataFrame({'Name':['A','B','C','D'],'Marks':[30,44,65,77]})
st.write(data)
#st.bar_chart(data)

code = '''print('Hello World')'''

st.code(code, language = 'python')

upload = st.file_uploader('Upload Csv File', type = 'csv')

if upload is not None:
    data1 = pd.read_csv(upload)
    st.dataframe(data1)
