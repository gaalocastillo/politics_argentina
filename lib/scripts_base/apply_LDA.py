import sys
sys.path.append('/home/Documentos/GitHub/politics_argentina/lib/scripts_base')
import os
import re
from FileWorker import *
from TweetParser import *
from TopicModeling import *
from pymongo import *
from datetime import datetime


import time
import pytz
from email.utils import parsedate_tz, mktime_tz
from TextManager import *

num_topics = 3
client = MongoClient('localhost', 27017)
db = client['twitter_db']
worker = FileWorker()


def apply_LDA(corpus,fileName,num_topics):
#	topics = [5, 6, 7, 8, 9, 10, 11, 12]
#	evaluator = TopicModelingEvaluator(corpus,topics)
#	evaluator.show_perplexity()

	lda = TopicModelingLDA(corpus,'term_score')
	lda.fit(num_topics,1000)
	dic_top_words = lda.get_highest_scores(10)
	
	data = {}
	data['results'] = dic_top_words
	data['score_criteria'] = 'term_score'
 	data['num_topics'] = num_topics
 	print data
	#worker.writeJSON(fileName + ".json",data)#guarda el resultado en .json
	
	top_words = lda.get_all_words()
	#if top_words:
	#	top_words = set(top_words)
	#	worker.write(fileName + ".txt",top_words)

	return top_words

def get_corpus_month(tweets):
	data = {}
	docs = []
	for tweet in tweets:
		if 'created_at' in tweet:
			if tweet['created_at'][-4:].strip() == '2017' and (not isRetweet(tweet)):
				timestamp = mktime_tz(parsedate_tz(tweet['created_at']))
				dt = datetime.fromtimestamp(timestamp, pytz.timezone('US/Central'))
				month = dt.month
				text = tweet["text"]
				if month in data:
					data[month] += text + ' '
				else:
					data[month] = text + ' '
	for month in data:
		doc = data[month]
		docs.append(doc)

	print 'Numero de documentos: ' + str(len(docs))
	return docs

def get_corpus_user(tweets):
	data = {}
	docs = []
	for tweet in tweets:
		if not isRetweet(tweet):
			text = tweet['text']
			user_id = tweet['user']['id']
			if user_id in data:
				data[user_id] += text + ' '
			else:
				data[user_id] = text + ' '
	for user_id in data:
		doc = data[user_id]
		docs.append(doc)

	print 'Numero de documentos: ' + str(len(docs))
	return docs

def get_corpus_chronologically(tweets, n, tz='US/Central'):
	dates = []
	docs = []
	for tweet in tweets:
		timestamp = mktime_tz(parsedate_tz(tweet['created_at']))
		dt = datetime.fromtimestamp(timestamp, pytz.timezone('America/Argentina/Buenos_Aires'))
		dates.append(dt)
	dates.sort()
	ordered_tweets = []
	tweets_count = 0
	doc = ''
	for date in dates1:
		for tweet in tweets:
			timestamp = mktime_tz(parsedate_tz(tweet['created_at']))
			dt = datetime.fromtimestamp(timestamp, pytz.timezone(tz))
			if dt == date:
				tweets_count += 1
				doc += tweet['text'] + ' '
				break
		if tweets_count == n:
			docs.append(doc)
			doc = ''
			n = 0
	print 'Numero de documentos: ' + str(len(docs))
	return docs

def get_corpus_by_month_weekday(tweets):
	docs = []


def build_political_dictionary():
	collection_oficialismo = db['lideres_oficialismo']
	collection_justicialista = db['lideres_justicialista']
	collection_renovador = db['lideres_renovador']
	collection_izquierda = db['lideres_izquierda']
	startdate = datetime(2017, 1 , 1 , 0, 0, 0)
	enddate = datetime(2017, 10 , 21 , 0, 0, 0)
	topics = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]


#	tweets_justicialista = collection_justicialista.find({'created_at_date': {'$lt' : enddate , '$gte': startdate } })
	tweets_justicialista = collection_justicialista.find()[:]
#	tweets_oficialismo = collection_oficialismo.find({'created_at_date': {'$lt' : enddate , '$gte': startdate } })
	tweets_oficialismo = collection_oficialismo.find()[:]
#	tweets_renovador = collection_renovador.find({'created_at_date': {'$lt' : enddate , '$gte': startdate } })
	tweets_renovador = collection_renovador.find()[:]	
#	tweets_izquierda = collection_izquierda.find({'created_at_date': {'$lt' : enddate , '$gte': startdate } })
	tweets_izquierda = collection_izquierda.find()[:]

	corpus_justicialista = get_corpus_month(tweets_justicialista)
	corpus_oficialismo = get_corpus_month(tweets_oficialismo)
#	corpus_renovador = get_corpus(tweets_renovador)
	corpus_izquierda = get_corpus_month(tweets_izquierda)





	words_justicialista = apply_LDA(corpus_justicialista,"topics_justicialista",num_topics)
	justicialista =  set(words_justicialista)
	worker.write("diccionario_politico_justicialista.txt",justicialista)
	
 #	words_oficialismo = apply_LDA(corpus_oficialismo,"topics_oficialismo",num_topics)
#	oficialismo = set(words_oficialismo)
 #	worker.write("diccionario_politico_oficialismo.txt",oficialismo)

# 	words_renovador = apply_LDA(corpus_renovador,"topics_oficialismo",num_topics)
# 	renovador = set(words_renovador)
# 	worker.write("diccionario_politico_renovador.txt",renovador)

# 	words_izquierda = apply_LDA(corpus_izquierda,"topics_izquierda",num_topics)
 #	izquierda = set(words_izquierda)
 #	worker.write("diccionario_politico_izquierda.txt",izquierda)

# 	dictionary = oficialismo.union(justicialista)
# 	dictionary = dictionary.union(renovador)
# 	dictionary = dictionary.union(izquierda)
	
# 	print dictionary
# 	worker.write("diccionario_politico.txt",dictionary)

build_political_dictionary()




#corpus_oposicion = [ " ".join(tweet["tokens"]) for tweet in tweets_oposicion if not(re.search("RT",tweet['text']))]
"""
num_topics = [5,10,20,30,40,50,60,70,80,90,100]
evaluator = TopicModelingEvaluator(corpus_oposicion,num_topics)
evaluator.show_perplexity()
"""



