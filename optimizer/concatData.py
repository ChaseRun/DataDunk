from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import time


# player statistical performance for one game
def playerStatsOne(playerId, game, statType):

    playerStatsTable = getTable("19-20_PlayerStats")
    stats = playerStatsTable.find_one({"_id": playerId})

    # get most recent game
    boxScoreT = stats["boxScoreTraditional"][game]
    boxScoreA = stats["boxScoreAdvanced"][game]
    boxScoreU = stats["boxScoreUsage"][game]

    returnStats = []

    del boxScoreT["GAME_ID"]
    del boxScoreT["START_POSITION"]
    del boxScoreT["COMMENT"]
    del boxScoreT["numGame"]

    del boxScoreA["GAME_ID"]
    del boxScoreA["START_POSITION"]
    del boxScoreA["COMMENT"]
    del boxScoreA["numGame"]
    del boxScoreA["MIN"]
    del boxScoreA["home/away"]

    del boxScoreU["GAME_ID"]
    del boxScoreU["START_POSITION"]
    del boxScoreU["COMMENT"]
    del boxScoreU["numGame"]
    del boxScoreU["MIN"]
    del boxScoreU["home/away"]

    # boxScoreTraditional stats
    for key in boxScoreT:
        if boxScoreT[key] == None:
            returnStats.append(0)
        else:

            if key == "MIN":
                returnStats.append(extractMin(boxScoreT[key]))
            else:
                returnStats.append(boxScoreT[key])

     # boxScoreTraditional stats
    for key in boxScoreA:
        if boxScoreA[key] == None:
            returnStats.append(0)
        else:
            returnStats.append(boxScoreA[key])

     # boxScoreTraditional stats
    for key in boxScoreU:
        if boxScoreU[key] == None:
            returnStats.append(0)
        else:
            returnStats.append(boxScoreU[key])

    return returnStats    

# average player statistical performance across past N games
# N is 5 for now
def playerStatsWindow(playerId, start, end, statType):

    stats = []

    count = start

    while count <= end:
        stats.append(playerStatsOne(playerId, count, statType))
        count = count + 1

    return list(map(lambda x: sum(x)/len(x), zip(*stats)))



# opposing team defense average statistical performance across the entire season
def teamStatsOne(teamId, game, statType):

    teamStatsTable = getTable("19-20_TeamStats")
    stats = teamStatsTable.find_one({"_id": teamId})

    boxScoreT = stats["boxScoreTraditional"][game]
    boxScoreA = stats["boxScoreAdvanced"][game]

    returnStats = []

    # add keys to return array
    keyAdd = True

    # get boxScoreT sums
    keys = list(boxScoreT.keys())
    keys.remove("GAME_ID")
    keys.remove("numGame")
    
    for key in keys:
        if boxScoreT[key] == None:
            returnStats.append(0)
        else:
            if key == "MIN":
                returnStats.append(extractMin(boxScoreT[key]))
            else:
                returnStats.append(boxScoreT[key])

    # get boxScoreA sums
    keys = list(boxScoreA.keys())
    keys.remove("GAME_ID")
    keys.remove("numGame")
    keys.remove("MIN")
    keys.remove("home/away")

    for key in keys:
        if boxScoreA[key] == None:
            returnStats.append(0)
        else:
            returnStats.append(boxScoreA[key])

    return returnStats
    


# opposing team defense average statistical performance acorss past N games
# N is 5 for now
def teamStatsWindow(teamId, start, end, statType):

    stats = []

    count = start

    while count <= end:
        stats.append(teamStatsOne(teamId, count, statType))
        count = count + 1

    return list(map(lambda x: sum(x)/len(x), zip(*stats)))


def getTable(table):
	# returns a mongodb table
	cluster = MongoClient("mongodb+srv://chase:thatredguy7@cluster0-rrnjh.mongodb.net/test?retryWrites=true&w=majority&connectTimeoutMS=480000")
	return cluster['nba_data'][table]

def getSalary(salary):
    sal = salary.translate({ord('$'): None})
    return int(sal.translate({ord(','): None}))

def getTeam(team):
    return team[1:4]

def getPosition(player):
    return player[7:len(player)-1]


def extractMin(min):

    returnMin = 0

    if len(min) == 4:
        returnMin = int(min[0])
        seconds = int(min[2:])
        seconds = seconds / 60
        return returnMin + seconds

    elif len(min) == 5:
        returnMin = int(min[:2])
        seconds = int(min[3:])
        seconds = seconds / 60
        return returnMin + seconds

    else:
        return 0

