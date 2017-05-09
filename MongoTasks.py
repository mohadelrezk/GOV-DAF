
from pymongo import CursorType
from pymongo import MongoClient
from bson import ObjectId
import mongo_config


class MongoTasks:

    def connect(slef,host, port,dbName,collectionName):
        try:
            client = MongoClient(host, port)
            db = client[dbName]
            coll = db[collectionName]
            print "successfuly connected to:" + host +"   "+ str(port)+"   "+  dbName+"   " + collectionName
        except BaseException as exce:
            print str(exce)
            slef.connect(host, port,dbName,collectionName)

        return coll

    def connect_to_db(slef, host, port, dbName):
        try:
            client = MongoClient(host, port)
            db = client[dbName]
            print "successfuly connected to:" + host + "   " + str(port) + "   " + dbName
        except BaseException as exce:
            print str(exce)
            slef.connect_to_db(host, port, dbName)

        return db



    def appendDataToMongo(self, collection, JsonObject):

        # JsonObject_id = collection.insert_one(JsonObject).inserted_id
        try:
            collection.update({'_id': ObjectId()}, JsonObject, True)
        except BaseException as exc:
            print exc
            self.appendDataListToMongo(collection, JsonObject)
            # return JsonObject_id
            # mongo connection and append logic


    def appendDataSetToMongo(self,collection, JsonObject):

        #JsonObject_id = collection.insert_one(JsonObject).inserted_id
        try:
            collection.update({'_id':JsonObject['DatasetId']},JsonObject,True)
        except BaseException as exc:
            print exc
            self.appendDataSetToMongo(collection, JsonObject)
        #return JsonObject_id
        # mongo connection and append logic

    def appendRelationToMongo(self,collection, JsonObject):

        #JsonObject_id = collection.insert_one(JsonObject).inserted_id
        try:
            _id = JsonObject['datasetA'] + str(JsonObject['datasetB'])
            collection.update({'_id': _id}, JsonObject, True)
        except BaseException as exc:
            print exc
            self.appendRelationToMongo(collection, JsonObject)
        #return JsonObject_id
        # mongo connection and append logic

    def appendPublishersRelationToMongo(self,collection, JsonObject):

        #JsonObject_id = collection.insert_one(JsonObject).inserted_id
        try:
            _id = JsonObject['publisherA'] +"--"+ str(JsonObject['publisherB'])
            collection.update({'_id': _id}, JsonObject, True)
        except BaseException as exc:
            print exc
            self.appendRelationToMongo(collection, JsonObject)
        #return JsonObject_id
        # mongo connection and append logic

    def getfromMongo(self,collection, query):

        try:
            if not query:
                cursor = collection.find(no_cursor_timeout=True)
            elif query:
                cursor = collection.find(query, no_cursor_timeout=True)
        except BaseException as exc:
            print exc
            self.getfromMongo(collection, query)


        return cursor

    def getfromMongoFindone(self,collection, query):
        try:
            if not query:
                cursor = collection.find_one(no_cursor_timeout=True)
            elif query:
                cursor = collection.find_one(query, no_cursor_timeout=True)
        except BaseException as exc:
            print exc
            self.getfromMongoFindone(collection, query)

        return cursor

    def getdistinctfromMongo(self, collection, field, query):
        try:
            if not query:
                cursor = collection.distinct(field)
            elif query:
                cursor = collection.distinct(field, query)
        except BaseException as exc:
            print exc
            self.getdistinctfromMongo(collection, field, query)


        return cursor

    def aggregateMongo(self,collection, query):
        try:
            if not query:
                # cursor = collection.aggregate(field,no_cursor_timeout=True)
                cursor = ("aggregate query shall have query param")
            elif query:
                cursor = collection.aggregate(query)
        except BaseException as exc:
            print exc
            self.getfromMongo(collection, query)

        return cursor

    def get_tweet_text(self, collection, tweet_id):

        try:
            if  tweet_id:
                query = {"id":tweet_id}
                cursor = collection.find_one(query, no_cursor_timeout=True)
            elif not tweet_id:
                # cursor = collection.find_one(no_cursor_timeout=True)
                "no text sent!"
        except BaseException as exc:
            print exc
            #self.getfromMongoFindone(collection, query)

        return cursor

    def run_command_search(self, db, command_name, collection_name,query):
        cursor = CursorType
        try:
            if not query:
                print "no command_run query provided!"
            elif query:
                print query
                cursor = db.command(command_name,collection_name,search=query, no_cursor_timeout=True)
                """
                db.command('text', 'collection', search='coffee', filter={'about': {'$regex': 'desserts'}}, limit=2,
                           projection={'comments': 1, '_id': 0})

                The
                first
                parameter is the
                command
                'text', the
                second is the
                name
                of
                the
                collection('collection' in this
                example).
                """
        except BaseException as exc:
            print exc
            #self.getfromMongo(collection, query)

        return cursor
"""
m = MongoTasks()
coll = m.connect(mongo_config.host, mongo_config.port, "test_policy","policy_analysis2")
c = m.get_tweet_text(coll,861278070719885314)
print c
"""