
from mLogger import logee
import nltk
from nltk import pos_tag, word_tokenize

# READ pdf TEXT
from pyPdf import PdfFileReader, PdfFileWriter

class Policy:

    policy_name = "policy_space"
    policy_row_text = ""
    #policy_cleaned_text = ""
    policy_cleaned_as_list_by_lines_or_pages=[]
    policy_topic_terms =[]






    #constructor
    def __init__(self):
        # initiate logger object
        global log
        log = logee("mastersThesis.log", "GOV-DAF:PolicyAnalytics")

        #define nltk_data path (contains the corpora/stopwords)
        nltk.data.path.append('/home/mohade/Documents/nltk_data/')

    def getAsJson(self):
        jsonresponde = {}

        # jsonresponde["_id"] = self.DatasetId.encode('hex')
        # jsonresponde["_id"] = self.DatasetId
        #jsonresponde["DatasetId"] = self.DatasetId
        jsonresponde["policy_name"] = self.policy_name
        jsonresponde["policy_row_text"] = self.policy_row_text
        jsonresponde["policy_cleaned_as_list_by_lines_or_pages"] = self.policy_cleaned_as_list_by_lines_or_pages
        jsonresponde["policy_topic_terms"] = self.policy_topic_terms


        return jsonresponde

    def clear(self):

        self.policy_name = ""
        self.policy_row_text = ""
        del self.policy_cleaned_as_list_by_lines_or_pages [:]
        del self.policy_topic_terms [:]



    def get_List(self, policy_space_path):
        print "mm"

    def extraction(self,pdf_path):
        """#Data Acquisition / Collection"""
        pdfOne = PdfFileReader(file(pdf_path, "rb"))

        policySpace_str = ''

        for page in pdfOne.pages:
            #print (page.extractText().lower())

            #get every page in new line
            policySpace_str = policySpace_str + page.extractText().lower()
            policySpace_str = policySpace_str + "\n"
        self.policy_row_text =  policySpace_str


    def cleaning(self):
        """#Data Cleaning"""
        #policySpace_str = ""
        # remove redundunt spaces
        dirty_string = self.policy_row_text.replace("  ", " ")
        dirty_string = dirty_string.replace("  ", " ")
        dirty_string = dirty_string.replace("  ", " ")
        # remove page numbering
        dirty_string = dirty_string.replace("1.", " ")
        dirty_string = dirty_string.replace("2.", " ")
        # policySpace_srt = policySpace_srt.replace("1", " ")
        # policySpace_srt = policySpace_srt.replace("2", " ")

        # remove specials
        # policySpace_str = policySpace_str.replace("\'", "")
        import re
        dirty_string = re.sub('[^a-zA-Z0-9\n\.]', ' ', dirty_string)

        # policySpace_srt = ' '.join([word for word in policySpace_str.split() if word not in (stopwords.words('english'))])
        #print (stopwords.words('english'))
        # print (policySpace_str)


        #convert policyspace to list of strings by pages
        dirty_string_list = dirty_string.splitlines()
        #print dirty_string_list


        # remove stopwords
        from nltk.corpus import stopwords
        dirty_string_list = [[word for word in policypage.lower().split() if word not in stopwords.words('english')] for policypage in dirty_string_list]
        print dirty_string_list

        #filter only words > 1
        self.policy_cleaned_as_list_by_lines_or_pages = [[word for word in policypage if len(word) > 1] for policypage in dirty_string_list]


        #final step
        #policySpace_list= dirty_string_list

        #return dirty_string_list

    def NLTK(self, policySpace_str):

        """#unstructured data analysis (NLP)"""
        # POS tagging

        # testing pos tagger
        policySpace_str_tokenized = word_tokenize(policySpace_str)
        policySpace_str_tokenized_posTagged = nltk.pos_tag(policySpace_str_tokenized)
        print(policySpace_str_tokenized)
        print(policySpace_str_tokenized_posTagged)

        # Limitizing policy space, So I have to provide the word and its part of speech tag
        from nltk.stem.wordnet import WordNetLemmatizer
        lmtzr = WordNetLemmatizer()
        # as limitizer only accepts nouns and verbs, I categorize POS to nouns and verbs
        noun_pos_tags = ('NN', 'NNS', 'NNP', 'NNPS')
        verb_pos_tags = ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ')

        analysis_ready_policy_space_vector = []

        for word in policySpace_str_tokenized_posTagged:
            print (word)
            word_w = str(word[0])
            pos = str(word[1])

            print (word_w)
            print (pos)

            if pos in noun_pos_tags:
                print (lmtzr.lemmatize(word_w, 'n'))

            if pos in verb_pos_tags:
                print (lmtzr.lemmatize(word_w, 'v'))

    def saveToFile(self,file_path, object ):#"outputs/policySpace.txt"
        # Build ploicy Space
        with open(file_path, "w") as text_file:
            text_file.write(object.encode("utf-8"))