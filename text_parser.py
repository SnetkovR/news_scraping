import copy

from bs4 import BeautifulSoup

from utils import concatenate


class TextParser:
    """This is a class for transform web page in readble text"""

    def __init__(self, config):
        """
        The constructor for TextParser class

        :param tags: html tags for parse
        :param config: parser config
        """
        self._config = config
        self._text = ""
        self.tags = eval(self._config.get("parser", "tags"))
        self.state = []
        head = int(self._config.get("parser", "head"))
        tail = int(self._config.get("parser", "tail"))
        if head >= 0:
            self.head = head
        else:
            self.head = 0

        if tail >= 0:
            self.tail = tail
        else:
            self.tail = 0

        self._max_len = 80 - 1
        self.rules = {
            '<a href="': "[",
            '">': "] ",
            '</a>': ""
        }

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text += value

    def parse(self, page):
        """Function for parse html page"""
        soup = BeautifulSoup(page, 'html.parser')
        tags_list = soup.find_all(self.tags)

        for tag in tags_list:
            tag = self.__replace_href(tag)
            self.state.append(tag)

        self.state = self.state[self.head:len(self.state) - self.tail]
        self._create_text()

    def __replace_href(self, tag):
        """Function for replace html ref to []"""
        if "<a href=" in str(tag.contents):
            if len(tag.contents) > 1:
                tag = concatenate(list(tag.contents))
            else:
                tag = str(tag.contents)[1:len(str(tag.contents)) - 1]
            for k, v in self.rules.items():
                tag = tag.replace(k, v)
        else:
            tag = tag.get_text()

        return tag

    def __split_seq(self, sequence):
        """Function for split text on readable parts"""
        seq = copy.copy(sequence)
        result = ""
        while len(seq) > self._max_len:
            if seq[self._max_len] == "":
                result += seq[:self._max_len] + "\n"
                seq = seq[self._max_len:]
            else:
                whitespace_index = self._max_len - seq[:self._max_len][::-1].find(" ")
                result += seq[:whitespace_index] + "\n"
                seq = seq[whitespace_index:]
        result += seq
        return result

    def _create_text(self):
        """Function for create final text page"""
        assert len(self.state) > 0
        tmp = ""
        for tag in self.state:
            if "<span" in tag or "<div" in tag:
                continue
            if len(tag) > self._max_len:
                tmp += self.__split_seq(tag) + "\n" + "\n"
            else:
                tmp += tag + "\n" + "\n"

        self.text = copy.copy(tmp)
