from typing import Type
from SeleniumProxy.events.instances import robotlogger, requestlogger
from logstash import AMQPLogstashHandler
from structlog import wrap_logger
from .processors import PROCESSORS
import structlog
import logging


class Singleton(type):

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances.keys():
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls


class LogEventManager(object):

    __metaclass__ = Singleton

    _loggers = {}

    def __init__(self, *args, **kwargs):
        self._loggers['suite_metrics'] = robotlogger()
        self._loggers['http_metrics'] = requestlogger()

    @staticmethod
    def getLogger(name=None):
        if name not in LogEventManager._loggers.keys():
            logging.basicConfig()
            LogEventManager._loggers[name] = logging.getLogger(str(name))
        if isinstance(LogEventManager._loggers[name].handlers[0], AMQPLogstashHandler):
            return wrap_logger(
                LogEventManager._loggers[name],
                processors=PROCESSORS,
                context_class=structlog.threadlocal.wrap_dict(dict),
                logger_factory=structlog.stdlib.LoggerFactory(),
                wrapper_class=structlog.stdlib.BoundLogger)
        return LogEventManager._loggers[name]
