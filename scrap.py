import configparser
import logging.config
import sys

from page_handler import PageHandler
from requester import Requester
from text_parser import TextParser
from utils import create_dirs
from logger.logger import LogDecorator


@LogDecorator()
def main(url):
    config = configparser.RawConfigParser()
    config.read("scraper.conf")
    handler = PageHandler(requester=Requester,
                          parser=TextParser,
                          scrap_config=config
                          )
    text = handler.handle(url)

    path = create_dirs(url)

    with open(path + ".txt", 'w', encoding="utf-8") as out:
        out.write(text)


if __name__ == "__main__":

    try:
        main(sys.argv[1])
    except Exception as e:
        pass
