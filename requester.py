import requests


class Requester:
    """This is a class for making http requests"""

    def __init__(self, headers=None):
        """
        The constructor for Requester class

        :param headers: headers in request if needed
        """
        if headers is None:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
            }

    def get(self, url):
        """
        Get request

        :param url: web page address
        :return: response from server
        """
        response = requests.get(url=url, headers=self.headers)
        return response
