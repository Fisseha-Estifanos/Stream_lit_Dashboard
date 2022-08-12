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
    """
    hashtags filter
    """
    print('hashtag run start')
    df = loadData()
    df.drop(columns=['hashtags', 'user_mentions'], axis = 1, inplace = True)
    
    # take the rows from that have values in the hashtag columns
    hashtags_list_df = df["clean_hashtags"].unique()
    hashTags = st.multiselect("choose combination of hashtags", hashtags_list_df)
    if hashTags:
        df = df[np.isin(df, hashTags).any(axis=1)]
        st.write(df)
    print('hashtag run end')


def selectUserMentions():
    """
    User mention filter
    """
    df = loadData()
    df.drop(columns=['hashtags', 'user_mentions'], axis = 1, inplace = True)

    # take the rows from that have values in the user mention columns
    user_mention_list_df = df["clean_mentions"].unique()
    mentions = st.multiselect("choose combination of user mentions", user_mention_list_df)
    if mentions:
        df = df[np.isin(df, mentions).any(axis=1)]
        st.write(df)


def selectSource():
    """
    Source of tweets filter
    """
    df = loadData()
    df.drop(columns=['hashtags', 'user_mentions'], axis = 1, inplace = True)

    # take the rows from that have values in the source columns
    source_list_df = df["source"].unique()
    source = st.multiselect("choose combination of user mentions", source_list_df)
    if source:
        df = df[np.isin(df, source).any(axis=1)]
        st.write(df)


def selectLocAndAuth():
    df = loadData()
    df.drop(columns=['hashtags', 'user_mentions'], axis = 1, inplace = True)

    location = st.multiselect("choose Location of tweets", list(df['place'].unique()))
    lang = st.multiselect("choose Language of tweets", list(df['lang'].unique()))

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


def barChart(data, title, X, Y):
    title = title.title()
    st.title(f'{title} Chart')
    msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                order='ascending')), y=f"{Y}:Q"))
    st.altair_chart(msgChart, use_container_width=True)


def wordCloud():
    df = loadData()
    df.drop(columns=['hashtags', 'user_mentions'], axis = 1, inplace = True)

    cleanText = ''
    for text in df['original_text']:
        tokens = str(text).lower().split()
        #print(f"token: {type(tokens)}")
        for tkn in tokens:
            if (tkn != 'https'):
                cleanText += " ".join(tokens) + " "
                #print(f"clean_text: {type(cleanText)}")


    wc = WordCloud(width=650, height=450, background_color='white', min_font_size=5).generate(cleanText)
    st.title("Tweet Text Word Cloud")
    st.image(wc.to_array())
wordCloud()

def stBarChart():
    df = loadData()
    df.drop(columns=['hashtags', 'user_mentions'], axis = 1, inplace = True)

    dfCount = pd.DataFrame({'Tweet_count': df.groupby(['retweet_count'])['original_text'].count()}).reset_index()
    dfCount["retweet_count"] = dfCount["retweet_count"].astype(str)
    dfCount = dfCount.sort_values("Tweet_count", ascending=False)

    num = st.slider("Select number of Rankings", 0, 50, 5)
    title = f"Top {num} Ranking By Number of tweets"
    barChart(dfCount.head(num), title, "retweet_count", "Tweet_count")


def langPie():
    df = loadData()
    dfLangCount = pd.DataFrame({'Tweet_count': df.groupby(['lang'])['original_text'].count()}).reset_index()
    dfLangCount["language"] = dfLangCount["lang"].astype(str)
    dfLangCount = dfLangCount.sort_values("Tweet_count", ascending=False)
    dfLangCount.loc[dfLangCount['Tweet_count'] < 10, 'lang'] = 'Other languages'
    st.title(" Tweets Language pie chart")
    fig = px.pie(dfLangCount, values='Tweet_count', names='language', width=500, height=350)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    colB1, colB2 = st.columns([2.5, 1])

    with colB1:
        st.plotly_chart(fig)
    with colB2:
        st.write(dfLangCount)


st.title("Twitter Data Analysis")

st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Hash tag filters</p>", unsafe_allow_html=True)
selectHashTag()
st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'></p>", unsafe_allow_html=True)


st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>User mention filters</p>", unsafe_allow_html=True)
selectUserMentions()
st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'></p>", unsafe_allow_html=True)


st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Location and Language filters</p>", unsafe_allow_html=True)
selectLocAndAuth()
st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'></p>", unsafe_allow_html=True)


st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Source filters</p>", unsafe_allow_html=True)
selectSource()
st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'></p>", unsafe_allow_html=True)


st.title("Twitter Data Visualizations")
st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Word Cloud visualizations</p>", unsafe_allow_html=True)
wordCloud()
st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'></p>", unsafe_allow_html=True)


with st.expander("Show More Graphical visualizations"):
    stBarChart()
    langPie()


print('over and out')
