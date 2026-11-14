import logging
import time


def configure_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        fmt="%(asctime)sZ %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    formatter.converter = time.gmtime

    handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[handler],
    )
