import configparser
import logging.config
import sys

from page_handler import PageHandler
from requester import Requester
from text_parser import TextParser
from utils import create_dirs


def main(url, logger):
    config = configparser.RawConfigParser()
    config.read("scraper.conf")
    handler = PageHandler(requester=Requester,
                          parser=TextParser,
                          logger=logger,
                          scrap_config=config
                          )
    text = handler.handle(url)

    path = create_dirs(url)

    with open(path + ".txt", 'w', encoding="utf-8") as out:
        out.write(text)

    logger.info("Result successful written.")


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG,
                        handlers=[
                            logging.FileHandler("history.log"),
                            logging.StreamHandler(sys.stdout)
                        ])
    logger = logging.getLogger()

    try:
        main(sys.argv[1], logger)
    except Exception as e:
        logger.error("Exception occurred", exc_info=True)
