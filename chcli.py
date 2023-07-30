import click

from src.commands.uberhanzi.UberHanzi import uberhanzi
from src.commands.ubersentences.UberSentences import ubersentences
from src.commands.yomichan.YomiChan import yomichan


@click.group()
def main():
    pass


if __name__ == '__main__':
    main.add_command(uberhanzi)
    main.add_command(yomichan)
    main.add_command(ubersentences)
    main()
