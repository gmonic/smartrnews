# import libraries
from flask import Flask, render_template, request
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tweepy, json
import pandas
import os
from geopy.geocoders import Nominatim
from wtforms import Form, BooleanField, StringField, validators, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

# setup app
app = Flask("MyApp")
csrf = CSRFProtect(app)

#  import access tokens
port = int(os.environ.get("PORT", 5000))
consumer_key = os.environ.get("consumer_key")
consumer_secret = os.environ.get("consumer_secret")
access_token = os.environ.get("acess_token")
access_token_secret = os.environ.get("acess_token_secret")
API_KEY=os.environ.get("API_KEY")
VALIDATION_KEY=os.environ.get("VALIDATION_KEY")
DOMAIN_NAME=os.environ.get("DOMAIN_NAME")
app.config['SECRET_KEY']="fdfoicn"
WTF_CSRF_SECRET_KEY="qazwsxedc"


# setup APIs
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# create analyser objecct
analyzer = SentimentIntensityAnalyzer()

#create form 1 for location entry
class Form1(FlaskForm):
    location = StringField('location')
    submit1 = SubmitField('submit')

#create form 2 for email address entry
class Form2(FlaskForm):
    email = StringField('email')
    submit2 = SubmitField('submit')

# create homepage
@app.route("/", methods=['GET','POST'])
def homepage():
    # create forms
    form1 = Form1()
    form2 = Form2()

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

    # get trends for a country
    def get_trends(id):
        trends_list=[]
        trends = api.trends_place(id=id,tweet_mode="extended") 
        trends_without_hashtags = list(filter(lambda x: not x["name"].startswith("#"), trends[0]["trends"]))
        for trend in trends_without_hashtags:
            trend_name=trend["name"]
            trends_list.append(trend_name)
        return trends_list

    def get_tweets(trends):
        latest_tweet_on_trend_list=[]
        if trends is not None:
            for trend_name in trends:
                search_results = api.search(q=trend_name, count=3, lang="en")
                if search_results is None:
                    search_results = "hello"
                else:
                    search = search_results[0]
                tweet_text = search.text
                print (tweet_text)
                latest_tweet_on_trend_list.append(tweet_text)
            return latest_tweet_on_trend_list

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

    # find longitude of nearest user entered place
    def find_longitude_from_input_name(use_location):
        geolocator = Nominatim(user_agent="my_app")
        location = geolocator.geocode(use_location)
        return location.longitude

    # find latitude of nearest user entered place
    def find_latitude_from_input_name(use_location):
        geolocator = Nominatim(user_agent="my_app")
        location = geolocator.geocode(use_location)
        return location.latitude

    # find address of nearest user entered place
    def find_address_from_input_name(use_location):
        geolocator = Nominatim(user_agent="my_app")
        location = geolocator.geocode(use_location)
        return location.address

    # find nearest trend place using coords
    def find_place_from_coords(lat, long):
        nearest = api.trends_closest(lat, long)
        use_this_id = nearest[0]["woeid"]
        return use_this_id

    # find trends of nearest trend place
    def find_trends_from_woeid(id):
        trends = api.trends_place(id)
        trends_without_hashtags = list(filter(lambda x: not x["name"].startswith("#"), trends[0]["trends"]))
        new_list = []
        for i in range (5):
            name = trends_without_hashtags[i]["name"]
            new_list.append(name)
        return new_list



    # UK section:
    uk_trends_without_hashtags = get_trends(uk_id)
    uk_latest_tweet_on_trend_list = get_tweets(uk_trends_without_hashtags)
    uk_sentiment_list = get_sentiment(uk_latest_tweet_on_trend_list)
    if form1.location.data and form1.validate():
        user_location = form1.location.data
        user_longitude = find_longitude_from_input_name(user_location)
        user_latitude = find_latitude_from_input_name(user_location)
        user_address = find_address_from_input_name(user_location)
        user_woeid = find_place_from_coords(user_latitude, user_longitude)
        user_trends = find_trends_from_woeid(user_woeid)
        top_tweets = get_tweets(user_trends)
        tweet_sentiment = get_sentiment(top_tweets) 
    #return html file
        return render_template("index.html", form1=form1, form2=form2,
                            user_location=user_location, user_address=user_address, user_trends=user_trends, top_tweets=top_tweets, tweet_sentiment=tweet_sentiment,
                            uk_trends_without_hashtags=uk_trends_without_hashtags, uk_latest_tweet_on_trend_list=uk_latest_tweet_on_trend_list, uk_sentiment_list=uk_sentiment_list)
    else:
        return render_template("index.html", form1=form1, form2=form2,
                            uk_trends_without_hashtags=uk_trends_without_hashtags, uk_latest_tweet_on_trend_list=uk_latest_tweet_on_trend_list, uk_sentiment_list=uk_sentiment_list)


# APPENDIX: BITS OF CODE I TRIED AND DIDN'T WANT TO PUT IN THE APP - BUT MAY WANT TO COME BACK TO LATER

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

    # get trend volume
    # def get_volume(trends):
    #     latest_trend_volume_list=[]
    #     for trend in trends:
    #         if trend["tweet_volume"] is None:
    #             volume = "hello"
    #             latest_trend_volume_list.append(volume)
    #         else:
    #             volume = trend["tweet_volume"]
    #             latest_trend_volume_list.append(volume)
    #     return latest_trend_volume_list

    # get latest tweet on each trend for said country


    # Argentina section:
    # argentina_trends_without_hashtags = get_trends(argentina_id)
    # argentina_trend_volume = get_volume(argentina_trends_without_hashtags)
    # argentina_latest_tweet_on_trend_list = get_tweets(argentina_trends_without_hashtags)
    # argentina_sentiment_list = get_sentiment(argentina_latest_tweet_on_trend_list) 


# run app and debug
app.run(host='0.0.0.0', port=port, debug=True)
