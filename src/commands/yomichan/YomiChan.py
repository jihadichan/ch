import click
from click import command

from src.commands.yomichan.functions import TtsServer, CreateHanziDict
from src.lookups.PinyinLookup import PinyinLookup
from src.utils import Utils


@click.command()
@click.option("--run-server", is_flag=True, help="Will run a server which provides the audio source endpoint")
@click.option("--create-hanzi-dict", is_flag=True,
              help="Will create the dict for hanzi lookup based on the UberHanzi deck")
def yomichan(run_server: bool, create_hanzi_dict: bool) -> command:
    if run_server:
        TtsServer.runServer()
        # TtsServer.voiceDemo() # For debug to test voices
        exit()

    if create_hanzi_dict:
        pinyinLookup = PinyinLookup.create()
        CreateHanziDict.run(pinyinLookup)
        exit()

    Utils.exitWithError("No command given. Use --help")
    return
