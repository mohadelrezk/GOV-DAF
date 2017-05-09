from __future__ import print_function
from flask import Flask, jsonify, request
import numpy as np
import os
import codecs
import csv
import re
from keras.preprocessing.text import Tokenizer
import nltk
from sklearn.feature_extraction.text import CountVectorizer
os.environ['KERAS_BACKEND']='theano'
from keras.preprocessing import sequence
from keras.models import load_model
app = Flask(__name__)


# set parameters:
Root_dir = os.path.dirname(os.path.abspath(__file__))
Embedding_dir = Root_dir + "/embeddings/glove.twitter.27B.100d.txt"
savedModelPath = Root_dir + "/savedModels/CNN_twitterSentiment_model.h5"
max_no_words = 27000000000 #fixed, should be same as the number of words in embeddings
maxlen= 40
np.random.seed(1337)  # for reproducibility

# start process_tweet
def cleanTweet(tweet):
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
    tweet = tweet.strip('\'"')
    return tweet
    # end

    p = codecs.open('data/twitterSemEval2013.csv', encoding='latin-1')
    read = csv.reader(p)
    outputFile = open('allNewProcessed.csv', 'w', newline='')
    outputWriter = csv.writer(outputFile)
    for row in read:
        processedTweet = cleanTweet(row[2])
        outputWriter.writerow([processedTweet])

    outputFile.close();
    p.close();


def pretrainedEmbeddings(EmbeddingPath):
	embedding_index = {}
	f = open(EmbeddingPath)
	next(iter(f))
	for line in f:
		values = line.split("\t")
		word = values[0]
		coefs = np.asarray(values[1:])
		embedding_index[word] = coefs
	f.close()
	return embedding_index

def classify(text):

    classifierModel = load_model(savedModelPath)

    embedding_index = pretrainedEmbeddings(Embedding_dir)
    max_no_words = len(embedding_index.keys())
    #vectorizerTrainDocList.append(next(iter(embedding_index.keys())))

    embedding_wordsList = []
    for word in embedding_index.keys():
        embedding_wordsList.append(word)


    tokenizer = Tokenizer(max_no_words)
    tokenizer.fit_on_texts(embedding_wordsList)
    test_sequences = tokenizer.texts_to_sequences([text])

    embeddingwords_index = tokenizer.word_index

    X_test = sequence.pad_sequences(test_sequences, maxlen=maxlen)

    y_test_predict = classifierModel.predict_classes(X_test)

    print(y_test_predict)
    if(y_test_predict==[0]):
            return("positive")
    elif(y_test_predict==[1]):
            return("negative")
    else:
        return("neutral")

# def split_sentences(text):
#     """
#     Utility function to return a list of sentences.
#     @param text The text that must be split in to sentences.
#     """
#     tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
#     sentences = tokenizer.tokenize(text)
#     return sentences

@app.route('/text=<text>', methods = ['GET'])
def run(text):
    tweet = cleanTweet(text)
    label = classify(tweet)

    return label

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
    #classify("@mariakaykay aga tayo tomorrow ah. :) Good night, Ces. Love you!")