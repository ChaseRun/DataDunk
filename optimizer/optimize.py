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

'''
cats = {
    "FG3M": [],
    "FGM": [],
    "FTM": [],
    "REB": [],
    "AST": [],
    "BLK": [],
    "STL": [],
    "TO": [],
    "MIN": []
}


playerStatsTable.update_many({"team_id": 1610612742}, { "$set" : {"ML_Data.X_Vals" : []}})
playerStatsTable.update_many({"team_id": 1610612742}, { "$set" : {"ML_Data.Y_Vals" : cats}})
exit()
'''

chase1 = [
            1610612742,   # mavs
            1610612756    # suns
]

chase2 = [
            1610612752,   # knicks
            1610612762,   # jazz
            1610612764    # wizards
]


chase3 = [
            1610612759,   # spurs
            1610612765    # pistons
]


chase4 = [
            1610612755,   # 76
            1610612758,   # kings
            1610612761   # raptors
]


chaseTeams = [
            #1610612745,
            #1610612760,
            #1610612746,
            1610612766,
            1610612749,
            1610612750,
            1610612737,
            1610612753,
            1610612747,
            1610612763
]

for team in chase1:

    # get team name
    name = teamTable.find_one({"_id": team})
    print("Starting " +  name["full_name"] + "\t " + str(teamCount) + " out of 15")
    
    
    players = playerStatsTable.find({"team_id": team})

    for player in players:

        print("Starting " + player["player_name"])
        concatMLData(player)


                
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
