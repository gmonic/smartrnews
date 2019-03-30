import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import pandas as pd


# set up twitter API
app = Flask("Twitter")

consumer_key = "XL5IFsytTIGvj5wMLj8C0XGBD"
consumer_secret = "USGzGWlCrOSBUTLZtByqrs4mxuJVyASyMgh1Yp3ENPh64DrTSA"
access_token = "1062100134253727745-0Jcw1uQQUDuP1kWPwVzpDmJtGa3VNR"
access_token_secret = "zLSC546FFCexMgUaYgUR5QVqCFn1sZaYxT3gG0LKn5kKc"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# create analyser objecct
analyzer = SentimentIntensityAnalyzer()

# create function to sentiment analyse sentence
def sentiment_analyzer_scores(sentence):
    score = analyzer.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))


# create 'Theresay May' tweet list
public_tweets=api.search('Theresa May')

tweet_text = []
for tweet in public_tweets:
    tweet = tweet._json
    tweet_text.append(tweet["text"])

score = [(tweet, analyzer.polarity_scores(tweet)["compound"]) for tweet in tweet_text]

# print output
for i in range(0,3):
    print("{:-<65} : {} \n".format(score[i][0], str(score[i][1])))



# print output
# for tweet in tweet_text:
#     print(tweet)



#   sentiment_analyzer_scores(tweet)

