import click
import mongo
from update.helperFunctions import *
from update.boxScoreT import *
from update.boxScoreU import *
from update.boxScoreA import *
from update.updateGameOrder import *
from update.combinePlayerStats import *
from update.combineTeamStats import *

@click.command()
@click.option("-s", "--start", nargs=1, required=False)
def main(start):


	if start:
		
		start_date = start
		end_date = getYesterdaysDate()
		days = dateRange(start_date, end_date)

		for day in days:

			print("Starting at: " + start)

			updateBoxScoreTraditional(day)
			time.sleep(30)
			updateBoxScoreUsage(day)
			time.sleep(30)
			updateBoxScoreAdvanced(day)
			#combinePlayerStats()
			#combineTeamStats()

	
	else:
		
		date = getYesterdaysDate()
		
		exit()
		
		updateBoxScoreTraditional()
		time.sleep(120)
		updateBoxScoreUsage()
		time.sleep(120)
		updateBoxScoreAdvanced()
		combinePlayerStats()
		combineTeamStats()

	return

if __name__ == '__main__':
	main()
