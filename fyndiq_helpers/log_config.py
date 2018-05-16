import logging
import logging.config

import structlog


class HealthFilter(logging.Filter):
    def filter(self, record):
        request = getattr(record, 'request', None)
        return '/health' not in request if request else True


def add_sanic_request(logger, level, event_dict):
    record = event_dict.get('_record')
    request = getattr(record, 'request', None)
    if request:
        event_dict['event'] = request
    return event_dict


def setup(use_debug_settings: bool, use_logstash: bool, use_filters: bool):  # noqa
    """ Sets up the log configuration.

    Args:
        use_debug_settings: Set this to true to get all library logs and colors
        use_logstash: Set true to use logstash logging format
        use_filters: Set to true to remove health endpoint logs (
            useful for suppressing k8s liveness check)
    """

    timestamper = structlog.processors.TimeStamper(
        fmt="ISO", utc=True
    )
    pre_chain = [
        structlog.stdlib.add_log_level,
        timestamper,
        add_sanic_request
    ]

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'logstash': {
                '()': 'logstash_formatter.LogstashFormatterV1',
            },
            'dev': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.dev.ConsoleRenderer(
                    colors=True if use_debug_settings else False
                ),
                'foreign_pre_chain': pre_chain,
            }
        },
        'filters': {
            'health_filter': {
                '()': 'fyndiq_helpers.log_config.HealthFilter'
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'logstash' if use_logstash else 'dev',
                'filters': [] if use_filters else ['health_filter']
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'sanic': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False
            },
            'datadog': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'raven': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False
            },
            'confluent_kafka_helpers': {
                'handlers': ['console'],
                'level': 'DEBUG' if use_debug_settings else 'WARNING',
                'propagate': False
            },
            'eventsourcing_helpers': {
                'handlers': ['console'],
                'level': 'DEBUG' if use_debug_settings else 'WARNING',
                'propagate': False
            }
        }
    })
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            timestamper,
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
