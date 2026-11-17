import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    market_limit: int
    request_timeout: int
    raw_data_dir: Path
    log_level: str

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str


def read_required_text(name: str) -> str:
    value = os.getenv(name)

    if value is None or not value.strip():
        raise ValueError(f"{name} must not be empty")

    return value


def read_positive_int(name: str, default: int) -> int:
    raw_value = os.getenv(name, str(default))

    try:
        value = int(raw_value)
    except ValueError as error:
        raise ValueError(f"{name} must be an integer") from error

    if value <= 0:
        raise ValueError(f"{name} must be positive")

    return value


def load_settings() -> Settings:
    load_dotenv(
        dotenv_path=Path(".env"),
        override=False,
    )

    db_host = read_required_text("DB_HOST")
    db_port = read_positive_int("DB_PORT", 5433)
    db_name = read_required_text("DB_NAME")
    db_user = read_required_text("DB_USER")
    db_password = read_required_text("DB_PASSWORD")

    if db_port > 65535:
        raise ValueError("DB_PORT must not exceed 65535")

    market_limit = read_positive_int("MARKET_LIMIT", 20)
    request_timeout = read_positive_int("REQUEST_TIMEOUT", 15)

    raw_dir_text = os.getenv("RAW_DATA_DIR", "data/raw").strip()

    if not raw_dir_text:
        raise ValueError("RAW_DATA_DIR must not be empty")

    log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper()

    allowed_levels = {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    }

    if log_level not in allowed_levels:
        raise ValueError("LOG_LEVEL must be DEBUG, INFO, WARNING, ERROR or CRITICAL")

    return Settings(
        market_limit=market_limit,
        request_timeout=request_timeout,
        raw_data_dir=Path(raw_dir_text),
        log_level=log_level,
        db_host=db_host,
        db_port=db_port,
        db_name=db_name,
        db_user=db_user,
        db_password=db_password,
    )
