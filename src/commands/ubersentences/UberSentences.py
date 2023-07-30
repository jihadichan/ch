import click
from click import command

from src.commands.ubersentences.functions import CreateMnemonics
from src.commands.yomichan.functions import TtsServer, CreateHanziDict
from src.lookups.PinyinLookup import PinyinLookup
from src.utils import Utils


@click.command()
@click.option("--create-mnemonics", is_flag=True,
              help="Will create the mnemonics.js file for the UberSentences deck")
def ubersentences(create_mnemonics: bool) -> command:

    if create_mnemonics:
        pinyinLookup = PinyinLookup.create()
        CreateMnemonics.run(pinyinLookup)
        exit()

    Utils.exitWithError("No command given. Use --help")
    return
