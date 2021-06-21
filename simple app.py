import streamlit as st
import time

def math():
    a = st.number_input('Enter Value a:')
    b = st.number_input('Enter Value b:')
    time.sleep(10)
    st.write('a*b = ', a*b)

math()
