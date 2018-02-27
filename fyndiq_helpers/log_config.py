import logging
import logging.config

import structlog


def setup(config):
    timestamper = structlog.processors.TimeStamper(
        fmt="ISO", utc=True
    )
    pre_chain = [
        structlog.stdlib.add_log_level,
        timestamper,
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
                    colors=True if config.DEBUG else False
                ),
                'foreign_pre_chain': pre_chain,
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'dev' if config.DEBUG else 'logstash'
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'datadog': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
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
