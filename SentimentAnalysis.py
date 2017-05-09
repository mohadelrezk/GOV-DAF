from NUIGsentiment.SentimentAnalysisDL import SentimentAnalysisDL
import NUIGsentiment.sentimentAPI as sentimentAPI


class SentimentAnalysis:


    def __init__(self):

        global sentimentAnalysisDL
        sentimentAnalysisDL = SentimentAnalysisDL()

    def analyze_Tweet(self, tweet_text, alogrithem):
        sentiment = "null"
        print "nn"
        if alogrithem == "deep_learning":
            sentiment = sentimentAnalysisDL.analyse_gov_daf(tweet_text)

        return sentiment

    def activate_nuig_sentiment_deep_learining_run_only_once(self):
        sentimentAnalysisDL.activate()

"""
x = SentimentAnalysis()
x.activate_nuig_sentiment_deep_learining_run_only_once()


for xx in range (0,10):
    label  = x.analyze_Tweet("@mariakaykay aga tayo tomorrow ah. :) Good night, Ces. Love you!", "deep_learning")
    print label

#print sentimentAPI.classify("@mariakaykay aga tayo tomorrow ah. :) Good night, Ces. Love you!")

"""