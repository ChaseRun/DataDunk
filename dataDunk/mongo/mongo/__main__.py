import click
import mongo
from update.boxScoreT import *

@click.command()
def main():

	updateBoxScoreTraditional()


	return

if __name__ == '__main__':
	main()
