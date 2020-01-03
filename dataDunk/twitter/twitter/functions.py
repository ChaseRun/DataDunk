import click
import tweepy
from datetime import datetime, timedelta
from pymongo import MongoClient
from operator import itemgetter
import os

def connect():
	# connect to @DataDunk

	CONSUMER_KEY = "LzKKRxjNEyubbzK0l9ufd8lUl"
	CONSUMER_SECRET = "sLlh6oDx1O5pDEa3uBpa4WegEoljnGeIBc7OZ5zWR4hwFPLpSB"
	ACCESS_TOKEN = "1019367115063689223-w5mGwqTsOorSROuz0Xqd12wNV46hlD"
	ACCESS_SECRET = "K3WRoPZfJ99AC7c5HIRYaXOV8O60CNmXFzKNQUfUWjSdp"

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	
	return tweepy.API(auth)


def numToMonth(month):
	# convert number to month
	
	if  month == 1:
		return "Jan"
	elif  month == 2:
		return "Feb"
	elif  month == 3:
		return "Mar"
	elif  month == 4:
		return "April"
	elif  month == 5:
		return "May"
	elif  month == 6:
		return "June"
	elif  month == 7:
		return "July"
	elif  month == 8:
		return "Aug"
	elif  month == 9:
		return "Sep"
	elif  month ==10:
		return "Oct"
	elif  month == 11:
		return "Nov"
	else:
		return "Dec"

def printWeek(day):
	# return true if its start of new week
	db = cluster['nba_data']
	seasonGames = db["19-20_Weeks"]
	weeks = seasonGames.find({})
	
	if day in weeks["start"]:
		return True
	# not time to print
	return False	

def getWeekBoxScores(month, day, year):
	#  
	db = cluster['nba_data']
	boxScores = db["boxScoreTraditional"]
	games = db["19-20_Season"]
	
	index = 0
	scores = {}

	while index < 7:

		dayStr = str(year) + "-" + str(month) + "-" + str(day)
		week = seasonGames.find({"start": dayStr})

		for game in week:
			scores.append(game)

		# increment day
		day = day + 1
		if month == 2 and day > 29:
			month = month + 1
			day = 1
		if month == 12 and day > 31:
			month = 1
			day = 1
			year = 2020
		if month != 12 and day > 31:
			month = month + 1

		index = index + 1

	return scores

def checkUpdate():
	# return true if its 8:00am
	now = datetime.now()
	hour = now.strftime("%H")
	#if (int(hour) == 8):
		#return True
	
	return False
	

def getBoxScoreTable():
	# returns a mongodb table
	cluster = MongoClient('mongodb+srv://chase:thatredguy7@cluster0-rrnjh.mongodb.net/test?retryWrites=true&w=majority')
	return cluster['nba_data']["boxScoreTraditional"]

