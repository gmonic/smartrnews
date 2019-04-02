import tweepy, json
from flask import Flask, render_template, request
import os
from geopy.geocoders import Nominatim

app = Flask("Twitter")

consumer_key = "XL5IFsytTIGvj5wMLj8C0XGBD"
consumer_secret = "USGzGWlCrOSBUTLZtByqrs4mxuJVyASyMgh1Yp3ENPh64DrTSA"
access_token = "1062100134253727745-0Jcw1uQQUDuP1kWPwVzpDmJtGa3VNR"
access_token_secret = "zLSC546FFCexMgUaYgUR5QVqCFn1sZaYxT3gG0LKn5kKc"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


nearest = api.trends_closest(51.5,-0.1)
use_this_id = nearest[0]["woeid"]
trends = api.trends_place(use_this_id)
trends_without_hashtags = list(filter(lambda x: not x["name"].startswith("#"), trends[0]["trends"]))
new_list = []
for i in range (5):
    name = trends_without_hashtags[i]["name"]
    new_list.append(name)

print(nearest[0]["woeid"])
print(new_list)


geolocator = Nominatim(user_agent="my_app")
location = geolocator.geocode("Sunbury")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)
