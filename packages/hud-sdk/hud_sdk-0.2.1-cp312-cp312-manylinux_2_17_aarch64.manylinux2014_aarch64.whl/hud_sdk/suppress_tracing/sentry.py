from logging import getLogger


def suppress_logger(logger_name: str) -> None:
    try:
        try:
            # Check if Sentry SDK is installed
            import sentry_sdk.integrations.logging as sentry_logging

            sentry_logging.ignore_logger(logger_name)
            getLogger(logger_name).info(
                "Logger {} suppressed in Sentry".format(logger_name)
            )
        except ImportError:
            getLogger(logger_name).info(
                "Sentry SDK is not installed. No suppression applied."
            )
    except Exception:
        pass
