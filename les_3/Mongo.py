from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['users_db_new']

users = db.users

# users.insert_one({"_id": 23165431684,
#                   "author": "Peter",
#                "age" : 78,
#                "text": "is cool! Wildberry",
#                "tags": ['cool','hot','ice'],
#                "date": '14.06.1983'})

# dicts = [{"author": "John",
#                "age" : 29,
#                "text": "Too bad! Strawberry",
#                "tags": ['ice'],
#                "date": '04.08.1971'},
#
#                     {"author": "Anna",
#                "age" : 36,
#                "title": "Hot Cool!!!",
#                "text": "easy too!",
#                "date": '26.01.1995'},
#
#                    {"author": "Jane",
#                "age" : 43,
#                "title": "Nice book",
#                "text": "Pretty text not long",
#                "date": '08.08.1975',
#                "tags":['fantastic','criminal']}
#       ]


# users.insert_many(dicts)

# pprint(users.find_one({'author':'Peter'}))

# for user in users.find({'author':'Jane','age':43},{'age':1,'author':1,'date':1,'_id':0}):
#      pprint(user)
#
# for user in users.find({'age':{'$gte':30}}):
#      pprint(user)


# for user in users.find({'age':{'$gte':30}}).sort('age',-1).limit(3):
#      pprint(user)


# for user in users.find({'tags.1':'hot'}):
#     pprint(user)

# for user in users.find({'$or':[{'author':'Jane','age':43},{'author':'Anna','age':36}]}):
#       pprint(user)

doc = {"author": "Smith",
               "age" : 16,
               "title": "some Cool!!!",
               "new_field": "some_new_value",
               "date": '23.11.1991'}


# users.update_one({'author':'Smith'},{'$set':doc})
# users.update_many({'author':'Smith'},{'$set':{'age':46}})

# users.replace_one({'author':'Smith'},doc)
# users.replace_many({'author':'Smith'},doc)

# users.delete_one({})
# users.delete_many({})


for user in users.find({}):
      pprint(user)