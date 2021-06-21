import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import regex as re
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


st.title('Simple Streamlit App')

st.markdown("""
This app performs Word Cloud
* **Python libraries:** streamlit, pandas, BeautifulSoup, wordcloud ......
* **Need to cantact: ** [SeaportAI.com](https://seaportai.com/contact-us/).
""")

st.set_option('deprecation.showPyplotGlobalUse', False)
#file_bytes = st.file_uploader("Upload a file", type="csv")

#if file_bytes is not None:
st.sidebar.header("Select Link")
links = ["https://seaportai.com/blog-predictive-maintenance/",
        "https://seaportai.com/2019/04/22/healthcare-analytics/",
        "https://seaportai.com/blog-rpameetsai/",
        "https://seaportai.com/covid-19/",
        "https://seaportai.com/industry4-0/"]
URL = st.sidebar.selectbox('Link', links)
st.sidebar.header("Select No.of words you want to display")
words = st.sidebar.selectbox("No.of Words", range(10,1000,10))
if URL is not None:
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('div', attrs = {'id':'main-content'})
    text = table.text
    cleaned_text = re.sub('\t', "", text)
    cleaned_texts = re.split('\n', cleaned_text)
    cleaned_textss = "".join(cleaned_texts)
    #st.write(cleaned_textss)
    st.write("Word Cloud Plot")
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(background_color="white", max_words=words,
                          stopwords=stopwords).generate(cleaned_textss)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot()



