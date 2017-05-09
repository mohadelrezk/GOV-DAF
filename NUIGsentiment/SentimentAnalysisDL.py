# coding: utf-8

# In[ ]:



from __future__ import division, print_function
import logging
import numpy as np
import os, codecs, csv, re, nltk
import xml.etree.ElementTree as ET

from senpy.plugins import SenpyPlugin, SentimentPlugin
from senpy.models import Results, Entry, Sentiment

logger = logging.getLogger(__name__)

# _
import math, itertools

from sklearn.feature_extraction.text import CountVectorizer

os.environ['KERAS_BACKEND'] = 'theano'
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.models import load_model

from datetime import datetime


# In[ ]:
"""
class SentimentAnalysisDL(SentimentPlugin):
    def __init__(self, info, *args, **kwargs):
        super(SentimentAnalysisDL, self).__init__(info, *args, **kwargs)
        self.name = info['name']
        self.id = info['module']
        self._info = info
        self.async = info['async']
"""
class SentimentAnalysisDL():
    def __init__(self):

        local_path = os.path.dirname(os.path.abspath(__file__))

        self.Embedding_dir = local_path + "/embeddings/glove.6B.200d.txt"
        self.savedModelPath = local_path + "/savedModels/LSTM_glove200_treedata_model.h5"

        self.max_no_words = 27000000000  # fixed, should be same as the number of words in embeddings
        self.maxlen = 40

    #def activate(self, *args, **kwargs):
    def activate(self):

        np.random.seed(1337)  # for reproducibility

        st = datetime.now()
        self._classifierModel = load_model(self.savedModelPath)
        logger.info("{} {}".format(datetime.now() - st, "loaded _classifierModel"))

        st = datetime.now()
        self._tokenizer = self.get_tokenizer()
        logger.info("{} {}".format(datetime.now() - st, "loaded _tokenizer"))

        # st = datetime.now()
        # nltk.download()
        # self._tokenizer_nltk = nltk.data.load('tokenizers/punkt/english.pickle')
        # logger.info("{} {}".format(datetime.now() - st, "loaded _tokenizer_nltk"))

        logger.info("SentimentAnalysisDL plugin is ready to go!")

    def deactivate(self, *args, **kwargs):
        try:
            logger.info("SentimentAnalysisDL plugin is being deactivated...")
        except Exception:
            print("Exception in logger while reporting deactivation of SentimentAnalysisDL")

    # MY FUNCTIONS
    def cleanTweet(self, tweet):
        tweet = tweet.lower()
        tweet = " " + tweet
        tweet = re.sub(r'[^\x00-\x7F]+', '', tweet)
        tweet = re.sub(' rt ', '', tweet)
        tweet = re.sub('(\.)+', '.', tweet)
        # tweet = re.sub('((www\.[^\s]+)|(https://[^\s]+) | (http://[^\s]+))','URL',tweet)
        tweet = re.sub('((www\.[^\s]+))', '', tweet)
        tweet = re.sub('((http://[^\s]+))', '', tweet)
        tweet = re.sub('((https://[^\s]+))', '', tweet)
        tweet = re.sub('@[^\s]+', '', tweet)
        tweet = re.sub('[\s]+', ' ', tweet)
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        tweet = re.sub('_', '', tweet)
        tweet = re.sub('\$', '', tweet)
        tweet = re.sub('%', '', tweet)
        tweet = re.sub('^', '', tweet)
        tweet = re.sub('&', '', tweet)
        tweet = re.sub('\*', '', tweet)
        tweet = re.sub('\(', '', tweet)
        tweet = re.sub('\)', '', tweet)
        tweet = re.sub('-', '', tweet)
        tweet = re.sub('\+', '', tweet)
        tweet = re.sub('=', '', tweet)
        tweet = re.sub('"', '', tweet)
        tweet = re.sub('~', '', tweet)
        tweet = re.sub('`', '', tweet)
        tweet = re.sub('!', '', tweet)
        tweet = re.sub(':', '', tweet)
        tweet = re.sub('^-?[0-9]+$', '', tweet)
        tweet = tweet.strip('\'"').replace('.', '').strip()
        return tweet

    def pretrainedEmbeddings(self, EmbeddingPath):
        embedding_index = {}
        f = open(EmbeddingPath)
        next(iter(f))
        embedding_wordsList = []
        for line in f:
            values = line.split(" ")
            word = values[0]
            coefs = np.asarray(values[1:])
            embedding_index[word] = coefs
            embedding_wordsList.append(word)
        f.close()
        return (embedding_index, embedding_wordsList)

    def get_tokenizer(self):
        st = datetime.now()
        self._embedding_index, self._embedding_wordsList = self.pretrainedEmbeddings(self.Embedding_dir)
        logger.info("{} {}".format(datetime.now() - st, "loaded WordEmbeddings"))

        # self.max_no_words = len(self._embedding_index.keys())# !? max_no_words already defined above

        tokenizer = Tokenizer(self.max_no_words)
        tokenizer.fit_on_texts(self._embedding_wordsList)
        return tokenizer

    def convert_text_to_vector(self, text, tokenizer):
        # st = datetime.now()
        test_sequences = self._tokenizer.texts_to_sequences(text)
        # logger.info("{} {}".format(datetime.now() - st, "test_sequences"))

        # st = datetime.now()
        X_test = sequence.pad_sequences(test_sequences, maxlen=self.maxlen)
        # logger.info("{} {}".format(datetime.now() - st, "X_test"))
        return X_test

    def classify(self, X_test):
        st = datetime.now()
        y_test_predict = self._classifierModel.predict_classes(X_test)
        logger.info("{} {}".format(datetime.now() - st, "y_test_predict"))

        # print(y_test_predict)
        return y_test_predict

        """
        Utility function to return a list of sentences.
        @param text The text that must be split in to sentences.
        """
        # sentences = self._tokenizer_nltk.tokenize(text)
        # return sentences

    def analyse(self, **params):
        logger.debug("SentimentAnalysisDL Analysing with params {}".format(params))

        text_input = params.get("input", None)

        # st = datetime.now()
        text = self.cleanTweet(text_input)
        # logger.info("{} {}".format(datetime.now() - st, "tweet cleaned"))

        X_test = self.convert_text_to_vector([text], self._tokenizer)
        y_pred = self.classify(X_test)

        response = Results()
        entry = Entry()

        _mapping_labels = {0: 'positive', 1: 'negative', 2: 'neutral'}
        _mapping_values = {0: "1", 1: "-1", 2: "0"}

        for sentence, y_i in zip([text], y_pred):
            sentiment = Sentiment()
            sentiment['marl:hasPolarity'] = _mapping_labels[y_i]
            sentiment["marl:polarityValue"] = _mapping_values[y_i]
            entry.sentiments.append(sentiment)

        entry.nif__isString = text_input
        response.entries.append(entry)

        return response

    def analyse_gov_daf(self, tweet_text):
        logger.debug("SentimentAnalysisDL Analysing with params {}".format(tweet_text))

        text_input = tweet_text#params.get("input", None)

        # st = datetime.now()
        text = self.cleanTweet(text_input)
        # logger.info("{} {}".format(datetime.now() - st, "tweet cleaned"))

        X_test = self.convert_text_to_vector([text], self._tokenizer)
        y_pred = self.classify(X_test)

        #response = Results()
        response_gov_daf = {}
        response_gov_daf["entries"] = []

        #entry = Entry()
        entry_gov_daf={}
        entry_gov_daf["sentiments"]=[]


        _mapping_labels = {0: 'positive', 1: 'negative', 2: 'neutral'}
        _mapping_values = {0: "1", 1: "-1", 2: "0"}

        for sentence, y_i in zip([text], y_pred):
            sentiment = Sentiment()
            sentiment['marl:hasPolarity'] = _mapping_labels[y_i]
            sentiment["marl:polarityValue"] = _mapping_values[y_i]
            entry_gov_daf["sentiments"].append(sentiment)

        entry_gov_daf["nif__isString"] = text_input
        response_gov_daf["entries"].append(entry_gov_daf)

        return response_gov_daf