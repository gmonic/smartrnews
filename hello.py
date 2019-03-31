# import libraries
from flask import Flask, render_template, request
import requests
from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tweepy, json
import pandas
import os

# setup app, import access tokens and setup api
app = Flask("MyApp")
port = int(os.environ.get("PORT", 5000))
consumer_key = os.environ.get("consumer_key")
consumer_secret = os.environ.get("consumer_secret")
access_token = os.environ.get("acess_token")
access_token_secret = os.environ.get("acess_token_secret")
API_KEY=os.environ.get("API_KEY")
VALIDATION_KEY=os.environ.get("VALIDATION_KEY")
DOMAIN_NAME=os.environ.get("DOMAIN_NAME")
newsapi = NewsApiClient(api_key='e5b7520feeb046d2bb39801f4957670e')

# setup twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# create analyser objecct
analyzer = SentimentIntensityAnalyzer()

# create homepage
@app.route("/", methods=['GET', 'POST'])
def homepage():

    # get trends for a country
    def get_trends(id):
        trends = api.trends_place(id=id,tweet_mode="extended") 
        trends_without_hashtags = list(filter(lambda x: not x["name"].startswith("#"), trends[0]["trends"]))
        return trends_without_hashtags

    # get trend volume
    def get_volume(trends):
        latest_trend_volume_list=[]
        for trend in trends:
            if trend["tweet_volume"] is None:
                volume = "hello"
            else:
                volume = trend["tweet_volume"]
            latest_trend_volume_list.append(volume)
        return latest_trend_volume_list

    # get latest tweet on each trend for said country
    def get_tweets(trends):
        latest_tweet_on_trend_list=[]
        if trends is not None:
            for trend in trends:
                trend_name = trend["name"]
                search_results = api.search( q=trend_name, count=3)
                search = search_results[0]
                tweet_text = search.text
                print (tweet_text)
                latest_tweet_on_trend_list.append(tweet_text)
            return latest_tweet_on_trend_list

                # search_results = tweepy.Cursor(api.search, q=trend_name, count=3, tweet_mode="extended").items()
                # for tweet in enumerate(search_results):
                #     tweet_text = tweet[2].full_text

    # get sentiment on latest tweet on trend for said country
    def get_sentiment(tweets):
        sentiment_list=[]
        if tweets is not None:
            for tweet in tweets:
                score = (analyzer.polarity_scores(tweet)["compound"]) 
                if score <-0.05:
                    sentiment_score = "Negative"
                if score >0.05:
                    sentiment_score = "Positive"
                else:
                    sentiment_score = "Neutral"
                sentiment_list.append(sentiment_score)
            return sentiment_list

    # list WOEIDs
    argentina_id = 23424747
    australia_id = 23424748
    brazil_id =  23424768
    canada_id = 23424775
    china_id = 23424971
    germany_id = 23424829
    france_id = 23424819
    india_id = 23424848
    indonesia_id =  23424846
    italy_id = 23424853
    japan_id = 23424856
    mexico_id = 23424900
    russia_id = 23424936
    saudi_Arabia_id = 29125356
    south_Africa_id = 24865670
    south_Korea_id = 23424868
    spain_id = 23424950
    turkey_id = 23424969
    uk_id = 23424975
    us_id = 23424977

    # UK section:
    uk_trends_without_hashtags = get_trends(uk_id)
    uk_trend_volume = get_volume(uk_trends_without_hashtags)
    uk_latest_tweet_on_trend_list = get_tweets(uk_trends_without_hashtags)
    uk_sentiment_list = get_sentiment(uk_latest_tweet_on_trend_list)
   
    # Argentina section:
    # argentina_trends_without_hashtags = get_trends(argentina_id)
    # argentina_trend_volume = get_volume(argentina_trends_without_hashtags)
    # argentina_latest_tweet_on_trend_list = get_tweets(argentina_trends_without_hashtags)
    # argentina_sentiment_list = get_sentiment(argentina_latest_tweet_on_trend_list)   
    
    #return html file
    return render_template("index.html", 
                            uk_trends_without_hashtags=uk_trends_without_hashtags, uk_latest_tweet_on_trend_list=uk_latest_tweet_on_trend_list, uk_trend_volume=uk_trend_volume, uk_sentiment_list=uk_sentiment_list)



#argentina_trends_without_hashtags=argentina_trends_without_hashtags, argentina_latest_tweet_on_trend_list=argentina_latest_tweet_on_trend_list, argentina_sentiment_list=argentina_sentiment_list, argentina_trend_volume=argentina_trend_volume

        # if request.method == 'POST':
        #     email_address = request.form['email_address']
        #     requests.post(
        #         "https://api.mailgun.net/v3/" + DOMAIN_NAME +"/messages",
        #         auth=("api", API_KEY),
        #         data={"from": "Monica <mailgun@" + DOMAIN_NAME + ">",
        #             "to": [email_address],
        #             "subject": "Thanks for subscribing to smartr news!",
        #             "text": "We welcome you to smartr news!"})
        #     return render_template("index.html", trends_without_hashtags=trends_without_hashtags, df=df,  search_results=search_results,search=search, new_list=new_list, length=length) 
        # else:

# run app and debug
app.run(host='0.0.0.0', port=port, debug=True)
