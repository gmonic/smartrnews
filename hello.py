from flask import Flask, render_template, request
import tweepy, json
import pandas
import os

app = Flask("MyApp")
port = int(os.environ.get("PORT", 5000))


with open("credentials.txt", "r") as file:
    consumer_key = file.readline().split()[2]
    consumer_secret = file.readline().split()[2]
    access_token = file.readline().split()[2]
    access_token_secret = file.readline().split()[2]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

@app.route("/")
def country_info():
    uk_trends = api.trends_place(id=23424975)

    return render_template("index.html", uk_trends=uk_trends)

@app.route("/contact")
def hello_someone():
    return render_template("hello.html")

@app.route("/subscribe", methods=["POST"])
def sign_up():
    form_data = request.form
    return render_template("result.html", form_data=form_data) 

@app.route("/random_page")
def my_first_twitter_app(): 

    tweets_timeline = api.home_timeline(count = 5)
    world_trends = api.trends_available()
    ldn_trends = api.trends_place(id = 44418)
    return render_template("third_page.html", tweets_timeline=tweets_timeline, world_trends=world_trends, ldn_trends=ldn_trends)

app.run(host='0.0.0.0', port=port, debug=True)