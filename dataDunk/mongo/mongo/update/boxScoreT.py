"""
Update boxScoreTraditional collection

Chase Austin
"""
from nba_api.stats.endpoints import boxscoretraditionalv2
from pymongo import MongoClient
import requests
import time
import datetime
from update.helperFunctions import *

def updateBoxScoreTraditional():



	headers = {
	    'Host': 'stats.nba.com',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
	    'Accept': 'application/json, text/plain, */*',
	    'Accept-Language': 'en-US,en;q=0.5',
	    'Referer': 'https://stats.nba.com/',
	    'Accept-Encoding': 'gzip, deflate, br',
	    'Connection': 'keep-alive',
	}


	boxScoreTable = getTable("boxScoreTraditional")
	newGames = gameIds()
	pastGames = boxScoreTable.find({})

	period = [0, 1, 2, 3, 4, 5]

	print("Getting BoxScore Info...")

	for game in newGames:
		if game["_id"] not in pastGames:
			
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

			for p in period:
				
				try:
					data = boxscoretraditionalv2.BoxScoreTraditionalV2(end_period=p, end_range="0", game_id=str(game["_id"]), range_type="0", start_period="1", start_range=p, headers=headers, timeout=50)

					stats = []

					stats.append(data.player_stats.get_dict())
					stats.append(data.team_starter_bench_stats.get_dict())
					stats.append(data.team_stats.get_dict())


					homePlayers = []
					awayPlayers = []
					heads = stats[0]["headers"]
					for person in stats[0]["data"]:
						if person[1] == game["home_team_id"]:
							homePlayers.append(dict(zip(heads, person)))
						
						else:
							awayPlayers.append(dict(zip(heads, person)))


					homeRoster = {}
					awayRoster = {}
					heads = stats[1]["headers"]
					for spot in stats[1]["data"]:
						if int(spot[1]) == game["home_team_id"]:
							if spot[5] == "Starters":
								homeRoster["starters"] = dict(zip(heads, spot))

							else:
								homeRoster["bench"] = dict(zip(heads, spot))

						else:
							if spot[5] == "Starters":
								awayRoster["starters"] = dict(zip(heads, spot))

							else:
								awayRoster["bench"] = dict(zip(heads, spot))

					homeStats = {}
					awayStats = {}
					heads = heds = stats[2]["headers"]
					for val in stats[2]["data"]:
						if val[1] == game["home_team_id"]:
							homeStats = dict(zip(heads, val))
						else:
							awayStats = dict(zip(heads, val))


					submit["period"][p]["homeTeamPlayerStats"] = homePlayers
					submit["period"][p]["awayTeamPlayerStats"] = awayPlayers
					submit["period"][p]["homeTeamStarterBenchStats"] = homeRoster
					submit["period"][p]["awayTeamStarterBenchStats"] = awayRoster
					submit["period"][p]["homeTeamStats"] = homeStats
					submit["period"][p]["awayTeamStats"] = awayStats

				except requests.exceptions.ReadTimeout:
					print("Read Timeout")
					print("Waiting 1 min until retry")
					time.sleep(120)

			boxScoreTable.insert_one(submit)