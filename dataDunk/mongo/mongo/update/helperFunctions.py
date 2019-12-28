from nba_api.stats.endpoints import boxscoretraditionalv2
from pymongo import MongoClient
from datetime import datetime, timedelta
import requests
from lxml.html import fromstring


def gameIds():
	# returns date, home_id, and away_id for today's game
	cluster = MongoClient("mongodb+srv://chase:thatredguy7@cluster0-rrnjh.mongodb.net/test?retryWrites=true&w=majority")
	seasonGames = cluster['nba_data']["19-20_Season"]
	day = datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%Y')
	return seasonGames.find({"game_date": day})


def getTable(table):
	# returns a mongodb table
	cluster = MongoClient("mongodb+srv://chase:thatredguy7@cluster0-rrnjh.mongodb.net/test?retryWrites=true&w=majority")
	return cluster['nba_data'][table]


def tableIds(table):
	# returns a list of the game ids in a table
	ids = []
	previousGames = table.find({})
	
	for game in previousGames:
		ids.append(game["_id"])
	
	return ids

def checkUpdate():
	# return true if its 1:00am
	now = datetime.now()
	hour = now.strftime("%H")
	if (int(hour) == 1):
		return True
	
	return False

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies