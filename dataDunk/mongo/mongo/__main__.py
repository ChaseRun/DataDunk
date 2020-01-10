import click
import mongo
from update.boxScoreT import *
from update.boxScoreU import *
from update.boxScoreA import *
from update.updateGameOrder import *
from update.combinePlayerStats import *

@click.command()
def main():

	#updateBoxScoreTraditional()
	updateBoxScoreUsage()
	updateBoxScoreAdvanced()
	combinePlayerStats()


	return

if __name__ == '__main__':
	main()