def tweetDailyLeaders(api, day):

	# check ifits 8:00am, (update time)
	#if not checkUpdate():
	#	print("Not 8:00am")
	#	return

	numLeaders = 5

	# get day
	printDay = datetime.strftime(datetime.now(pytz.timezone('US/Eastern')) - timedelta(1), '%m %d, %Y')

	month = printDay[3:]
	printDay = printDay[3:]
	printDay = numToMonth(month) + " " + printDay


	# get games
	data = getBoxScoreTable()
	games = data.find({"date": day})


	players = []

	# add players to list
	for game in games:
		for player in game["period"][0]["homeTeamPlayerStats"]:
			players.append(player)
		
		for player in game["period"][0]["awayTeamPlayerStats"]:
			players.append(player)

	topPts = players
	topAst = players
	topReb = players
	topBlk = players
	topStl = players
	topFG3M = players

	# remove players with no stats
	topPts[:] = [p for p in topPts if p.get('PTS') != None]
	topAst[:] = [p for p in topAst if p.get('AST') != None]
	topReb[:] = [p for p in topReb if p.get('REB') != None]
	topBlk[:] = [p for p in topBlk if p.get('BLK') != None]
	topStl[:] = [p for p in topStl if p.get('STL') != None]
	topFG3M[:] = [p for p in topFG3M if p.get('FG3M') != None]

	# sort stats
	topPts = sorted(topPts, key=itemgetter("PTS"))
	topAst = sorted(topAst, key=itemgetter("AST"))
	topReb = sorted(topReb, key=itemgetter("REB"))
	topBlk = sorted(topBlk, key=itemgetter("BLK"))
	topStl = sorted(topStl, key=itemgetter("STL"))
	topFG3M = sorted(topFG3M, key=itemgetter("FG3M"))

	# get top stats
	# reverse List and get top num leaders
	# get lastPlayer with min stat
	numLeaders = numLeaders - 1
	
	topPts = topPts[::-1]
	lastPlayer = numLeaders
	while topPts[lastPlayer]["PTS"] == topPts[numLeaders]["PTS"]:
		lastPlayer = lastPlayer + 1
	topPts = topPts[0: lastPlayer]

	topAst  = topAst [::-1]
	lastPlayer = numLeaders 
	while topAst[lastPlayer]["AST"] == topAst[numLeaders]["AST"]:
		lastPlayer = lastPlayer + 1
	topAst = topAst[0: lastPlayer]

	topReb = topReb[::-1]
	lastPlayer = numLeaders 
	while topReb[lastPlayer]["REB"] == topReb[numLeaders]["REB"]:
		lastPlayer = lastPlayer + 1
	topReb = topReb[0: lastPlayer]

	topBlk = topBlk[::-1]
	lastPlayer = numLeaders 
	while topBlk[lastPlayer]["BLK"] == topBlk[numLeaders]["BLK"]:
		lastPlayer = lastPlayer + 1
	topBlk = topBlk[0: lastPlayer]

	topStl = topStl[::-1]
	lastPlayer = numLeaders 
	while topStl[lastPlayer]["STL"] == topStl[numLeaders]["STL"]:
		lastPlayer = lastPlayer + 1
	topStl = topStl[0: lastPlayer]

	topFG3M = topFG3M[::-1]
	lastPlayer = numLeaders 
	while topFG3M[lastPlayer]["FG3M"] == topFG3M[numLeaders]["FG3M"]:
		lastPlayer = lastPlayer + 1
	topFG3M = topFG3M[0: lastPlayer]
	

	# tweet steals
	rank = 1	
	tweet = "Steal Leaders " + printDay + "\n\n"
	for player in topStl:
		tweet = tweet + str(rank) + ". " + str(player["PLAYER_NAME"]) + " " + str(player["STL"]) + "\n"
		rank = rank + 1
		if rank == 6:
			break
	api.update_status(tweet)

	# tweet blocks
	rank = 1	
	tweet = "Block Leaders " + printDay + "\n\n"
	for player in topBlk:
		tweet = tweet + str(rank) + ". " + str(player["PLAYER_NAME"]) + " " + str(player["BLK"]) + "\n"
		rank = rank + 1
		if rank == 6:
			break
	api.update_status(tweet)	
	
	# tweet rebounds
	rank = 1	
	tweet = "Rebound Leaders " + printDay + "\n\n"
	for player in topReb:
		tweet = tweet + str(rank) + ". " + str(player["PLAYER_NAME"]) + " " + str(player["REB"])+ "\n"
		rank = rank + 1
		if rank == 6:
			break
	api.update_status(tweet)

	# tweet assists
	rank = 1	
	tweet = "Assist Leaders " + printDay + "\n\n"
	for player in topAst:
		tweet = tweet + str(rank) + ". " + str(player["PLAYER_NAME"]) + " " + str(player["AST"]) + "\n"
		rank = rank + 1
		if rank == 6:
			break
	api.update_status(tweet)

	# tweet 3 points
	rank = 1	
	tweet = "3 Point Leaders " + printDay + "\n\n"
	for player in topFG3M:
		tweet = tweet + str(rank) + ". " + str(player["PLAYER_NAME"]) + " " + str(player["FG3M"]) + "\n"
		rank = rank + 1
		if rank == 6:
			break
	api.update_status(tweet)

	# tweet points
	rank = 1	
	tweet = "Point Leaders " + printDay + "\n\n"
	for player in topPts:
		tweet = tweet + str(rank) + ". " + str(player["PLAYER_NAME"]) + " " + str(player["PTS"]) + "\n"
		rank = rank + 1
		if rank == 6:
			break
	api.update_status(tweet)


	print("Tweeted Daily Leaders")

	return

