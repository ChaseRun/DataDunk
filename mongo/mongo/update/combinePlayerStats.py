"""
Update CombinePlayerStats

Chase Austin
"""
from pymongo import MongoClient
import requests
import time
import datetime
from update.helperFunctions import *


def combinePlayerStats():

    boxScoreTraditional = getTable("boxScoreTraditional")
    boxScoreAdvanced = getTable("boxScoreAdvanced")
    boxScoreUsage = getTable("boxScoreUsage")
    newGames = gameIds()
    playerStats = getTable("19-20_PlayerStats")

    count = 0

    print("Assigning BoxScore stats to individual players...")
    for game in newGames:

        # box score traditional
        #print("box score traditional")
        stats = boxScoreTraditional.find_one({"_id": game["_id"]}, no_cursor_timeout=True)            
        for player in stats["period"][0]["homeTeamPlayerStats"]:
            
            playerItem = playerStats.find_one({"_id": player["PLAYER_ID"]})

            # check for player in collection
            if playerItem == None:

                emptyList1 = []
                emptyList2 = []
                emptyList3 = []

                submit = {
                    "_id": player["PLAYER_ID"],
                    "player_name": player["PLAYER_NAME"],
                    "team_id": player["TEAM_ID"],
                    "boxScoreTraditional": emptyList1,
                    "boxScoreAdvanced": emptyList2,
                    "boxScoreUsage": emptyList3
                }

                # create new player in collection
                newData = player
                del newData['TEAM_ID']
                del newData["TEAM_ABBREVIATION"]
                del newData["TEAM_CITY"]
                del newData["PLAYER_ID"]
                del newData["PLAYER_NAME"]
                newData["numGame"] = 0
                newData["home/away"] = 1
                submit["boxScoreTraditional"].append(newData)

                playerStats.insert_one(submit)
            
            else:

                playerId = player["PLAYER_ID"]

                newData = player
                del newData['TEAM_ID']
                del newData["TEAM_ABBREVIATION"]
                del newData["TEAM_CITY"]
                del newData["PLAYER_ID"]
                del newData["PLAYER_NAME"]
                newData["home/away"] = 1
                last = len(playerItem["boxScoreTraditional"]) - 1

                
                newData["numGame"] = playerItem["boxScoreTraditional"][last]["numGame"] + 1 

                playerStats.update({"_id": playerId}, 
                                {'$push': {"boxScoreTraditional": newData}})

        for player in stats["period"][0]["awayTeamPlayerStats"]:
            
            playerItem = playerStats.find_one({"_id": player["PLAYER_ID"]})

            # check for player in collection
            if playerItem == None:

                emptyList1 = []
                emptyList2 = []
                emptyList3 = []

                submit = {
                    "_id": player["PLAYER_ID"],
                    "player_name": player["PLAYER_NAME"],
                    "team_id": player["TEAM_ID"],
                    "boxScoreTraditional": emptyList1,
                    "boxScoreAdvanced": emptyList2,
                    "boxScoreUsage": emptyList3
                }

                # create new player in collection
                newData = player
                del newData['TEAM_ID']
                del newData["TEAM_ABBREVIATION"]
                del newData["TEAM_CITY"]
                del newData["PLAYER_ID"]
                del newData["PLAYER_NAME"]
                newData["numGame"] = 0
                newData["home/away"] = 1
                submit["boxScoreTraditional"].append(newData)

                playerStats.insert_one(submit)
            
            else:

                playerId = player["PLAYER_ID"]

                newData = player
                del newData['TEAM_ID']
                del newData["TEAM_ABBREVIATION"]
                del newData["TEAM_CITY"]
                del newData["PLAYER_ID"]
                del newData["PLAYER_NAME"]
                newData["home/away"] = 0
                last = len(playerItem["boxScoreTraditional"]) - 1
                newData["numGame"] = playerItem["boxScoreTraditional"][last]["numGame"] + 1 

                playerStats.update({"_id": playerId}, 
                                    {'$push': {"boxScoreTraditional": newData}})
        
        # end boxScoreTraditional
        # start boxScoreAdvanced
        #print("box score advanced")
        stats = boxScoreAdvanced.find_one({"_id": game["_id"]}, no_cursor_timeout=True)

        for player in stats["period"][0]["homeTeamPlayerStats"]:
            
            playerItem = playerStats.find_one({"_id": player["PLAYER_ID"]})

            playerId = player["PLAYER_ID"]

            newData = player
            del newData['TEAM_ID']
            del newData["TEAM_ABBREVIATION"]
            del newData["TEAM_CITY"]
            del newData["PLAYER_ID"]
            del newData["PLAYER_NAME"]
            newData["home/away"] = 0

            if len(playerItem["boxScoreAdvanced"]) == 0:
                newData["numGame"] = 0
            else:
                last = len(playerItem["boxScoreAdvanced"]) - 1
                newData["numGame"] = playerItem["boxScoreAdvanced"][last]["numGame"] + 1 

            playerStats.update({"_id": playerId}, 
                                {'$push': {"boxScoreAdvanced": newData}})


        for player in stats["period"][0]["awayTeamPlayerStats"]:
                
            playerItem = playerStats.find_one({"_id": player["PLAYER_ID"]})

            playerId = player["PLAYER_ID"]

            newData = player
            del newData['TEAM_ID']
            del newData["TEAM_ABBREVIATION"]
            del newData["TEAM_CITY"]
            del newData["PLAYER_ID"]
            del newData["PLAYER_NAME"]
            newData["home/away"] = 0

            if len(playerItem["boxScoreAdvanced"]) == 0:
                newData["numGame"] = 0
            else:
                last = len(playerItem["boxScoreAdvanced"]) - 1
                newData["numGame"] = playerItem["boxScoreAdvanced"][last]["numGame"] + 1 

            playerStats.update({"_id": playerId}, 
                                {'$push': {"boxScoreAdvanced": newData}})

        # end boxScoreAdvanced
        # start boxScoreUsage
        #print("box score usage")
        stats = boxScoreUsage.find_one({"_id": game["_id"]}, no_cursor_timeout=True)

        for player in stats["period"][0]["homeTeamPlayerStats"]:
            
            playerItem = playerStats.find_one({"_id": player["PLAYER_ID"]})

            playerId = player["PLAYER_ID"]

            newData = player
            del newData['TEAM_ID']
            del newData["TEAM_ABBREVIATION"]
            del newData["TEAM_CITY"]
            del newData["PLAYER_ID"]
            del newData["PLAYER_NAME"]
            newData["home/away"] = 0

            if len(playerItem["boxScoreUsage"]) == 0:
                newData["numGame"] = 0
            else:
                last = len(playerItem["boxScoreUsage"]) - 1
                newData["numGame"] = playerItem["boxScoreUsage"][last]["numGame"] + 1 

            playerStats.update({"_id": playerId}, 
                                {'$push': {"boxScoreUsage": newData}})


        for player in stats["period"][0]["awayTeamPlayerStats"]:
                
            playerItem = playerStats.find_one({"_id": player["PLAYER_ID"]})

            playerId = player["PLAYER_ID"]

            newData = player
            del newData['TEAM_ID']
            del newData["TEAM_ABBREVIATION"]
            del newData["TEAM_CITY"]
            del newData["PLAYER_ID"]
            del newData["PLAYER_NAME"]
            newData["home/away"] = 0

            if len(playerItem["boxScoreUsage"]) == 0:
                newData["numGame"] = 0
            else:
                last = len(playerItem["boxScoreUsage"]) - 1
                newData["numGame"] = playerItem["boxScoreUsage"][last]["numGame"] + 1 

            playerStats.update({"_id": playerId}, 
                                {'$push': {"boxScoreUsage": newData}})

        count = count + 1
        print("on game " + str(count))