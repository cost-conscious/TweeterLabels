####
## Import libraries
####

import streamlit as st
import pandas as pd
from PIL import Image
import streamlit.components.v1 as components
import requests
import random
import tweepy
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex

####
## CSS Layout
####

# title 
title = '<p style="color:white; font-size: 50px; text-align: center;"><strong>Twitter Disaster Prediction</strong></p>'
st.markdown(title, unsafe_allow_html=True)


# # twitter icon
my_file = './WebApp/TwitterIcon.png'
image = Image.open(my_file)
st.image(image)

# description
description_1 = '<p style="color:white; font-size: 40px; text-align: center;"><strong>Predict whether a tweet is about a real disaster or not</strong></p>'
st.markdown(description_1, unsafe_allow_html=True)


# prompt
prompt = '<p style="color:white; font-size: 30px; margin-bottom: -40px; text-align: center;">Please paste the tweet or the URL of the tweet below</p>'
st.markdown(prompt, unsafe_allow_html=True)


# load css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("./WebApp/style.css")


# field for tweet URL or text
tweet = st.text_input("", "Insert tweet here...") 


# button for predicting tweet URL or text
button_clicked = st.button("Predict inserted tweet")


# "OR" text
or_text = '<p style="color:white; font-size: 30px; text-align: center;">OR</p>'
st.markdown(or_text, unsafe_allow_html=True)


# button for predicting a random tweet
lucky = st.button("Predict random tweet")

####
## Model Loading & Functions
####

# load model and data required for prediction
embeddings_dim = 384
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
annoy_index = AnnoyIndex(embeddings_dim, 'angular')
annoy_index.load('./Data/annoy_index.ann')
target = pd.read_csv("./Data/train.csv", encoding='utf-8', usecols = ['id', 'target'])


def tweetHTML(tweet_url):
    """
    Retrieves the html of a given twitter url
    """

    api = "https://publish.twitter.com/oembed?url={}".format(tweet_url)
    response = requests.get(api)
    res = response.json()["html"]

    return res


def encode(text):
    """
    Encodes given text
    """
    emb = model.encode(text, convert_to_tensor=True).tolist()

    return emb


def get_prediction(emb_tweet):
    """
    Gets the predicted label (1/0: real disaster/not real disaster) of a given encoded tweet
    """
    label_id = annoy_index.get_nns_by_vector(emb_tweet,n=1,search_k=-1,include_distances=False)
    
    label = target.loc[target['id']==label_id[0], ['target']].values[0][0]
    
    return label


def get_results(prediction):
    """
    Gets the resulting markdown text shown to the user that says whether the tweet is about a real disaster or not
    """
    if prediction == 1:
        results = '<p style="color:red; font-size: 30px; text-align: center; text-shadow: 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black, 0 0 4px black;">We predict that this tweet is about a <strong>real</strong> disaster &#9888;</p>'
    elif prediction == 0:
        results = '<p style="color:white; font-size: 30px; text-align: center; ">We predict that this tweet is <strong>not</strong> about a real disaster</p>'

    return results

####
## Button actions
####

# if "Predict random tweet" button is pressed
if lucky:

    # call api
    client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAHtrjgEAAAAAWTPEH5e5lZQ1mH6NwKZuTV8tGsM%3Dp7s5cERyDIPkUsv2I8HSzeZJgYNhBM1PROBACpJkSEcsjG6QFz')
    
    # get a hashtag from list + tweet must be in English
    disaster_hashtags = ['#evacuation', '#hurricane', '#earthquake', '#bushfire', '#disaster', '#tsunami','#puppy']
    query = random.choice(disaster_hashtags) + " lang:en" 

    # get url of a random tweet among 10 that contain hashtag
    tweets = client.search_recent_tweets(query=query, tweet_fields=['id', 'text'], max_results=10)
    i = random.randrange(0, 10)
    url = 'https://twitter.com/twitter/statuses/' + str(tweets.data[i].id)

    # get html of tweet
    res = tweetHTML(url) 

    # align tweet to center and display
    aligned = res[:32] + ' tw-align-center"' + res[33:] 
    components.html(aligned,height= 300, scrolling=True)

    # get tweet text
    tweet_list = res.split('>')
    tweet_text = tweet_list[2][:-3]

    # encode tweet text
    emb_tweet = encode(tweet_text)

    # get prediction
    prediction = get_prediction(emb_tweet)

    # get correct output
    results = get_results(prediction)

    st.markdown(results, unsafe_allow_html=True)


# if "Predict inserted tweet" button is pressed
if button_clicked:

    # if user input is a url, display the tweet and encode
    if tweet[:8] == "https://": 

        # get html of tweet
        res = tweetHTML(tweet) 

        # align tweet to center
        aligned = res[:32] + ' tw-align-center"' + res[33:]

        # display embedded tweet
        components.html(aligned,height= 300, scrolling=True)

        # get tweet text
        tweet_list = res.split('>')
        tweet = tweet_list[2][:-3]

    # encode tweet text
    emb_tweet = encode(tweet)
    
    # get prediction
    prediction = get_prediction(emb_tweet)

    # get correct output
    results = get_results(prediction)

    # show results
    st.markdown(results, unsafe_allow_html=True)
