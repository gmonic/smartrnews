import tweepy
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

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print (tweet.text)