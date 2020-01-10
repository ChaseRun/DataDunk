"""
Update CombinePlayerStats

Chase Austin
"""
from pymongo import MongoClient
import requests
import time
import datetime
from update.helperFunctions import *


def combineTeamStats():

    boxScoreTraditional = getTable("boxScoreTraditional")
    boxScoreAdvanced = getTable("boxScoreAdvanced")
    newGames = gameIds()
    teamStatsTable = getTable("19-20_TeamStats")

    count = 0

    print("Assigning BoxScore stats to individual teams...")

    for game in newGames:


        # box score traditional
        
        # home team
        stats = boxScoreTraditional.find_one({"_id": game["_id"]}, no_cursor_timeout=True)            
        teamStats = stats["period"][0]["homeTeamStats"]
        teamItem = teamStatsTable.find_one({"_id": teamStats["TEAM_ID"]})

        # check for team in collection
        if teamItem == None:

            emptyList1 = []
            emptyList2 = []

            submit = {
                "_id": teamStats["TEAM_ID"],
                "boxScoreTraditional": emptyList1,
                "boxScoreAdvanced": emptyList2,
            }

            # create new team in collection
            newData = teamStats
            del newData['TEAM_ID']
            del newData["TEAM_NAME"]
            del newData["TEAM_ABBREVIATION"]
            del newData["TEAM_CITY"]

            newData["numGame"] = 0
            newData["home/away"] = 1
            submit["boxScoreTraditional"].append(newData)

            teamStatsTable.insert_one(submit)
        
        else:

            teamId = teamStats["TEAM_ID"]

            newData = teamStats
            del newData['TEAM_ID']
            del newData["TEAM_NAME"]
            del newData["TEAM_ABBREVIATION"]
            del newData["TEAM_CITY"]

            newData["home/away"] = 1
            last = len(teamItem["boxScoreTraditional"]) - 1

            newData["numGame"] = teamItem["boxScoreTraditional"][last]["numGame"] + 1 

            teamStatsTable.update({"_id": teamId}, 
                            {'$push': {"boxScoreTraditional": newData}})

        # away team
        teamStats = stats["period"][0]["awayTeamStats"]
        teamItem = teamStatsTable.find_one({"_id": teamStats["TEAM_ID"]})    
        # check for team in collection
        if teamItem == None:

            emptyList1 = []
            emptyList2 = []

            submit = {
                "_id": teamStats["TEAM_ID"],
                "boxScoreTraditional": emptyList1,
                "boxScoreAdvanced": emptyList2,
            }

            # create new player in collection
            newData = teamStats
            del newData['TEAM_ID']
            del newData["TEAM_NAME"]
            del newData["TEAM_ABBREVIATION"]
            del newData["TEAM_CITY"]

            newData["numGame"] = 0
            newData["home/away"] = 0
            submit["boxScoreTraditional"].append(newData)

            teamStatsTable.insert_one(submit)
        
        else:

            teamId = teamStats["TEAM_ID"]

            newData = teamStats
            del newData['TEAM_ID']
            del newData["TEAM_NAME"]
            del newData["TEAM_ABBREVIATION"]
            del newData["TEAM_CITY"]

            newData["home/away"] = 0
            last = len(teamItem["boxScoreTraditional"]) - 1

            newData["numGame"] = teamItem["boxScoreTraditional"][last]["numGame"] + 1 

            teamStatsTable.update({"_id": teamId}, 
                            {'$push': {"boxScoreTraditional": newData}})
        
        
        # end boxScoreTraditional
        # start boxScoreAdvanced
        
        # home team
        stats = boxScoreAdvanced.find_one({"_id": game["_id"]}, no_cursor_timeout=True)
        teamStats = stats["period"][0]["homeTeamStats"]
        teamItem = teamStatsTable.find_one({"_id": teamStats["TEAM_ID"]})

        teamId = teamStats["TEAM_ID"]

        newData = teamStats
        del newData['TEAM_ID']
        del newData["TEAM_NAME"]
        del newData["TEAM_ABBREVIATION"]
        del newData["TEAM_CITY"]

        newData["home/away"] = 1

        if len(teamItem["boxScoreAdvanced"]) == 0:
            newData["numGame"] = 0
        else:
            last = len(teamItem["boxScoreAdvanced"]) - 1
            newData["numGame"] = teamItem["boxScoreAdvanced"][last]["numGame"] + 1 

        teamStatsTable.update({"_id": teamId}, 
                        {'$push': {"boxScoreAdvanced": newData}})
        

        # away team
        teamStats = stats["period"][0]["awayTeamStats"]
        teamItem = teamStatsTable.find_one({"_id": teamStats["TEAM_ID"]})

        teamId = teamStats["TEAM_ID"]

        newData = teamStats
        del newData['TEAM_ID']
        del newData["TEAM_NAME"]
        del newData["TEAM_ABBREVIATION"]
        del newData["TEAM_CITY"]

        newData["home/away"] = 0
        
        if len(teamItem["boxScoreAdvanced"]) == 0:
            newData["numGame"] = 0
        else:
            last = len(teamItem["boxScoreAdvanced"]) - 1
            newData["numGame"] = teamItem["boxScoreAdvanced"][last]["numGame"] + 1 

        teamStatsTable.update({"_id": teamId}, 
                        {'$push': {"boxScoreAdvanced": newData}})

        # end boxScoreAdvanced

        count = count + 1
        print("on game " + str(count))
    
    print("done with " + str(day))