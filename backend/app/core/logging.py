import logging
from app.core.settings import settings

DEFAULT_LOGLEVEL = logging.INFO


class Logger():
    def setupLogger() -> None:
        try:
            lv = logging.getLevelName(settings.LOGLEVEL)

            Logger.getLogger().setLevel(lv)
            logging.getLogger("uvicorn.error").setLevel(lv)
            logging.getLogger("uvicorn.access").setLevel(lv)
            logging.getLogger("uvicorn.asgi").setLevel(lv)
        except Exception:
            log = Logger.getLogger()
            name = logging._levelToName(DEFAULT_LOGLEVEL)
            log.warning(
                f"Invalid log level: {settings.LOGLEVEL}. Using default: {name}."
            )

            Logger.getLogger().setLevel(DEFAULT_LOGLEVEL)
            logging.getLogger("uvicorn.error").setLevel(DEFAULT_LOGLEVEL)
            logging.getLogger("uvicorn.access").setLevel(DEFAULT_LOGLEVEL)
            logging.getLogger("uvicorn.asgi").setLevel(DEFAULT_LOGLEVEL)

    def getLogger() -> logging.Logger:
        logger = logging.getLogger("uvicorn")
        return logger


Logger.setupLogger()
log: logging.Logger = Logger.getLogger()
