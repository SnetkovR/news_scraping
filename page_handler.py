from exceptions.content_exception import ContentTypeException
from exceptions.response_exception import ResponseException


class PageHandler:
    """This is a class for handle web pages for some pretty style."""

    def __init__(self, requester, parser, logger, scrap_config):
        """
        The constructor for PageHandler class

        :param requester: class that is responsible for web page requests
        :param parser: class that is responsible for web page requests
        :param logger: instance of the logging
        :param scrap_config: config with info about template
        """
        self.requester = requester
        self.parser = parser
        self.logger = logger
        self.config = scrap_config

    def handle(self, url):
        """
        The function for take and transform web page

        :param url: web page address
        :return: text from a web page in template format
        """
        response = self.__take_page(url)
        self.logger.info(f"Successful request to {url}")

        parser = self.parser(self.config)
        parser.parse(response.text)
        self.logger.info("Page successful parsed.")

        return parser.text

    def __take_page(self, url):
        """
        The function for take web page

        :param url: web page address
        :return: response from server
        """
        requester = self.requester()
        response = requester.get(url)

        if response.status_code != 200:
            self.logger.error(f"Response code {response.status_code}.")
            raise ResponseException({"message": f"Response code {response.status_code}."})

        if "text/html" not in response.headers['content-type']:
            self.logger.error("Result not html text as expected.")
            raise ContentTypeException({"message": "Result not html text as expected."})

        return response
