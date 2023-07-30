import click
from click import command

from src.commands.uberhanzi.functions import ScrapeHanzi, ScrapeMp3, CreateCsv, CreateReadings, CreateConfs
from src.lookups.HanziFreqLookup import HanziFreqLookup
from src.lookups.PinyinLookup import PinyinLookup
from src.lookups.RadicalsLookup import RadicalsLookup
from src.utils import Utils


@click.command()
@click.option("--scrape-hanzi", is_flag=True, help="Will scrape unknown hanzi and cache them, sourced from 'uberhanzi/resources/hanzi_list.txt'")
@click.option("--scrape-mp3", is_flag=True, help="Will scrape all pinyin pronunciation MP3 files and cache them, sourced from 'uberhanzi/resources/pinyin.txt'")
@click.option("--create-csv", is_flag=True, help="Creates the CSV to import in Anki. Stored in 'output/'")
@click.option("--create-readings", is_flag=True, help="Creates the reading mnemonics as JSON for Anki. Scraped from 'docs/readings.md'. Stored in 'output/'")
@click.option("--create-confs", is_flag=True, help="Creates the confs.js file for Anki. Stored in 'output/'")
def uberhanzi(scrape_hanzi: bool, scrape_mp3: bool, create_csv: bool, create_readings: bool, create_confs: bool) -> command:
    hanziFreqLookup = HanziFreqLookup.create()
    pinyinLookup = PinyinLookup.create()
    radicalsLookup = RadicalsLookup.create()

    if scrape_hanzi:
        ScrapeHanzi.scrape(hanziFreqLookup, radicalsLookup)
        exit()

    if scrape_mp3:
        ScrapeMp3.scrape(pinyinLookup)
        exit()

    if create_csv:
        CreateCsv.create(hanziFreqLookup, pinyinLookup)
        exit()

    if create_readings:
        CreateReadings.create()
        exit()

    if create_confs:
        CreateConfs.create()
        exit()

    Utils.exitWithError("No command given. Use --help")
    return
