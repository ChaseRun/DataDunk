import click
import mongo
from update.boxScoreT import *

@click.command()
@click.argument("collection", nargs=1)
def main(collection):

	if collection == "boxScoreTraditional":
		updateBoxScoreTraditional()


	return

if __name__ == '__main__':
	main()