def tweetWeeklyLeaders(api):
	numLeaders = 5

	# get day
	dt = datetime.datetime.today()
	realDay = dt.day
	month = dt.month
	year = dt.year

	day = str(dt.month) + "-" + str(dt.day) + "-" + str(dt.year)

	#if not printWeek(): 
		#return



	#dayList = getWeek(day)

	# get games
	data = getBoxScoreTable(day)

	games = data.find({"date": day})

	month = 12
	realDay = 24
	year = 2019

	games = getWeekBoxScores(month, realDay, year)

	players = []

	# add players to list
	for game in games:
		for player in game["period"][0]["homeTeamPlayerStats"]:
			
			if any(d["_id"] == player["_id"] for d in players):
				d["PTS"] = d["PTS"] + player["PTS"]
				d["AST"] = d["AST"] + player["AST"]
				d["REB"] = d["REB"] + player["REB"]
				d["BLk"] = d["BLK"] + player["BLK"]
				d["STL"] = d["STL"] + player["STL"]

		
		for player in game["period"][0]["awayTeamPlayerStats"]:
			if any(d["_id"] == player["_id"] for d in players):
				d["PTS"] = d["PTS"] + player["PTS"]
				d["AST"] = d["AST"] + player["AST"]
				d["REB"] = d["REB"] + player["REB"]
				d["BLk"] = d["BLK"] + player["BLK"]
				d["STL"] = d["STL"] + player["STL"]


	topPts = sorted(players, key=itemgetter("PTS"))
	topAst = sorted(players, key=itemgetter("AST"))
	topReb = sorted(players, key=itemgetter("REB"))
	topBlk = sorted(players, key=itemgetter("BLK"))
	topStl = sorted(players, key=itemgetter("STL"))



	# get top stats
	# reverse List and get top num leaders
	# get lastPlayer with min stat
	numLeaders = numLeaders - 1

	topPts = topPts[::-1]

	print(topPts[:3])
	exit()

	lastPlayer = numLeaders
	while topPts[lastPlayer]["PTS"] == topPts[numLeaders ]["PTS"]:
		lastPlayer = lastPlayer + 1
	topPts = topPts[0: lastPlayer]

	topAst  = topAst [::-1]
	lastPlayer = numLeaders
	while topAst[lastPlayer]["AST"] == topAst[numLeaders]["AST"]:
		lastPlayer = lastPlayer + 1
	topAst = topAst[0: lastPlayer]

	topReb = topReb[::-1]
	lastPlayer = numLeaders
	while topReb[lastPlayer]["REB"] == topReb[numLeaders]["REB"]:
		lastPlayer = lastPlayer + 1
	topReb = topReb[0: lastPlayer]

	topBlk = topBlk[::-1]
	lastPlayer = numLeaders
	while topBlk[lastPlayer]["BLK"] == topBlk[numLeaders]["BLK"]:
		lastPlayer = lastPlayer + 1
	topBlk = topBlk[0: lastPlayer]

	topStl = topStl[::-1]
	lastPlayer = numLeaders
	while topStl[lastPlayer]["STL"] == topStl[numLeaders]["STL"]:
		lastPlayer = lastPlayer + 1
	topStl = topStl[0: lastPlayer]
	

	# tweet steals
	rank = 1	
	tweet = "Steal Leaders " + numToMonth(month) + " " + str(realDay) + ", " + str(year) + "\n\n"
	for player in topStl:
		tweet = tweet + str(rank) + ". " + str(player["PLAYER_NAME"]) + " " + str(player["STL"]) + "\n"
		rank = rank + 1
	#api.update_status(tweet)

	# tweet blocks
	rank = 1	
	tweet = "Block Leaders " + numToMonth(month) + " " + str(realDay) + ", " + str(year) + "\n\n"
	for player in topBlk:
		tweet = tweet + str(rank) + ". " + str(player["PLAYER_NAME"]) + " " + str(player["BLK"]) + "\n"
		rank = rank + 1
	#api.update_status(tweet)	
	
	# tweet rebounds
	rank = 1	
	tweet = "Rebound Leaders " + numToMonth(month) + " " + str(realDay) + ", " + str(year) + "\n\n"
	for player in topReb:
		tweet = tweet + str(rank) + ". " + str(player["PLAYER_NAME"]) + " " + str(player["REB"])+ "\n"
		rank = rank + 1
	#api.update_status(tweet)

	# tweet assists
	rank = 1	
	tweet = "Assist Leaders " + numToMonth(month) + " " + str(realDay) + ", " + str(year) + "\n\n"
	for player in topAst:
		tweet = tweet + str(rank) + ". " + str(player["PLAYER_NAME"]) + " " + str(player["AST"]) + "\n"
		rank = rank + 1
	#api.update_status(tweet)

	# tweet points
	rank = 1	
	tweet = "Point Leaders " + numToMonth(month) + " " + str(realDay) + ", " + str(year) + "\n\n"
	for player in topPts:
		tweet = tweet + str(rank) + ". " + str(player["PLAYER_NAME"]) + " " + str(player["PTS"]) + "\n"
		rank = rank + 1
	api.update_status(tweet)

	
	return

