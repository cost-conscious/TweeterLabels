import streamlit as st
import pandas as pd
from PIL import Image
import string
import joblib
import streamlit.components.v1 as components
import requests
import json
# from sentence_transformers import SentenceTransformer

# title 
title = '<p style="color:white; font-size: 50px;"><strong>Twitter Disaster Prediction</strong></p>'
st.markdown(title, unsafe_allow_html=True)

# twitter icon
image = Image.open('TwitterIcon.png')
st.image(image)

# description
description = '<p style="color:white; font-size: 30px;">In order to predict whether the tweet is a real disaster or not, please paste the tweet or the URL of the tweet below</p>'
st.markdown(description, unsafe_allow_html=True)

# get css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")


# get user input

def theTweet(tweet_url):
    api = "https://publish.twitter.com/oembed?url={}".format(tweet_url)
    response = requests.get(api)
    res = response.json()["html"]
    return res

tweet = st.text_input("", "Insert tweet here...")
button_clicked = st.button("OK")


# TODO: process user input

# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# def encode(text):
#     emb = model.encode(text, convert_to_tensor=True).tolist()
#     return emb

# TODO: get prediction

# model = joblib.load('model.pkl')
# prediction = model.predict(input_tweet)

if button_clicked:
    # TODO: if (prediction[0]==1):
    #     st.write("We predict that this tweet is about a **real** disaster")
    # else:
    #     st.write("We predict that is tweet is **not** about a real disaster")

    if tweet[:8] == "https://": # if user input is a url, display the tweet
        res = theTweet(tweet)
        components.html(res,height= 300)
        
    st.write("We predict that this tweet is about a **real** disaster")