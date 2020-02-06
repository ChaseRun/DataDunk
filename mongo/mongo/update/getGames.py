from nba_api.stats.endpoints import playernextngames
import pymongo
from pymongo import MongoClient
import requests

import time

cluster = MongoClient('mongodb+srv://chase:thatredguy7@cluster0-rrnjh.mongodb.net/test?retryWrites=true&w=majority')
db = cluster['nba_data']
season = db["19-20_Season"]

headers = {
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}


players = []
x = db["teamRosters"].find({"season": 2019})

for y in x:
	players.append(y["players"][0]["id"])

i = 1
for person in players:

	print("Generating game" + str(i))

	try:
		data = playernextngames.PlayerNextNGames(number_of_games=200, player_id=person, season_type_all_star="Regular Season", league_id_nullable="00", headers=headers)


		game_info = data.next_n_games.get_dict()


		for game in game_info["data"]:


			previousGames = season.find({})
			
			check = True

			for pGame in previousGames:
				if pGame["_id"] == game[0]:
					check = False

			if check:
				info = {
					"_id": game[0],
					"game_date": game[1],
					"home_team_id": game[2],
					"away_team_id": game[3] 
				}

				season.insert_one(info)


	except requests.exceptions.ReadTimeout:
			print("Read Timeout")
			print("Waiting 1 min until retry")
			time.sleep(60)


	i = i + 1