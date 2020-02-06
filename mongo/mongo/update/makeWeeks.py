import pymongo
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://chase:thatredguy7@cluster0-rrnjh.mongodb.net/test?retryWrites=true&w=majority')
db = cluster['nba_data']
weeks = db["19-20_Weeks"]


i = 0

week = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
start = ["12-24-2019", 
		"12-31-2019", 
		"01-07-2020", 
		"01-14-2020", 
		"01-21-2020", 
		"01-28-2020", 
		"02-04-2020", 
		"02-11-2020", 
		"02-18-2020", 
		"02-25-2020", 
		"03-03-2020", 
		"03-10-2020", 
		"03-17-2020", 
		"03-24-2020", 
		"03-31-2020", 
		"04-07-2020"]

end = ["12-30-2019", 
		"01-6-2020", 
		"01-13-2020", 
		"01-20-2020", 
		"01-27-2020", 
		"01-03-2020", 
		"02-10-2020", 
		"02-17-2020", 
		"02-24-2020", 
		"02-02-2020", 
		"03-09-2020", 
		"03-16-2020", 
		"03-23-2020", 
		"03-30-2020", 
		"03-06-2020", 
		"04-15-2020"]



i = 0

while i < len(week):

	record = {
		"week": week[i],
		"start": start[i],
		"end": end[i]
	}

	i = i + 1

	weeks.insert_one(record)




