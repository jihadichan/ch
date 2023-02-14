import click
from click import command

from src.commands.uberhanzi import ScrapeHanzi, ScrapeMp3
from src.commands.uberhanzi.HanziFreqLookup import HanziFreqLookup
from src.commands.uberhanzi.PinyinLookup import PinyinLookup
from src.commands.uberhanzi.RadicalsLookup import RadicalsLookup
from src.utils import Utils


@click.command()
@click.option("--scrape-hanzi", is_flag=True, help="Will scrape unknown hanzi and cache them, sourced from uberhanzi/resources/hanzi_list.txt")
@click.option("--scrape-mp3", is_flag=True, help="Will scrape all pinyin pronunciation MP3 files and cache them, sourced from uberhanzi/resources/pinyin.txt")
def uberhanzi(scrape_hanzi: bool, scrape_mp3: bool) -> command:
    hanziFreqLookup = HanziFreqLookup.create()
    pinyinLookup = PinyinLookup.create()
    radicalsLookup = RadicalsLookup.create()

    if scrape_hanzi:
        ScrapeHanzi.scrape(hanziFreqLookup, pinyinLookup, radicalsLookup)
        exit()

    if scrape_mp3:
        ScrapeMp3.scrape(pinyinLookup)
        exit()

    Utils.exitWithError("No command given. Use --help")
    return
