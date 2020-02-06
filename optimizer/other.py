from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import pandas as pd
from sklearn.linear_model import LogisticRegression


# player statistical performance for one game
def playerStatsOne(playerId, game, statType):

    teamStatsTable = getTable("19-20_PlayerStats")
    stats = teamStatsTable.find_one({"_id": playerId})

    # get most recent game
    boxScoreT = stats["boxScoreTraditional"][game]
    boxScoreA = stats["boxScoreAdvanced"][game]
    boxScoreU = stats["boxScoreUsage"][game]

    returnStats = {}

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
            returnStats[statType + "_" + key] = 0
        else:
            returnStats[statType + "_" + key] = boxScoreT[key]

     # boxScoreTraditional stats
    for key in boxScoreA:
        if boxScoreA[key] == None:
            returnStats[statType + "_" + key] = 0
        else:
            returnStats[statType + "_" + key] = boxScoreA[key]

     # boxScoreTraditional stats
    for key in boxScoreU:
        if boxScoreU[key] == None:
            returnStats[statType + "_" + key] = 0
        else:
            returnStats[statType + "_" + key] = boxScoreU[key]

    return returnStats    

# average player statistical performance across past N games
# N is 5 for now
def playerStatsWindow(playerId, start, end, statType):

    stats = []
    returnStat = {}

    count = start

    while count < end:
        stats.append(playerStatsOne(playerId, count, statType))
        count = count + 1

    df = pd.DataFrame(stats)
    return dict(df.mean())



# opposing team defense average statistical performance across the entire season
def teamStatsOne(teamId, game, statType):
   
    teamStatsTable = getTable("19-20_TeamStats")
    stats = teamStatsTable.find_one({"_id": teamId})

    boxScoreT = stats["boxScoreTraditional"][game]
    boxScoreA = stats["boxScoreAdvanced"][game]

    returnStats = {}

    # add keys to return array
    keyAdd = True

    # get boxScoreT sums
    keys = list(boxScoreT.keys())
    keys.remove("GAME_ID")
    keys.remove("numGame")
    
    for key in keys:
        if boxScoreT[key] == None:
            returnStats[statType + "_" + key] = 0
        else:
            returnStats[statType + "_" + key] = boxScoreT[key]

    # get boxScoreA sums
    keys = list(boxScoreA.keys())
    keys.remove("GAME_ID")
    keys.remove("numGame")
    keys.remove("MIN")
    keys.remove("home/away")

    for key in keys:
        if boxScoreA[key] == None:
            returnStats[statType + "_" + key] = 0
        else:
            returnStats[statType + "_" + key] = boxScoreA[key]

    return returnStats
    


# opposing team defense average statistical performance acorss past N games
# N is 5 for now
def teamStatsWindow(teamId, start, end, statType):

    stats = []
    returnStat = {}

    count = start

    while count < end:
        stats.append(teamStatsOne(teamId, count, statType))
        count = count + 1

    df = pd.DataFrame(stats)
    return dict(df.mean())


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


def optimizePlayer(player):

    categories = ["FG3M", "FGM", "FTM", "REB", "AST", "BLK", "STL", "TO"]

    for stat in categories:
        trainTestModel(player, stat)



def trainTestModel(player, stat):



    playerStatsTable = getTable("19-20_PlayerStats")
    teamStatsTable = getTable("19-20_TeamStats")
    gamesTable = getTable("19-20_Season")

    playerStats = playerStatsTable.find_one({"player_name": player["full_name"]})

    playerId = playerStats["_id"]


    lastGame = len(playerStats["boxScoreTraditional"])

    # 5 game window
    start = 0
    end = 4

    X_Train = []
    Y_Train = []

    print(lastGame)

    while end < lastGame - 2:

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
        X_Vals = {**statsP1, **statsP2, **statsT1, **statsT2}

        # get Y train val
        Y_val = playerStats["boxScoreTraditional"][end + 1][stat]

        # add X train and Y train to list
        X_Train.append(X_Vals)
        Y_Train.append(Y_val)

        # iterate start and end games
        start = start + 1
        end = end + 1

        print("done with iteration\tstart: " + str(start) + "\tend: " + str(end))
        


    # get test vals for upcomming game
    print("done getting testing_data")
    
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
    X_TestVals = {**statsP1, **statsP2, **statsT1, **statsT2}

    # train and test on data
    logreg = LogisticRegression()


    print("\n")
    print("\n")
    print("\n")

    

    Xlist = [v for k, v in dict.items()] 

    print(Xlist)
    
    print("\n")
    print("\n")
    print("\n")
    
    print(Y_Train)

    print("training model")
    logreg.fit(Xlist, Y_Train)

    print("predicting model")

    print("\n")
    print("\n")

    print(logreg.predict(X_TestVals))














    







    