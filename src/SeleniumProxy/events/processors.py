from deepmerge import always_merger
from structlog import BoundLoggerBase
import structlog


_METHOD_TO_NAME = {
    'critical': 'CRITICAL',
    'exception': 'ERROR',
    'error': 'ERROR',
    'warn': 'WARNING',
    'warning': 'WARNING',
    'info': 'INFO',
    'debug': 'DEBUG',
    'notset': 'NOTSET',
}


def add_log_level(logger, method_name, event_dict):
    event_dict['level'] = _METHOD_TO_NAME[method_name]
    return event_dict

def ecs_format(logger, method_name, event):
    

PROCESSORS = [
    structlog.stdlib.filter_by_level,
    add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.UnicodeDecoder(),
    # required as LogstashHandler uses `extra` for logging JSON values
    structlog.stdlib.render_to_log_kwargs,
    # NestedDictJSONRenderer(),
    # structlog.dev.ConsoleRenderer()
]
