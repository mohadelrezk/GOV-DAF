from Policy import Policy
from Policy_LDA_topic_modeling import Gensim
from CitizenSatisfactionAnalysis import Correlation_cell, CitizenSatisfactionAnalysis
from MongoTasks import MongoTasks
import mongo_config
import json
import pprint
import copy
from SentimentAnalysis import SentimentAnalysis

#policySpace=""

policy_db_name ="policy_test"
policy_collection_name ="policy_test"
tweets_db_name = "test_policy"
tweets_collection_name = "policy_analysis2"

"""step#1:Data Acquisition / Collection"""

global policy
policy = Policy()

pfd_path = "/Users/mohade/GoogleDrive/__MYPERSONALBACKUP/TEMP-WAITING-ORGANIZATION/3-workspace/GOV-DAF/inputs/policies/1.pdf"
#/home/mohade/workspace/masters-jupyter/masters_code/inputs/policies/1.pdf

policy.extraction(pfd_path)

#print policySpace

"""step#2:Push extracted policy text to mongo """
global mongo
mongo = MongoTasks()

collection = mongo.connect(mongo_config.host, mongo_config.port, policy_db_name, policy_collection_name+"_extracted")
mongo.appendDataToMongo(collection, policy.getAsJson())
print ("Public Policy Information Extracted form .pdf to json, and pushed to mogodb Succefully!")

"""step#3:Data Cleaning"""

policy.cleaning()

print policy.policy_cleaned_as_list_by_lines_or_pages


"""step#4:Push extracted and cleaned policy text to mongo """

collection = mongo.connect(mongo_config.host, mongo_config.port, policy_db_name, policy_collection_name+"_extracted_cleaned")
mongo.appendDataToMongo(collection, policy.getAsJson())
print ("Public Policy Cleaned and pushed to mogodb Succefully!")


"""step#5:Topic Modelig Gensim"""

global gensim
gensim = Gensim()

policy.policy_topic_terms = gensim.LDA_topics(policy.policy_name, policy.policy_cleaned_as_list_by_lines_or_pages,2)


for z in policy.policy_topic_terms:
    print z

#to csv
#gensim.policy_topic_to_csv(policySpace,"outputs/topicPERpolicy_" )

"""step#6:push topic(policy) = terms(policy) to mongo"""

collection = mongo.connect(mongo_config.host, mongo_config.port, policy_db_name, policy_collection_name+"_extracted_cleaned_topicmodeled")
mongo.appendDataToMongo(collection, policy.getAsJson())

print ("Public Policy Topics detected and pushed to mogodb Succefully!")

"""step#7:Correlation Matrix Building"""

global correlation_cell
correlation_cell = Correlation_cell()

correlationsMatrix = correlation_cell.build_correlation_matrix(policy.policy_topic_terms)
print correlationsMatrix

#.correlation_matrix_to_csv("outputs/matrix_", correlationsMatrix)

"""step#7:Push Matrix to Mongo"""
collection = mongo.connect(mongo_config.host, mongo_config.port, policy_db_name, policy_collection_name+"_correlationMatrix")
for cell in correlationsMatrix:
    mongo.appendDataToMongo(collection, cell.getAsJson())

print ("Public Policy co-occurances matrix constructed and pushed to mogodb Succefully!")

"""step#8:query tweets dataset by correlation matrix"""
tweet_collection= mongo.connect(mongo_config.host, mongo_config.port,tweets_db_name,tweets_collection_name)

temp_list = []
for cell in correlationsMatrix:
    cursur = mongo.run_command_search(tweet_collection, "$text",cell.get_related_tweets_query())
    print cell.term_A +" /co/ "+cell.term_B
    if cursur.count()>0:
        for r in cursur["results"]:
            #print json.dumps(r, indent=4, sort_keys=True)
            temp_list.append(copy.deepcopy(r["obj"]["id"]))
            #
            print r["obj"]["id"]
            #pprint.pprint(
        cell.related_tweets_ids = copy.deepcopy(temp_list)
        del temp_list [:]

"""step#9:Push Matrix to Mongo with related_tweets_ids"""
collection = mongo.connect(mongo_config.host, mongo_config.port, policy_db_name, policy_collection_name+"_correlationMatrix_with_tweets")
for cell in correlationsMatrix:
    mongo.appendDataToMongo(collection, cell.getAsJson())

print ("Public Policy related tweets collected and pushed to mogodb Succefully!")

"""step#10:Calculate sentiments"""
global sentiment_analysis
sentiment_analysis = SentimentAnalysis()
sentiment_analysis.activate_nuig_sentiment_deep_learining_run_only_once()
tweet_text = ""
tweets_collection = mongo.connect(mongo_config.host, mongo_config.port, tweets_db_name, tweets_collection_name)


for cell in correlationsMatrix:
    #print ""
    #getting tweet text
    for tweet_id in cell.related_tweets_ids:
        tweet_cursor = mongo.get_tweet_text(tweets_collection,tweet_id)
        print tweet_cursor
        tweet_text = tweet_cursor["text"]
        #passing tweet text to sentiment service
        sentiment_result = sentiment_analysis.analyze_Tweet(tweet_text, "deep_learning")
        sentiment_label = sentiment_result["entries"][0]["sentiments"][0]["marl:hasPolarity"]
        #saving sentiment analysis result in cell.neg/pos/nutral
        print sentiment_label
        if sentiment_label == "positive":
            cell.positive_tweets_ids.append(copy.deepcopy(tweet_id))
        if sentiment_label == "negative":
            cell.negative_tweets_ids.append(copy.deepcopy(tweet_id))
        if sentiment_label == "neutral":
            cell.neutral_tweets_ids.append(copy.deepcopy(tweet_id))

"""step#11:Push Matrix to Mongo with sentiments"""
collection = mongo.connect(mongo_config.host, mongo_config.port, policy_db_name, policy_collection_name+"_correlationMatrix_with_sentiments")
for cell in correlationsMatrix:
    mongo.appendDataToMongo(collection, cell.getAsJson())

print ("Public Policy tweets sentiments calculated and pushed to mogodb Succefully!")

"""step#12:Satisfaction index calculation"""

global citizendatisfactionanalysis
citizendatisfactionanalysis = CitizenSatisfactionAnalysis()

citizendatisfactionanalysis.calculate_predict_satisfaction(correlationsMatrix)
#print correlationsMatrix_Csatisfaction_calc


"""step#13:Push Matrix to Mongo with sentiments and calculated satisfaction index"""
collection = mongo.connect(mongo_config.host, mongo_config.port, policy_db_name, policy_collection_name+"_correlationMatrix_sentiment_satisfaction")
for cell in citizendatisfactionanalysis.matrix_prediction_ready:
    mongo.appendDataToMongo(collection, cell.getAsJson())


"""step#14:prediction fuction model building"""

"""step#15:prediction fuction model testing"""

"""step#16:system evaluation"""








