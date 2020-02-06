from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression


# player statistical performance for one game
def playerStatsOne(playerId, game, statType):

    teamStatsTable = getTable("19-20_PlayerStats")
    stats = teamStatsTable.find_one({"_id": playerId})

    # get most recent game
    boxScoreT = stats["boxScoreTraditional"][game]
    boxScoreA = stats["boxScoreAdvanced"][game]
    boxScoreU = stats["boxScoreUsage"][game]

    returnStats = []

    # clean data

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
	cluster = MongoClient("mongodb+srv://chase:thatredguy7@cluster0-rrnjh.mongodb.net/test?retryWrites=true&w=majority")
	return cluster['nba_data'][table]

def getSalary(salary):
    sal = salary.translate({ord('$'): None})
    return int(sal.translate({ord(','): None}))

def getTeam(team):
    return team[1:4]

def getPosition(player):
    return player[7:len(player)-1]

def getTodaysPlayers():
    
    page = requests.get("https://www.fantasypros.com/daily-fantasy/nba/fanduel-salary-changes.php")
    soup = BeautifulSoup(page.content, 'html.parser')
    soup.prettify()
    rawPlayers = soup.find("tbody").find_all("tr")

    players = []

    for row in rawPlayers:

        player = {}
        player["full_name"] = row.find("a", target="_blank").getText()
        player["salary"] = getSalary(row.find("td", class_="salary").getText())
        player["team"] = getTeam(row.find("small").getText())
        player["position"] = getPosition(row.find("small").getText())

        players.append(player)
    
    return players

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




def trainTestModel(player):

    playerStatsTable = getTable("19-20_PlayerStats")
    teamStatsTable = getTable("19-20_TeamStats")
    gamesTable = getTable("19-20_Season")

    playerStats = playerStatsTable.find_one({"player_name": player["full_name"]})

    if playerStats == None:
        return

    playerId = playerStats["_id"]



    lastGame = len(playerStats["boxScoreTraditional"])

    # 5 game window
    start = 0
    end = 4

    X_Train = []
    Y_Train = {}

    categories = ["FG3M", "FGM", "FTM", "REB", "AST", "BLK", "STL", "TO"]


    for cat in categories:
        Y_Train[cat] = []

    while end < lastGame - 1:

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
        statsT1 = teamStatsWindow(teamId, 0, end, "teamSeason")

        # opposing team performance over last 5 games
        statsT2 = teamStatsWindow(teamId, start, end, "TeamFive")

        # combine x vals
        X_Vals = statsP1 + statsP2 + statsT1 + statsT2

        # add X train and Y train to list
        X_Train.append(X_Vals)

        # get Y train vals
        for cat in categories:
            Y_val = playerStats["boxScoreTraditional"][end + 1][cat]
            if Y_val == None:
                Y_val = 0
            Y_Train[cat].append(Y_val)

        # iterate start and end games
        #print("done with iteration\tstart: " + str(start) + "\tend: " + str(end))
        
        start = start + 1
        end = end + 1

    for cat in categories:

        # get test vals for upcomming game
       # print("done getting testing_data")
        
        # player performance last game
        statsP1 = playerStatsOne(playerId, end, "playerLast")

        # player average performance over last 5 games
        statsP2 = playerStatsWindow(playerId, start, end, "playerFive") 

        # get opposing team id
        #teamId = getTodaysOpponetId(playerStats["team_id"])
        teamId = 1610612749

        # opopsing team performance over season
        statsT1 = teamStatsWindow(teamId, 0, end, "teamSeason")

        # opposing team performance over last 5 games
        statsT2 = teamStatsWindow(teamId, start, end, "TeamFive")

        # combine x vals
        X_Test = statsP1 + statsP2 + statsT1 + statsT2

        # train and test on data
        logreg = LogisticRegression(max_iter=10000)
        
        #print("training model")
        logreg.fit(X_Train, Y_Train[cat])

        #print("predicting model")

        answer = logreg.predict([X_Test])

        player[cat] = answer

        #print("Estimated " + cat + ": " + str(answer))

    print(player)
    return player
















    







    