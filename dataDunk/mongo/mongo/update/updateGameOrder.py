"""
Update CombinePlayerStats

Chase Austin
"""
from pymongo import MongoClient
import requests
import time
import datetime
from update.helperFunctions import *


def updateGameOrder():

    games = getTable("19-20_Season")


    dates = previousGames()

    count = 1

    for date in dates:

        stats = games.find({"game_date": date})

        # make sure game was played on this day
        check = 0
        for s in stats:
            check = check + 1
            continue
        
        if check != 0:
            games.update_many({"game_date": date}, {"$set": {"order": count}})
            count = count + 1

        print(date)



