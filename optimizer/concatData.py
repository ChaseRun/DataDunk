from pymongo import MongoClient
import numpy as np
import bsonnumpy
from bson.json_util import dumps

client = MongoClient("mongodb+srv://chase:thatredguy7@cluster0-rrnjh.mongodb.net/test?retryWrites=true&w=majority")
collection = client['nba_data']["19-20_PlayerStats"]

queryFilter = {'_id': 202695 }
queryProjection = { '$arrayElmAt': [ '$boxScoreTraditional', 68] }

proj = { '_id': 0, 
         "player_name": 0, 
         "team_id": 0, 
         "boxScoreAdvanced": 0, 
         "boxScoreusage": 0, 
         'boxScoreTraditional': {'$elemMatch': {"numGame": 0} } 
         }

test = collection.find_one(queryFilter, proj)

print(dumps(test))
#exit()

dtype = np.dtype([('MIN', 'S10'), 
                ('FMG', np.int64), 
                ('FGA', np.int64), 
                ('FG_PCT', np.double), 
                ('FG3M', np.int64), 
                ('FG3A', np.int64), 
                ('FG3_PCT', np.double), 
                ('FTM', np.int64), 
                ('FTA', np.int64),
                ('FT_PCT', np.double), 
                ('OREB', np.int64), 
                ('DREB', np.int64), 
                ('REB', np.int64), 
                ('AST', np.int64), 
                ('STL', np.int64), 
                ('BLK', np.int64), 
                ('TO', np.int64), 
                ('PF', np.int64), 
                ('PTS', np.int64), 
                ('PLUS_MINUS', np.int64)])

ndarray = bsonnumpy.sequence_to_ndarray(collection.find_raw_batches(queryFilter, proj), dtype, collection.count(queryFilter))

print(ndarray)


# for each game

# create player dict

# traditional
# advanced
# usage

# add each to player dict

# add player last game stats

# add average player stats over last 5 games

# add average team stats overt last 5 games

# add team stats over season