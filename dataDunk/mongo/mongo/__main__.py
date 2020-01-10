import click
import mongo
from update.boxScoreT import *
from update.boxScoreU import *
from update.boxScoreA import *
from update.updateGameOrder import *
from update.combinePlayerStats import *
from update.combineTeamStats import *

@click.command()
def main():

	#updateBoxScoreTraditional()
	#time.sleep(120)
	#updateBoxScoreUsage()
	#time.sleep(120)
	#updateBoxScoreAdvanced()
	#combinePlayerStats()
	combineTeamStats()

	return

if __name__ == '__main__':
	main()
