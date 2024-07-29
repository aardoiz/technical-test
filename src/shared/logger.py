import sys
import logging

from loguru import logger

# Logger Genérico 

LOG_LEVEL = "DEBUG"  
DEBUG = True  

logger.remove()  

logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{module}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)
logger.add(
    sink=sys.stderr,
    level=LOG_LEVEL.upper(),
    serialize=not DEBUG,
    colorize=DEBUG,
    diagnose=DEBUG,
    format=logger_format,
    enqueue=True,
)

class EndpointFilter(logging.Filter):
    def __init__(self, excluded_endpoints: list[str]) -> None:
        super().__init__()
        self.excluded_endpoints = excluded_endpoints

    def filter(self, record: logging.LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] not in self.excluded_endpoints