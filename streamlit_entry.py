# import libraries
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px


# import custom libraries
from data_handler import db_execute_fetch
from data_handler import DBConnect

# set the page and title
st.set_page_config(page_title="Twitter data analysis", layout="wide")


def loadData():
    """
    A method to load the data from our data base
    """
    connection = DBConnect(dbName='tweets.db')
    query = "select * from TweetInformation"
    df = db_execute_fetch(connection, query, dbName="tweets.db", rdf=True)
    return df


def selectHashTag():
    df = loadData()
    hashTags = st.multiselect("choose combination of hashtags", list(df['hashtags'].unique()))
    if hashTags:
        df = df[np.isin(df, hashTags).any(axis=1)]
        st.write(df)


def selectLocAndAuth():
    df = loadData()
    location = st.multiselect("choose Location of tweets", list(df['location'].unique()))
    lang = st.multiselect("choose Language of tweets", list(df['language'].unique()))

    if location and not lang:
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    elif lang and not location:
        df = df[np.isin(df, lang).any(axis=1)]
        st.write(df)
    elif lang and location:
        location.extend(lang)
        df = df[np.isin(df, location).any(axis=1)]
        st.write(df)
    else:
        st.write(df)



