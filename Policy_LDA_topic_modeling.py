import logging, gensim, bz2
from gensim import corpora
import copy
import csv

class Gensim:


    # constructor
    def __init__(self):
        # initiate logger object
        #global log
        #log = logee("/log/mastersThesis.log", "GOV-DAF:PolicyAnalytics")

        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    #Define the dataset
    ## load id->word mapping (the dictionary), one of the results of step 2 above

    def LDA_topics(self, policy_name, policySpace_list, num_topics):


        # load id->word mapping (the dictionary), one of the results of step 2 above
        dictionary = corpora.Dictionary(policySpace_list)

        #crrating bag of words for every (policy page) and creating the corpus
        corpus = [dictionary.doc2bow(text) for text in policySpace_list]
        #print corpus

        #Then I define the LDA model.
        # extract 100 LDA topics, using 1 pass and updating once every 1 chunk (10,000 documents)
        lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, update_every=1, chunksize=10000, passes=1)

        #TO DICTIONARY
        topics_list = []
        topic_dic = {}
        keywords_list = []
        keywords_dic = {}

        for i in lda.show_topics():
            # print i[0]
            topic_dic["policy_name"] = policy_name
            topic_dic["topic_id"] = i[0]

            # extracting keywords
            keys = i[1]
            keys_list = keys.split()
            for k in keys_list:
                if k not in "+":
                    new_keys = k.split("*")
                    # loops= len(new_keys)/2
                    # print new_keys

                    # if isinstance(l, basestring):
                    # if "\"" in new_keys(i) :
                    keywords_dic["term"] = str(new_keys[1]).replace("\"","")
                    # if "\"" not in l:
                    keywords_dic["score"] = new_keys[0]
                    keywords_list.append(copy.deepcopy(keywords_dic))

            topic_dic["topic_terms"] = copy.deepcopy(keywords_list)
            topics_list.append(copy.deepcopy(topic_dic))
            keywords_dic.clear()
            topic_dic.clear()
            del keywords_list[:]

        #for z in topics_list:
         #   print z

        return topics_list
        #Then I print the topics:

        #lda.print_topics(5)

    def LDA_topics_onePolicy(self, policySpace_list, no_topics):


        # load id->word mapping (the dictionary), one of the results of step 2 above
        dictionary = corpora.Dictionary(policySpace_list)

        #crrating bag of words for every (policy page) and creating the corpus
        corpus = [dictionary.doc2bow(text) for text in policySpace_list]
        print corpus

        #Then I define the LDA model.
        # extract 100 LDA topics, using 1 pass and updating once every 1 chunk (10,000 documents)
        lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=no_topics, update_every=1, chunksize=10000, passes=1)



        #Then I print the topics:

        #lda.print_topics(5)



    def policy_topic_to_csv(self, policySpace_LDA, folder):

        header = ['policy_name','topic_id', 'keywords', 'score']
        relationrecord_r = []
        with open(folder + "topics_" + "LDA.csv", 'w+') as output:
            outputwriter = csv.writer(output, delimiter=',', quotechar='\"')
            # putting the header
            outputwriter.writerow(header)
            row=[]
            for r in policySpace_LDA:
                #row.append(r["topic_id"])
                for n in r["topic_keywords"]:
                    row.append(r["policy_name"])
                    row.append(r["topic_id"])
                    row.append(n["word"])
                    row.append(n["score"])
                    outputwriter.writerow(copy.deepcopy(row))
                    del row [:]
