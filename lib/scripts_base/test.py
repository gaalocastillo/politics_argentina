from pymongo import *
from costa_pol import *
from TextManager import *
import pandas as pd
import matplotlib.pyplot as plt


def isRetweet(tweet):
	texto = tweet['text']
	if 'retweeted_status' in tweet or (len(texto) > 4 and texto[:4] == 'RT @'):
		return True
	return False

client = MongoClient('localhost', 27017)
db = client['twitter_db']

collection_oficialismo = db['lideres_oficialismo']
collection_justicialista = db['lideres_justicialista']
collection_renovador = db['lideres_renovador']
collection_izquierda = db['lideres_izquierda']


def writeLeaningsCorpus():
	f = open('oficialismo_documents.txt', 'w')
	for tweet in collection_oficialismo.find()[:]:
		if not isRetweet(tweet):
			f.write(tweet['text'] + '\n')
	f.close()
	f = open('justicialista_documents.txt', 'w')
	for tweet in collection_justicialista.find()[:]:
		if not isRetweet(tweet):
			f.write(tweet['text'] + '\n')
	f.close()
	f = open('renovador_documents.txt', 'w')
	for tweet in collection_renovador.find()[:]:
		if not isRetweet(tweet):
			f.write(tweet['text'] + '\n')
	f.close()



#leanings = ['oficialismo', 'justicialista', 'frente_renovador', 'frente_izquierda']
#classified_users = generate_clasified_lists('../../data/seed_users.csv', leanings)
#politic_leaders_users = classified_users['oficialismo'] + classified_users['justicialista'] + classified_users['frente_renovador']
#getUsersWeeklyHourData(politic_leaders_users)


de = pd.read_csv("users_basic_data.csv")
de["username"] = de["username"].apply(lambda x: x.split(".")[0])

dist = de.groupby(["hour"]).sum()[["retweet_count"]]
dist.plot()
plt.title('Amount of retweets per day hour')
plt.xlabel('Hour')
plt.ylabel('Retweets')
plt.show()
