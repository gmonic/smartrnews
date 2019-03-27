import tweepy
from textblob import TextBlob
from flask import Flask, render_template, request


app = Flask("Twitter")

with open("credentials.txt", "r") as file:
    consumer_key = file.readline().split()[2]
    consumer_secret = file.readline().split()[2]
    access_token = file.readline().split()[2]
    access_token_secret = file.readline().split()[2]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets=api.search('Theresa May')

for tweet in public_tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
    if analysis.sentiment[0]>0:
        print('Positive')
    elif analysis.sentiment[0]<0:
        print('Negative')
    else:
        print('Neutral')

if not trend["name"].startswith("#"):
    trend = uk_trends[0]["trends"]       
    for i in range(0,5):
        trend_no_hashtag[i] = trend[i]
        
