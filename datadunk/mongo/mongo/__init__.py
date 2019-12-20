"""DataDunk:mongo package initializer."""
from nba_api.stats.endpoints import *
from pymongo import MongoClient
import requests
import time
import datetime

import index.update
from mongo.mongo.config import *
