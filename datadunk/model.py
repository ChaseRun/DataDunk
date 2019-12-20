import datetime
import requests
from pymongo import MongoClient



def gamesToday():
	# returns a dictionary of date, home_id, and away_id for today's game
	seasonGames = db["19-20_Season"]
	dt = datetime.datetime.today()
	day = str(dt.month) + "-" + str(dt.day) + "-" + str(dt.year)
	
	return seasonGames.find({"game_date": day})


def getTable(table):
	# returns a mongodb table
	cluster = MongoClient('mongodb+srv://chase:thatredguy7@cluster0-rrnjh.mongodb.net/test?retryWrites=true&w=majority')
	return cluster['nba_data'][table]


def tableIds(table):
	# returns a list of the game ids in a table
	ids = []
	previousGames = table.find({})
	
	for game in previousGames:
		ids.append(game["_id"])
	
	return ids