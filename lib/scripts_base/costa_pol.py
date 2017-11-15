from FileWorker import FileWorker
import time
from datetime import datetime
import pytz
from email.utils import parsedate_tz, mktime_tz


def get2017(newFilename, lastFilename):
	fileworker = FileWorker()
	data = fileworker.readJSON(lastFilename)
	new_data = {}
	new_data['num_tweets'] = data['num_tweets']
	new_data['tweets'] = []
	tweets = data['tweets']
	new_tweets = new_data['tweets']
	for tweet in tweets:
		if 'created_at' in tweet:
			if tweet['created_at'][-4:].strip() == '2017':
				new_tweets.append(tweet)
	fileworker.writeJSON(newFilename, new_data)

def isRetweet(tweet):
	texto = tweet['text']
	if 'retweeted_status' in tweet or (len(texto) > 4 and texto[:4] == 'RT @'):
		return True
	return False

def getRetweetCount(tweet):
	return tweet['retweet_count']

def getFavoriteCount(tweet):
	return tweet['favorite_count']

def fillWeekHours(user_info):
	for day in user_info['days']:
		for month in range(1,13):
			user_info['days'][day][month] = {}
			for hour in range(24):
				user_info['days'][day][month][hour] = {}
				user_info['days'][day][month][hour]['retweet_count'] = 0
				user_info['days'][day][month][hour]['favorite_count'] = 0

def getUsersWeeklyHourData(users_list):
	fileworker = FileWorker()
	f = open('users_basic_data.csv', 'w')
	f.write('username,retweet_count,favorite_count,month,day,hour\n')
	for username in users_list:
		user_info = { 'days': {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}}}
		user_info['username'] = username
		fillWeekHours(user_info)
		user_data = fileworker.readJSON(username + '.json')
		tweets = user_data['tweets']
		for tweet in tweets:
			timestamp = mktime_tz(parsedate_tz(tweet['created_at']))
			dt = datetime.fromtimestamp(timestamp, pytz.timezone('US/Central'))
			weekday = dt.weekday()
			hour = dt.hour
			month = dt.month
			if not isRetweet(tweet):
				user_info['days'][weekday][month][hour]['retweet_count'] += getRetweetCount(tweet)
				user_info['days'][weekday][month][hour]['favorite_count'] += getFavoriteCount(tweet)
		writeUserWeeklyHourData(user_info, f)
	f.close()

def writeUserWeeklyHourData(user_info, f):
	username = user_info['username']
	for day in user_info['days']:
		for month in user_info['days'][day]:
			for hour in user_info['days'][day][month]:

				retweet_count = user_info['days'][day][month][hour]['retweet_count']
				favorite_count = user_info['days'][day][month][hour]['favorite_count']
				f.write(username + ',' + str(retweet_count) + ',' + str(favorite_count) + ',')
				f.write(str(month) + ',' + str(day) + ',' + str(hour) + '\n')

getUsersWeeklyHourData(['diazfabr'])
#get2017('archivo', 'diazfabr.json')