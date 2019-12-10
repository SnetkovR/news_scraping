import functools
import sys
import logging.config

from helpers.singleton import SingletonType


class LogDecorator(object, metaclass=SingletonType):
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                            level=logging.DEBUG,
                            handlers=[
                                logging.FileHandler("history.log"),
                                logging.StreamHandler(sys.stdout)
                            ])
        self.logger = logging.getLogger()

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            try:
                self.logger.debug("Started {0}".format(fn.__name__))
                result = fn(*args, **kwargs)
                self.logger.debug("Ended {0}".format(fn.__name__))
                return result
            except Exception as ex:
                self.logger.debug("Exception {0}".format(ex))
                raise ex
        return decorated
