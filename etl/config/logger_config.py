from config.settings import settings

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"custom_formatter": {"format": "%(levelname)-10s %(name)-10s [%(asctime)s] : %(message)s"}},
    "handlers": {
        "console_handler": {
            "class": "logging.StreamHandler",
            "formatter": "custom_formatter",
        },
    },
    "loggers": {"etl": {"handlers": ["console_handler"], "level": settings.log_level, "propagate": True}},
}
