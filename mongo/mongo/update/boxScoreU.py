"""
Update boxScoreUsage collection

Chase Austin
"""
from nba_api.stats.endpoints import boxscoreusagev2
from pymongo import MongoClient
import requests
import time
import datetime
from update.helperFunctions import *
from itertools import cycle
import pdb

def updateBoxScoreUsage(day):

	boxScoreUsageTable = getTable("boxScoreUsage")
	newGames = gameIds(day)

	period = [0, 1, 2, 3, 4, 5]

	count = 1
	proxy = ""
	
	print("Getting BoxScore Usage...")
	for game in newGames:

		#proxies = get_proxies()
		#proxyPool = cycle(proxies)

		#firstProxy = list(proxies)[0]
		
		periodArr = []
		for p in period:
			periodArr.append({})

		submit = {
			"_id": game["_id"],
			"home_team": game["home_team_id"],
			"away_team": game["away_team_id"],
			"date": game["game_date"],
			"period": periodArr
		}	

		p = 0
		#proxyCount = 0
		while p < len(period):

			#if proxyCount >= len(proxies):
			#	proxies = get_proxies()
			#	proxyPool = cycle(proxies)
			#	print("Generated new proxy list")
			#	proxyCount = 0

			#proxy = next(proxyPool)
			#proxyCount = proxyCount + 1

			try:
				data = boxscoreusagev2.BoxScoreUsageV2(end_period=p, 
																	end_range="0", 
																	game_id=str(game["_id"]), 
																	range_type="0", 
																	start_period="1", 
																	start_range=p,
																	timeout=15)

			except:
				print("Proxy failed: " + str(proxy))					
				time.sleep(1)
			
			else:
				#print("Proxy worked: " + str(proxy))

				stats = []

				stats.append(data.sql_players_usage.get_dict())

				homePlayers = []
				awayPlayers = []
				heads = stats[0]["headers"]
				for person in stats[0]["data"]:
					if person[1] == game["home_team_id"]:
						homePlayers.append(dict(zip(heads, person)))
					
					else:
						awayPlayers.append(dict(zip(heads, person)))


				submit["period"][p]["homeTeamPlayerStats"] = homePlayers
				submit["period"][p]["awayTeamPlayerStats"] = awayPlayers

				p = p + 1

		boxScoreUsageTable.insert_one(submit)
		print (count)
		count = count + 1