"""
Update boxScoreTraditional collection

Chase Austin
"""
from nba_api.stats.endpoints import boxscoretraditionalv2
from pymongo import MongoClient
import requests
import time
import datetime
from helperFunctions import *


boxScoreT = getTable("boxScoreTraditional")
boxScoreA = getTable("boxScoreAdvanced")
boxScoreU = getTable("boxScoreUsage")

# need to delete from 20-29
days = ["01-20-2020", "01-21-2020", "01-22-2020", "01-23-2020", "01-24-2020", "01-25-2020", "01-26-2020", "01-27-2020", "01-28-2020", "01-29-2020"]

for day in days:    

    boxScoreT.delete_many({"date": day})
    boxScoreA.delete_many({"date": day})
    boxScoreU.delete_many({"date": day})

# re add game data from 20-29


data = boxscoretraditionalv2.BoxScoreTraditionalV2(end_period=p, 
																		end_range="0", 
																		game_id=str(game["_id"]), 
																		range_type="0", 
																		start_period="1", 
																		start_range=p, 
																		proxy=proxy, 
																		timeout=15)
