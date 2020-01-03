import click
import mongo
from functions import *
import tweepy
from datetime import datetime, timedelta, timezone
import pytz

@click.command()
def main():

	# tweet different parameters 
	# program runs daily at 1:00 am after all games finishcd .

	# get twitter connection
	api = connect()

	#api.update_status("Test aws script")

	day = datetime.strftime(datetime.now(pytz.timezone('US/Eastern')) - timedelta(1), '%m-%d-%Y')

	tweetDailyLeaders(api, day)
	tweetStandOutPlayers(api, day)
	#tweetWeeklyLeaders(api)
	#tweetSeasonLeaders(api)

	return

if __name__ == '__main__':
	main()
