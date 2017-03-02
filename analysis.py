
# coding: utf-8

# In[1]:

import pprint
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
# access the database called 'osm'
db = client.myosm
coll = db.kolkata

def total_nodes():
    return coll.find().count()

def no_of_users():
    return len(coll.distinct('create.user'))
     
def node_count():
    return coll.find({"type":"node"}).count()
        
def way_count():
    return coll.find({"type":"way"}).count()

def top_users():
    
    pipeline =[{"$group":{"_id":"$create.user","count":{"$sum":1}}},
                   {"$sort":{"count":-1}},
                      {"$limit":10}]
    
    
    return [doc for doc in coll.aggregate(pipeline)]



if __name__ == '__main__':
    
    no_of_nodes = total_nodes()
    print "Total number of nodes : {}".format(no_of_nodes)
    print '\n'
    
    users = no_of_users()
    print "Total number of unique users : {}".format(users)
    print '\n'
    
    nodes = node_count()
    ways = way_count()
    print "no of nodes :{0} and no of ways :{1}".format(nodes,ways)
    print '\n'
    
    contributers = top_users()
    print "Top 10 contributers are :"
    pprint.pprint(contributers)
    



