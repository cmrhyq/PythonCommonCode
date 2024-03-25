"""
@File          printLog.py
@Contact       cmrhyq@163.com
@License       (C)Copyright 2022-2025, AlanHuang
@Modify Time   2022/10/26 下午11:21
@Author        Alan Huang
@Version       0.0.1
@Description   None
"""

import logging
from logging.handlers import TimedRotatingFileHandler


class PrintLogger(object):
    def __init__(self, logfile, logsize, loglevel):
        self.logger = logging.getLogger()
        self.logger.setLevel(loglevel)
        self.formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d %(message)s")
        self.handler = logging.handlers.RotatingFileHandler(logfile, mode='a', maxBytes=logsize, backupCount=5)
        # self.handler = logging.StreamHandler()
        self.handler.setLevel(loglevel)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def error(self, msginfo, exc_val=False):
        self.logger.error(msginfo, exc_info=exc_val)

    def warn(self, msginfo, exc_val=False):
        self.logger.warning(msginfo, exc_info=exc_val)

    def info(self, msginfo):
        self.logger.info(msginfo)

    def debug(self, msginfo):
        self.logger.debug(msginfo)


if __name__ == '__main__':
    Log = PrintLogger('test.log', 1214, 'INFO')
    Log.info("this is a test.")
