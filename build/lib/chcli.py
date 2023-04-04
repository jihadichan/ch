import click

from src.commands.uberhanzi.UberHanzi import uberhanzi


@click.group()
def main():
    pass


if __name__ == '__main__':
    main.add_command(uberhanzi)
    main()
