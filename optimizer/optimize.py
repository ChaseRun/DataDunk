from bs4 import BeautifulSoup
import requests
from helperFunctions import *
import time
from concatData import *



playerStatsTable = getTable("19-20_PlayerStats")
teamTable = getTable("teams")

#teams = teamTable.find({})
teamCount = 1

START = time.time()



tylerTeams1 = [1610612757, 
            1610612748, 
            1610612754, 
            1610612759, 
            1610612765, 
            1610612741, 
            1610612743, 
            1610612755, 
            1610612758, 
            1610612761
]

tylerTeams2 = [1610612751, 
            1610612738, 
            1610612740, 
            1610612742, 
            1610612756, 
            1610612744, 
            1610612739, 
            1610612752, 
            1610612762, 
            1610612764
]

chaseTeams = [1610612745,
            1610612760,
            1610612746,
            1610612766,
            1610612749,
            1610612750,
            1610612737,
            1610612753,
            1610612747,
            1610612763
]


prevPlayers = ["Terrance Ferguson", "Fanilo Gallinari", "Steven Adams"]

for team in tylerTeams2:

    # get team name
    name = teamTable.find_one({"_id": team})

    print("Starting " + name["full_name"] + "\t " + str(teamCount) + " out of 15")

    players = playerStatsTable.find({"team_id": team})

    playerCount = 1
    #numPlayers = players.count

    for player in players:

        if player["player_name"] not in prevPlayers:

            #getNewStat(player)
            #time.sleep(30)
            print("Starting " + player["player_name"])
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
