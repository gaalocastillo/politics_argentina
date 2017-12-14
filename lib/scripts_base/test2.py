import pandas as pd
import seaborn as sns
from pymongo import *
client = MongoClient('localhost', 27017)
db = client['twitter_db']

collection_oficialismo = db['lideres_oficialismo']
collection_justicialista = db['lideres_justicialista']
collection_renovador = db['lideres_renovador']
collection_izquierda = db['lideres_izquierda']



def get_retweets (user, collection):
    result = 0
    tweets = 0
    for tweet in collection:
        if user == tweet["user"]["screen_name"]:
            tweets +=0
            retweets += tweet["retweet_count"]
    return (tweets,result)


#suponiendo qu elos tweets de una coleccion se leen como una coleccion de python
users = set()
def distribucion(collection):
    name = ''
    f = open("data.csv","w")
    f.write("user,retweets,tweets\n")
    for tweet in collection.find()[:]:   
        if name not in users:
            num_tweets = tweet['in_reply_to_screen_name']["statuses_count"] 
            name = tweet["in_reply_to_screen_name"]
            tweets,retweets = get_retweets(name,collection)
            retweets = retweeets/tweets
            users.add(name) - {''}
            f.write("%s,%d,%d\n"%(name,num_tweets,retweets))
            
    f.close()
    df = pd.read_csv("data.csv")
    df.plot.scatter(y="retweets")

distribucion(collection_oficialismo)