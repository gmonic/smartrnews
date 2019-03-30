from flask import Flask, render_template, request
from newsapi import NewsApiClient
import tweepy, json
import pandas
import os


#setup app, import access tokens and setup api
app = Flask("MyApp")
port = int(os.environ.get("PORT", 5000))
consumer_key = os.environ.get("consumer_key")
consumer_secret = os.environ.get("consumer_secret")
access_token = os.environ.get("acess_token")
access_token_secret = os.environ.get("acess_token_secret")
newsapi = NewsApiClient(api_key='e5b7520feeb046d2bb39801f4957670e')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#homepage setup
#find UK trends, remove those with hashtags.
#put trends into dataframe
#find latest bbc news article on the first 5 UK trends with no hashtag (uses bbc news api)
#store bbc headline in dataframe (if no headline returned - this sometimes happens, put 0 in its place)
@app.route("/")
def country_info():
    new_list=[]
    uk_id=23424975
    uk_trends = api.trends_place(id=uk_id) 
    trends_without_hashtags = list(filter(lambda x: not x["name"].startswith("#"), uk_trends[0]["trends"]))
    df = pandas.DataFrame(data=trends_without_hashtags) 
    
    for x in range(0,5):
       trend = trends_without_hashtags[x]
       trend_name = trend["name"]
       search_results=api.search(q=trend_name, count=2)
       search=search_results[0]
       json_str=json.dumps(search._json)
       new_list.append(json_str)
    length = len(new_list)
    #    search_results=api.search(q=trend_name, count=1)
    #    search=search_results[0]
    #    json_str=json.dumps(search._json)
    #    df_new = pandas.DataFrame(data=search_results)

    return render_template("index.html", trends_without_hashtags=trends_without_hashtags, df=df,  search_results=search_results,search=search, new_list=new_list, length=length)

        # all_articles = newsapi.get_everything(q=trend_name, sources='bbc-news', domains='bbc.co.uk', sort_by='relevancy')

# return str(all_articles["articles"][0]["title"])
#       trend_name_g = "from:Reuters "+trend_name
#       search_results = api.search(q=trend_name_g)
#        for i in search_results:


 

#contact page
@app.route("/contact")
def hello_someone():
    return render_template("contact.html")


#subscribe page
@app.route("/subscribe", methods=["POST"])
def sign_up():
    form_data = request.form
    return render_template("result.html", form_data=form_data) 


#testing page
@app.route("/random_page")
def my_first_twitter_app(): 

    tweets_timeline = api.home_timeline(count = 5)
    world_trends = api.trends_available()
    ldn_trends = api.trends_place(id = 44418)
    return render_template("third_page.html", tweets_timeline=tweets_timeline, world_trends=world_trends, ldn_trends=ldn_trends)

app.run(host='0.0.0.0', port=port, debug=True)
