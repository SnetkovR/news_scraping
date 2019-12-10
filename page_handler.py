from exceptions.content_exception import ContentTypeException
from exceptions.response_exception import ResponseException
from logger.logger import LogDecorator


class PageHandler:
    """This is a class for handle web pages for some pretty style."""

    def __init__(self, requester, parser, scrap_config):
        """
        The constructor for PageHandler class

        :param requester: class that is responsible for web page requests
        :param parser: class that is responsible for web page requests
        :param scrap_config: config with info about template
        """
        self.requester = requester
        self.parser = parser
        self.config = scrap_config

    @LogDecorator()
    def handle(self, url):
        """
        The function for take and transform web page

        :param url: web page address
        :return: text from a web page in template format
        """
        response = self.__take_page(url)
        parser = self.parser(self.config)

        if getattr(self.parser, "parse"):
            parser.parse(response.text)
        else:
            raise NotImplementedError("The parser does not match the declared interface")

        return parser.text

    @LogDecorator()
    def __take_page(self, url):
        """
        The function for take web page

        :param url: web page address
        :return: response from server
        """
        requester = self.requester()
        if getattr(self.requester, "get"):
            response = requester.get(url)
        else:
            raise NotImplementedError("The requester does not match the declared interface")

        if response.status_code != 200:
            raise ResponseException({"message": f"Response code {response.status_code}."})

        if "text/html" not in response.headers['content-type']:
            raise ContentTypeException({"message": "Result not html text as expected."})

        return response
