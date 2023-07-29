import click
from click import command

from src.commands.yomichan.server import TtsServer
from src.utils import Utils


@click.command()
@click.option("--run-server", is_flag=True, help="Will run a server which provides the audio source endpoint")
def yomichan(run_server: bool) -> command:
    if run_server:
        TtsServer.runServer()
        # TtsServer.voiceDemo()
        exit()

    Utils.exitWithError("No command given. Use --help")
    return
