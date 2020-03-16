from pythonjsonlogger import jsonlogger
import structlog
import logstash
import logging
import json


def robotlogger():
    logger = logging.getLogger("robot_events")
    logger.setLevel(logging.DEBUG)
    rmq_handler = logstash.AMQPLogstashHandler(
        host='localhost', version=1, durable=True)
    rmq_handler.setFormatter(jsonlogger.JsonFormatter())
    logger.addHandler(rmq_handler)
    return logger


def requestlogger():
    logger = logging.getLogger("web_events")
    logger.setLevel(logging.DEBUG)
    rmq_handler = logstash.AMQPLogstashHandler(
        host='localhost', version=1, durable=True)
    rmq_handler.setFormatter(jsonlogger.JsonFormatter())
    logger.addHandler(rmq_handler)
    return logger
