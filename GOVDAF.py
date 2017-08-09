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