def tweetSeasonLeaders(api):
	return

def tweetStandOutPlayers(api, day):
	
	# check ifits 8:00am, (update time)
	#if not checkUpdate():
	#	print("Not 8:00am")
	#	return

	numLeaders = 5

	# get day
	printDay = datetime.strftime(datetime.now(pytz.timezone('US/Eastern')) - timedelta(1), '%m %d, %Y')

	month = printDay[3:]
	printDay = printDay[3:]
	printDay = numToMonth(month) + " " + printDay


	# get games
	data = getBoxScoreTable()
	games = data.find({"date": day})


	players = []

	# add players to list
	for game in games:
		for player in game["period"][0]["homeTeamPlayerStats"]:
			players.append(player)
		
		for player in game["period"][0]["awayTeamPlayerStats"]:
			players.append(player)

	
	starPlayers = []

	# get star players
	for player in players:

		# over 20 points
		if player["PTS"] is not None and int(player["PTS"]) >= 20:
			starPlayers.append(player)
			#os.makedirs("twitter/photos/" + player["TEAM_ABBREVIATION"] + "/" + player["PLAYER_NAME"])
			continue

		# over 12 assists
		elif player["AST"] is not None and int(player["AST"]) >= 12:
			starPlayers.append(player)
			#os.makedirs("twitter/photos/" + player["TEAM_ABBREVIATION"] + "/" + player["PLAYER_NAME"])
			continue

		# over 12 rebounds
		elif player["REB"] is not None and int(player["REB"]) >= 12:
			starPlayers.append(player)
			#os.makedirs("twitter/photos/" + player["TEAM_ABBREVIATION"] + "/" + player["PLAYER_NAME"])
			continue

		# over 8 blocks
		elif player["BLK"] is not None and int(player["BLK"]) >= 8:
			starPlayers.append(player)
			#os.makedirs("twitter/photos/" + player["TEAM_ABBREVIATION"] + "/" + player["PLAYER_NAME"])
			continue

		# over 5 steals
		elif player["STL"] is not None and int(player["STL"]) >= 5:
			starPlayers.append(player)
			#os.makedirs("twitter/photos/" + player["TEAM_ABBREVIATION"] + "/" + player["PLAYER_NAME"])
			continue

		# check for double doubles and triple doubles
		pCheck = 0
		aCheck = 0
		rCheck = 0
		bCheck = 0
		sCheck = 0

		if player["PTS"] is not None and int(player["PTS"]) >= 10:
			pCheck = 1
		if player["AST"] is not None and int(player["AST"]) >= 10:
			aCheck = 1
		if player["REB"] is not None and int(player["REB"]) >= 10:
			rCheck = 1
		if player["BLK"] is not None and int(player["BLK"]) >= 10:
			bCheck = 1
		if player["STL"] is not None and int(player["STL"]) >= 10:
			sCheck = 1

		doubles = pCheck + aCheck + rCheck + bCheck + sCheck		
		# double double
		if doubles >= 2:
			starPlayers.append(player)
			#os.makedirs("twitter/photos/" + player["TEAM_ABBREVIATION"] + "/" + player["PLAYER_NAME"])


	count = 1
	print("Tweeting Star Players")
	for player in starPlayers:

		tweet = player["PLAYER_NAME"] + " last night: \n\n"

		tweet = tweet + str(player["PTS"]) + " Points\n"
		tweet = tweet + str(player["AST"]) + " Assists\n"
		tweet = tweet + str(player["REB"]) + " Rebounds\n"
		tweet = tweet + str(player["BLK"]) + " Blocks\n"
		tweet = tweet + str(player["STL"]) + " Steals\n\n"

		tweet = tweet + "FG% " + "{:.1%}".format(player["FG_PCT"]) + "(" + str(player["FGM"]) + "-" + str(player["FGA"]) + ")\n"
		tweet = tweet + "3PT% " + "{:.1%}".format(player["FG3_PCT"]) + "(" + str(player["FG3M"]) + "-" + str(player["FG3A"]) + ")\n"
		tweet = tweet + "FT% " + "{:.1%}".format(player["FT_PCT"]) + "(" + str(player["FTM"]) + "-" + str(player["FTA"]) + ")\n"

		api.update_status(tweet)
		print(str(count))
		count = count + 1

	return
	