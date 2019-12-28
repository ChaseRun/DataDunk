import click
import mongo
from functions import *
import tweepy

@click.command()
def main():

	# tweet different parameters 
	# program runs daily at 1:00 am after all games finishcd .

	# get twitter connection
	api = connect()

	api.update_status("Test aws script")

	#tweetDailyLeaders(api)
	#tweetStandOutPlayers(api)
	#tweetWeeklyLeaders(api)
	#tweetSeasonLeaders(api)

	return

if __name__ == '__main__':
	main()
