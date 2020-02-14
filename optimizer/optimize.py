from bs4 import BeautifulSoup
import requests
from helperFunctions import *
import time
from concatData import *



playerStatsTable = getTable("19-20_PlayerStats")
teamTable = getTable("teams")

teams = teamTable.find({})
teamCount = 1

START = time.time()

for team in teams:

    print("Starting " + team["full_name"] + "\t " + str(teamCount) + " out of 30")

    players = playerStatsTable.find({"team_id": team["_id"]})
    playerCount = 1

    numPlayers = players.count
    
    for player in players:

        #getNewStat(player)
        concatMLData(player)
        #print(str(playerCount) + "/" + str(numPlayers) + "Players")
        

END = time.time()
print("\n\nFinished")
print("Took " + str(((END - START) / 60 / 60)) + " hours.")

exit()


players = getTodaysPlayers()

newlist = sorted(players, key=lambda k: k['salary'], reverse=True) 

listOfPlayers = []

count = 1
total = len(newlist)

for player in newlist:
    print("Calculating stats for: " + player["full_name"])
    #listOfPlayers.append(trainTestModel(player))

    
    start = time.time()
    trainTestModel(player)
    end = time.time()

    print("Operation took", end - start, " seconds")

    print(str(count) + "/" + str(total))
    count = count + 1

with open("Values.txt", "w") as filehandle:
    for item in listOfPlayers:
        filehandle.write(listitem)
