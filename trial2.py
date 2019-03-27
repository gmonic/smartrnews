import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
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

analyser = SentimentIntensityAnalyzer()

public_tweets=api.search('Theresa May')

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))

for tweet in public_tweets:
   sentiment_analyzer_scores(tweet)

