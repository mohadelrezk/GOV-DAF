
"""
#!/usr/bin/python

import sys, getopt
import pymongo

def main(argv):
   db_name = ''
   collection_name = ''
   field_name = ''
   try:
      opts, args = getopt.getopt(argv,"h:db:col:field:",["db=","col=", "field="])

   except getopt.GetoptError:
      print 'exeption:usage: mongo_text_indexing.py -db <database> -col <collection> -field <field>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'help:usage: mongo_text_indexing.py -db <database> -col <collection> -field <field>'
         sys.exit()
      elif opt in ("-db", "--database"):
         db_name = arg
      elif opt in ("-col", "--collection"):
         collection_name = arg
      elif opt in ("-field", "--field"):
         field_name = arg
   print 'Database is "', db_name
   print 'Collection is "', collection_name
   print 'Field is "', field_name



   client = pymongo.MongoClient()
   db = client[db_name]
   collection = db[collection_name]

   collection.create_index([(field_name, 'text')])

   search_this_string = "stuff"
   print collection.find({"$text": {"$search": search_this_string}}).count()


if __name__ == "__main__":
   main(sys.argv[1:])


"""

#!/usr/bin/python

import sys
import pymongo


db_name = ''
collection_name = ''
field_name = ''
try:
   db_name = sys.argv[1]
   collection_name = sys.argv[2]
   field_name = sys.argv[3]
except Exception as e:
   print 'mongo_text_indexing.py <database> <collection> <field>'
   sys.exit(2)

print 'Database is "', db_name
print 'Collection is "', collection_name
print 'Field is "', field_name



client = pymongo.MongoClient()
db = client[db_name]
collection = db[collection_name]

collection.create_index([(field_name, 'text')])

print collection.find({"$text": {"$search": "a"}}).count()


