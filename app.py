import streamlit as st
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import plotly.offline as py


st.title('Simple Streamlit App')

st.header('Time  Series Analysis')

st.subheader('Prophet Model')

#st.text('Type a number in the box below')

#n = st.number_input(label = 'Number', step=1, value = 1)

#st.write(f'{n} + 1 = {n+1}')

#s = st.text_input('Type a name in the box below')

#st.write(f'Hello {s}')

file_bytes = st.file_uploader("Upload a file", type="csv")

if file_bytes is not None:
    data = pd.read_csv(file_bytes)
    #st.dataframe(data)

    m = Prophet()
    m.fit(data)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    #st.dataframe(forecast.head(5))
    plot1 = m.plot(forecast)
    st.write(plot1)
    #py.init_notebook_mode()

    #fig = plot_plotly(m, forecast)  # This returns a plotly Figure
    #dd = py.iplot(fig)
    #st.write(dd)
    



