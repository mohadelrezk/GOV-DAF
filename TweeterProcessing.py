
import tweeter_config
import tweepy
from MongoTasks import MongoTasks
import mongo_config
import json

class TwitterProcessing:

    global mongo
    mongo = MongoTasks()



    def get_auth(self):
        print "read from config file!"

        auth = tweepy.OAuthHandler(tweeter_config.consumer_key, tweeter_config.consumer_secret)
        auth.set_access_token(tweeter_config.access_token, tweeter_config.access_token_secret)
        return auth

    def connect_twitter_api_search(self, auth):
        print "connect"
        api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
        return api

    def connect_twitter_stream(self, auth):
        l = tweepy.StdOutListener()
        stream = tweepy.Stream(auth, l)
        stream.filter(languages=["en"], track=["a", "the", "i", "you", "u"])  # etc
        return stream

    def get_tweet(self,api,keywords):
        print "get tweets"
        public_tweets = api.search(keywords)
        #for tweet in public_tweets:
            #print tweet.text
        return public_tweets

    def put_in_mongo(self, tweets):
        print "put in mongo"



    def run(self, dbName,collectionName):

        auth = self.get_auth()
        api = self.connect_twitter_api_search(auth)
        tweets = self.get_tweet(api, "policy")
        collection = mongo.connect(mongo_config.host, mongo_config.port,dbName,collectionName)
        print json.dumps(tweets, indent=4, sort_keys=True)
        for tweet in tweets["statuses"]:
            #print tweet
            #t = json.loads(tweet)
            if tweet["lang"] == "en":
                mongo.appendDataToMongo(collection, tweet)
         #   print tweet

x = TwitterProcessing()
x.run("test_policy","policy_analysis2")

