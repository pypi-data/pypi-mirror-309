from __future__ import annotations
from pyspark.sql import SparkSession


### FOR LOCAL DEV ENV USE
class Log4j(object):

    def __init__(self, spark: SparkSession):
        conf = spark.sparkContext.getConf()
        app_id = conf.get("spark.app.id")
        app_name = conf.get("spark.app.name")

        log4j = spark._jvm.org.apache.log4j
        message_prefix = '<' + app_name + ' ' + app_id + '>'
        self.logger = log4j.LogManager.getLogger(message_prefix)

    def error(self, msg):
        """Log a error.

        :param: Warning message to write to log
        :return: None
        """
        self.logger.error(msg)
        return None

    def warn(self, message):
        """Log a warning.

        :param: Warning message to write to log
        :return: None
        """
        self.logger.warn(message)
        return None

    def info(self, message):
        """Log information.

        :param: Information message to write to log
        :return: None
        """
        self.logger.info(message)
        return None