def getTodaysOpponetId(teamId):
    
    gamesTable = getTable("19-20_Season")
    day = datetime.strftime(datetime.now(pytz.timezone('US/Eastern')) - timedelta(1), '%m-%d-%Y')
    todayGames = gamesTable.find({"game_date": day})

    for game in todayGames:
        if game["home_team_id"] == teamId:
            
            return game["away_team_id"]
        
        elif game["away_team_id"] == teamId:
            
            return game["home_team_id"]


def concatMLData(player):

    playerStatsTable = getTable("19-20_PlayerStats")
    teamStatsTable = getTable("19-20_TeamStats")
    gamesTable = getTable("19-20_Season")

    playerStats = playerStatsTable.find_one({"_id": player["_id"]})

    if playerStats == None:
        return

    playerId = player["_id"]

    lastGame = len(playerStats["boxScoreTraditional"])

    # 5 game window
    start = 0
    end = 4

    categories = ["FG3M", "FGM", "FTM", "REB", "AST", "BLK", "STL", "TO", "MIN"]

    totalStart = time.time()

    while end < lastGame - 1:

        print("\t" + str(end) + "/" + str(lastGame))

        Y_Train = {}

        # player performance last game
        statsP1 = playerStatsOne(playerId, end, "playerLast")

        # player average performance over last 5 games
        statsP2 = playerStatsWindow(playerId, start, end, "playerFive") 

        # get opposing team id
        gameTrain = playerStats["boxScoreTraditional"][end + 1]["GAME_ID"]
        otherTeamSide = (playerStats["boxScoreTraditional"][end + 1]["home/away"])
        otherTeam = gamesTable.find_one({"_id": gameTrain})
        teamId = 0
        if otherTeamSide == 0:
            teamId = otherTeam["home_team_id"]
        else:
            teamId = otherTeam["away_team_id"]

        # opopsing team performance over season

        teamObj = teamStatsTable.find_one({"_id": teamId})
        teamEnd = len(teamObj["boxScoreTraditional"]) - 1

        statsT1 = teamStatsWindow(teamId, 0, teamEnd, "teamSeason")

        # opposing team performance over last 5 games
        statsT2 = teamStatsWindow(teamId, teamEnd - 4, teamEnd, "TeamFive")

        # combine x vals
        X_Vals = statsP1 + statsP2 + statsT1 + statsT2

        # add X vals to player
        playerStatsTable.update({"_id":  playerId}, { "$push": { "ML_Data.X_Vals": X_Vals }})
    
        # add Y vals to player
        for cat in categories:
            Y_val = playerStats["boxScoreTraditional"][end + 1][cat]

            if cat == "MIN":
                if Y_val == None:
                    Y_val = 0
                else:
                    Y_val = extractMin(Y_val)

            else if Y_val == None:
                Y_val = 0

            place = "ML_Data.Y_Vals." + cat
            playerStatsTable.update({"_id":  playerId}, { "$push": { place: Y_val}})

        start = start + 1
        end = end + 1

    totalEnd = time.time()

    print("\t" + player["player_name"] + "\t" + str(int(totalEnd - totalStart)) + " seconds")
    
'''
def getNewStat(player):


    playerId = player["_id"]

    playerStatsTable = getTable("19-20_PlayerStats")

    player = playerStatsTable.find_one({"_id": playerId})

    count = 0

    totalGames = len(player["boxScoreTraditional"])

    while count < totalGames:

        PTS = player["boxScoreTraditional"][count]["PTS"]
        FG = player["boxScoreTraditional"][count]["FGM"] + player["boxScoreTraditional"][count]["FG3M"]
        FGA = player["boxScoreTraditional"][count]["FGA"] + player["boxScoreTraditional"][count]["FG3A"]
        FTA = player["boxScoreTraditional"][count]["FTA"]
        FT = player["boxScoreTraditional"][count]["FTM"]
        ORB = player["boxScoreTraditional"][count]["OREB"]
        DRB = player["boxScoreTraditional"][count]["DREB"]
        STL = player["boxScoreTraditional"][count]["STL"]
        AST = player["boxScoreTraditional"][count]["AST"]
        BLK = player["boxScoreTraditional"][count]["BLK"]
        PF = player["boxScoreTraditional"][count]["PF"]
        TOV = player["boxScoreTraditional"][count]["TO"]

        GmSc =PTS+(0.4*FG)-(0.7*FGA)-(0.4*(FTA-FT))+(0.7*ORB)+(0.3*DRB)+STL+(0.7*AST)+(0.7*BLK)-(0.4*PF)-TOV

        playerStatsTable.update({"_id":  playerId}, { "$set": { "boxScoreTraditional": GmSc}})

        count = count + 1
        print(playerId)
        exit()


'''