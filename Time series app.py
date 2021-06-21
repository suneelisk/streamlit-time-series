import streamlit as st
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import plotly.offline as py


st.title('Simple Streamlit App')

st.markdown("""
This app performs Timeseries Forecast
* **Python libraries:** streamlit, pandas, fbprophet, ......
* **Need to cantact: ** [SeaportAI.com](https://seaportai.com/contact-us/).
""")


file_bytes = st.file_uploader("Upload a file", type="csv")

if file_bytes is not None:
    data = pd.read_csv(file_bytes)
    st.sidebar.header("Select no.of days you want to forecast")
    Numbers = st.sidebar.selectbox('No.of Days', list(range(10, 366)))
    m = Prophet()
    m.fit(data)
    future = m.make_future_dataframe(periods=Numbers)
    forecast = m.predict(future)
    plot1 = m.plot(forecast)
    st.write(plot1)
    



