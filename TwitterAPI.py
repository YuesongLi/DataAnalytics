import oauth2 as oauth
import urllib
import simplejson as json
import sqlite3 as lite
import sys
import os
from gexf import Gexf
import time

# Go to https://apps.twitter.com/ to get a new Application, and get the token
# create a Application and get the token we need as follows:
consumer_key='repKTknuB0grIwucOsoFFmEaC'
consumer_secret='np2H4J6L2AoQDSkSF9oTHQgUoYxtljJnl4VydHk2L6xl5k5wud'
access_token_key='3436085711-NvOwD2UaNKDsNudftmxORS6QcpBAdqY4XtC7dLK'
access_token_secret='zwdp5r48g8smJ7JU1txg7OOuxcpsIX5KFA2in1R5qRFGF'
consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
token = oauth.Token(key=access_token_key, secret=access_token_secret)
client = oauth.Client(consumer, token)
# the topic we are querying
q = "Kobe Bryant" 
count="100"		#every time get 100 data
# store information of tweet user information
User=dict()
# store realtionship information of tweet user and tweet user_mention
Edge=dict()
# use user to store the tweet account (both the user and user_mentioned )in each tweet
Month = {"Jan": "01", "Feb": "02", "Mar":"03", "Apr":"04","May":"05", "Jun": "06","Jul":"07", "Aug":"08", "Sep": "09", "Oct":"10", "Nov":"11", "Dec":"12"}
user = []
edge = []
for i in range(1,50):	##To get enough users
	url = """https://api.twitter.com/1.1/search/tweets.json?q=%s&include_entities=true&result_type=recent&count=%s""" % (q,count)
	header, fhand = client.request(url, method="GET")		##get data
	jDoc = json.loads(fhand, encoding='utf8')
	#deal with each tweet in quering result
	for tweet in jDoc['statuses']:
		# time of tweet created
		month=tweet["created_at"].split(" ")[1]
		Time=tweet["created_at"].split(" ")[5]+"-"+Month[month]+"-"+tweet["created_at"].split(" ")[2]+" "+tweet["created_at"].split(" ")[3]
		checkUser = 0
		# use list node to store information of the tweet user, and store the user name and when he created the tweet account
		# the information is in the "user" part
		user.append(tweet["user"]["name"])
		user.append(Time)
		user.append(1)
		# check if the user has already exist in the dictionary Node, use checkUser to check the result, 1 means exist, 0 means not exist
		for key in User:
			if (key == tweet["user"]["id"]):
				checkUser = 1
				# User[key][2]=User[key][2]+1
		# if there is no same tweet account in the dictionary, add the tweet account into User dictionary
		if (checkUser == 0):
			User[tweet["user"]["id"]]=user
		#initialize user and edge
		user = []
		edge=[]
		#get the user mentions information: the user_mentions name and when he created the tweet account
		# there may be many people being @ at one tweet, so the tweet["entities"]["user_mentions"] is a List
		# if there is no @ in the tweet, this for loop will be skipped
		# otherwise, every user being @ will be searched
		for person in tweet["entities"]["user_mentions"]:
				# add the information into user
			user.append(person["name"])
			user.append(Time)
			user.append(1)
		# check if the user mentions has already exist in the dictionary User, use checkUser to check the result, 1 means exist, 0 means not exist
			for key in User:
				if (key == person["id"]):
					checkUser = 1
					User[key][2]=User[key][2]+1
			if (checkUser == 0):
				User[person["id"]] = user
		# collect the times of @ between user and user_mentions and use it as weight to show whether they are strength relation or not
		#use user id + user_mentions id as key of dictionary Link, and user id is int, so we need to transfer from int to string
			EdgeBetween = str(tweet["user"]["id"]) + "->" + str(person["id"])
		 #user checkEdge to judge whether there already exist relation between the two users
			checkEdge = 0
			edge.append(Time)
			edge.append(1)
			for key in Edge:
				if (key == EdgeBetween):
					Edge[key][1]=Edge[key][1]+1
					checkEdge=1
			if(checkEdge==0):
				Edge[EdgeBetween]=edge
			#initialize user, edge
			user = []
			edge=[]
		

print """<?xml version="1.0" encoding="UTF-8"?>\n"""
print """<gexf xmlns="http://www.gexf.net/1.2draft" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd" version="1.2">\n"""
# currentDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))		
currentDate="2015-11-20 16:00:00"
print """\t<meta lastmodifieddate="%s">\n""" % (currentDate)
print """\t\t<creator>Dereck</creator>\n"""
print """\t</meta>\n"""
print """\t<graph mode="dynamic" defaultedgetype="directed" timeformat="dateTime">\n"""

########################################################
############# NODES ####################################
########################################################
print """\t\t<nodes>\n"""

for key in User:
	print """\t\t\t<node id="%s" label="%s" start="%s" end="%s"/>\n""" % (key, User[key][0], User[key][1], currentDate)
	# print """<ns0:size value="%d" />""" %(User[key][2])
print """\t\t</nodes>\n"""	
########################################################
############# EDGES ####################################
########################################################
print """\t\t<edges>\n"""
for key in Edge:
	source = key.split("->")[0]
	target = key.split("->")[1]
	print """\t\t\t<edge source="%s" target="%s" start="%s" end="%s" weight="%d"/>\n""" % (source, target, Edge[key][0],currentDate,Edge[key][1])
print """\t\t</edges>\n"""	

print """\t</graph>\n"""
print """</gexf>\n"""
