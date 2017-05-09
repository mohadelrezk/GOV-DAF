import copy
import itertools

class CitizenSatisfactionAnalysis:

    #global correlation_cell
    #correlation_cell = Correlation_cell()

    matrix_prediction_ready = []


    def getAsJson(self):
        jsonresponde = {}

        # jsonresponde["_id"] = self.DatasetId.encode('hex')
        # jsonresponde["_id"] = self.DatasetId
        #jsonresponde["DatasetId"] = self.DatasetId
        jsonresponde["matrix_prediction_ready"] = self.matrix_prediction_ready

        return jsonresponde

    def clear(self):

        del self.matrix_prediction_ready [:]



    def calculate_predict(self, matrix_analysis_ready):
            print """not coded yet dummy code"""

    def calculate_predict_satisfaction(self, matrix_analysis_ready):

            for cell in matrix_analysis_ready:
                cell.calculate_satisfaction_at_coocorance_cell_level()
                self.matrix_prediction_ready.append(copy.deepcopy(cell))
                cell.clear()
            #self.matrix_prediction_ready







class Correlation_cell:
    #correlation_cell = {}
    #row = {}
    term_A = ""
    term_B = ""
    related_tweets_ids = []
    positive_tweets_ids = []
    negative_tweets_ids = []
    neutral_tweets_ids = []

    total_positive = 0
    total_negative = 0
    total_neutral = 0
    total_reactions = 0
    satisfaction_index = 0.0

    def getAsJson(self):
        jsonresponde = {}

        # jsonresponde["_id"] = self.DatasetId.encode('hex')
        # jsonresponde["_id"] = self.DatasetId
        #jsonresponde["DatasetId"] = self.DatasetId
        jsonresponde["term_A"] = self.term_A
        jsonresponde["term_B"] = self.term_B
        jsonresponde["related_tweets_ids"] = self.related_tweets_ids
        jsonresponde["positive_tweets_ids"] = self.positive_tweets_ids
        jsonresponde["negative_tweets_ids"] = self.negative_tweets_ids
        jsonresponde["neutral_tweets_ids"] = self.neutral_tweets_ids

        jsonresponde["total_positive"] = self.total_positive
        jsonresponde["total_negative"] = self.total_negative
        jsonresponde["total_neutral"] = self.total_neutral
        jsonresponde["total_reactions"] = self.total_reactions
        jsonresponde["satisfaction_index"] = self.satisfaction_index



        return jsonresponde

    def clear(self):

        self.term_A = ""
        self.term_B = ""

        del self.related_tweets_ids [:]
        del self.positive_tweets_ids[:]
        del self.negative_tweets_ids[:]
        del self.neutral_tweets_ids[:]

        self.total_positive = 0
        self.total_negative = 0
        self.total_neutral = 0
        self.total_reactions = 0
        self.satisfaction_index = 0.0

    def build_correlation_matrix(self, policy_topic_terms):
        #print policySpace_LDA

        correlation_matrix = []

        #correlation_cell = {}
        #row = {}
        #related_tweets_ids = []
        #positive_tweets_ids = []
        #negative_tweets_ids = []
        #neutral_tweets_ids = []


        for topic in policy_topic_terms:
            terms = []
            for bi in topic["topic_terms"]:
                terms.append(bi["term"])
        #uniqes
        uniqe_terms = set(terms)

        #nchoosek
        Choose2ForTerms= self.nchoosek(uniqe_terms)

        for bi in Choose2ForTerms:
            self.term_A = bi[0]
            self.term_B = bi[1]
            #correlation_cell["terms"] = copy.deepcopy(row)
            #row.clear()
            correlation_matrix.append(copy.deepcopy(self))
            self.clear()



        #print terms
        return correlation_matrix

    def nchoosek(self, uniqe_terms):

        Choose2ForTerms = list(itertools.combinations(uniqe_terms, 2))

        #print Choose2ForTerms
        return Choose2ForTerms

    """
    def correlation_matrix_to_csv(self, folder, correlation_matrix):

        header = ['term_A', 'term_B', 'related_tweets_ids', 'positive_tweets_ids', 'negative_tweets_ids', 'neutral_tweets_ids']
        cell_row = []
        with open(folder + "_matrix" + ".csv", 'w+') as output:
            outputwriter = csv.writer(output, delimiter=',', quotechar='\"')
            # putting the header
            outputwriter.writerow(header)
            row = []
            for r in correlation_matrix:
                row.append(r["terms"]["term_A"])
                row.append(r["terms"]["term_B"])
                row.append(r["related_tweets_ids"])
                row.append(r["positive_tweets_ids"])
                row.append(r["negative_tweets_ids"])
                row.append(r["neutral_tweets_ids"])
                outputwriter.writerow(copy.deepcopy(row))
                del row[:]
    """

    def calculate_satisfaction_at_coocorance_cell_level(self):

            self.total_positive += len(self.positive_tweets_ids)
            self.total_negative += len(self.negative_tweets_ids)
            self.total_neutral += len(self.neutral_tweets_ids)
            self.total_reactions += len(self.related_tweets_ids)
            if self.total_reactions >0:
                self.satisfaction_index = self.total_positive/self.total_reactions


    def get_related_tweets_query(self):
        #building mongo query for related tweets
        #text = "\"" + self.term_A +"\" " +"\""+self.term_B + "\""
        #q= {"search": text}
        q2= "\"policy\" \"l\""

        return q2 #text

