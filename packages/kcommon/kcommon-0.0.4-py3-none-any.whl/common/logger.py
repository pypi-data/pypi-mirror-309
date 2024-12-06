import logging as logger


### FOR LOCAL DEV ENV USE
class Logger(object):

    def error(self, msg):
        """Log a error.

        :param: Warning message to write to log
        :return: None
        """
        logger.error(msg)
        return None

    def warn(self, message):
        """Log a warning.

        :param: Warning message to write to log
        :return: None
        """
        logger.warning(message)
        return None

    def info(self, message):
        """Log information.

        :param: Information message to write to log
        :return: None
        """
        logger.info(message)
        return None
