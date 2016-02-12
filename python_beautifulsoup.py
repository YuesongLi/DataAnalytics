import os 
import csv
import urllib
import sqlite3 as lite
import re
ratingsList = "http://boxnumbertwo.com/MovieData/ratings.list"
response = urllib.urlopen(ratingsList)
Movie = dict()
Number = dict()
NumberN=dict()
Rate = dict()
originalName=''

for line in response:
	words = re.sub(' +',' ',line.strip()).split(" ",3)
	number=words[1]
	rate=words[2]
	name=words[3].split(" {",1)[0]
	name=name.replace('"','')
	name=name.lower()
	Movie[name]=name
	Rate[name]=rate
	if name==originalName:
		Number[name]=Number[name]+','+number
	else:
		Number[name]=number
	originalName=name
# print count
# for key in sorted(Number.keys()):
# 	print key
# 	print Number[key]
for k,v in Number.iteritems():
	numberS=v.split(',')
	maxNumber=int(numberS[0])
	for item in numberS:
		if int(item)>maxNumber:
			maxNumber=int(item)
	NumberN[k]=maxNumber
# for key in sorted(NumberN.keys()):
# 	print key
# 	print NumberN[key]
directoryForDB = "D:/DBClass/MovieData"
if not os.path.exists(directoryForDB):
	os.makedirs(directoryForDB)

directoryForDB = directoryForDB + "movies.db"
#If database does not exist, creates items
#If database does exist, opens it
con = lite.connect(directoryForDB)
with con:

	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS MovieRate") 
	cur.execute("CREATE TABLE MovieRate(Movie TEXT, MovieRate TEXT, MovieNumber TEXT)")
	for key in Rate:
		insertStatement = """INSERT INTO MovieRate VALUES("%s","%s","%s")"""% (Movie[key],Rate[key],NumberN[key])
		cur.execute(insertStatement)

     
	## NEEDED, if not, database does not update
	# cur.execute('SELECT * FROM MovieBudget')
	# rows = cur.fetchall()
	# for row in rows:
	# 	print row[0],row[1],row[2],row[3],row[4]
	con.commit()


