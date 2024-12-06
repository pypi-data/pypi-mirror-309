import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
        },
        'simple': {
            'format': '%(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'INFO',
        },
        'file_info': {
            'class': 'logging.FileHandler',
            'filename': 'info.log',
            'formatter': 'standard',
            'level': 'INFO',
        },
        'file_debug': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'detailed',
            'level': 'DEBUG',
        },
        'file_error': {
            'class': 'logging.FileHandler',
            'filename': 'error.log',
            'formatter': 'detailed',
            'level': 'ERROR',
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file_info'],
            'level': 'INFO',
        },
        'inference_worker.core.worker': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

logger.error("example")