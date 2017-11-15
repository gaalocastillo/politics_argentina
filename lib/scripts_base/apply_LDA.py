import sys
sys.path.append('/home/Documentos/GitHub/politics_argentina/lib/scripts_base')
import os
import re
from FileWorker import *
from TweetParser import *
from TopicModeling import *
from pymongo import *
from datetime import datetime

num_topics = 12
client = MongoClient('localhost', 27017)
db = client['twitter_db']
worker = FileWorker()


def apply_LDA(corpus,fileName,num_topics):
	lda = TopicModelingLDA(corpus,'term_score')
	lda.fit(num_topics,1000)
	dic_top_words = lda.get_highest_scores(10)
	
	data = {}
	data['results'] = dic_top_words
	data['score_criteria'] = 'term_score'
 	data['num_topics'] = num_topics

	#worker.writeJSON(fileName + ".json",data)#guarda el resultado en .json
	
	top_words = lda.get_all_words()
	#if top_words:
	#	top_words = set(top_words)
	#	worker.write(fileName + ".txt",top_words)

	return top_words

def get_corpus(tweets):
	data = {}

	for tweet in tweets:
		created_at_date = tweet['created_at_date'].strftime("%Y-%m-%d")
		if not(created_at_date in data.keys()):
			data[created_at_date] = []
		data[created_at_date].append(tweet)

	docs = []
	fields = ['tokens']
	args = {
		'mentionsFlag':False,
		'hashtagsFlag':True,
		'urlsFlag':False,
		'userFlag':False,
		'coordinatesFlag':False,
		'placeFlag':False
	}

	parser = TweetParser(fields,**args)

	for key in data:
		tweets = data[key]
		doc = ""
		
		for rawTweet in tweets:
			tweet = parser.parse(rawTweet)
			doc = doc + " ".join(tweet["tokens"])

		docs.append(doc)

	return docs

def build_political_dictionary():
	collection_oficialismo = db['lideres_oficialismo']
	collection_justicialista = db['lideres_justicialista']

	startdate = datetime(2017, 1 , 1 , 0, 0, 0)
	enddate = datetime(2017, 10 , 21 , 0, 0, 0)

	tweets_oposicion = collection_oposicion.find({'created_at_date': {'$lt' : enddate , '$gte': startdate } })
	tweets_oficialismo = collection_oficialismo.find({'created_at_date': {'$lt' : enddate , '$gte': startdate } })

	corpus_oposicion = get_corpus(tweets_oposicion)
	corpus_oficialismo = get_corpus(tweets_oficialismo)

	words_oposicion = apply_LDA(corpus_oposicion,"topics_oposicion",num_topics)
	oposicion =  set(words_oposicion)
	worker.write("diccionario_politico_oposicion.txt",oposicion)
	
	words_oficialismo = apply_LDA(corpus_oficialismo,"topics_oficialismo",num_topics)
	oficialismo = set(words_oficialismo)
	worker.write("diccionario_politico_oficialismo.txt",oficialismo)

	dictionary = oficialismo.union(oposicion)
	print dictionary
	worker.write("diccionario_politico.txt",dictionary)

build_political_dictionary()

#corpus_oposicion = [ " ".join(tweet["tokens"]) for tweet in tweets_oposicion if not(re.search("RT",tweet['text']))]
"""
num_topics = [5,10,20,30,40,50,60,70,80,90,100]
evaluator = TopicModelingEvaluator(corpus_oposicion,num_topics)
evaluator.show_perplexity()
"""



