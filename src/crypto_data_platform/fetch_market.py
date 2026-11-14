import logging
from pathlib import Path
from time import perf_counter

from crypto_data_platform.client import fetch_market
from crypto_data_platform.logging_config import configure_logging
from crypto_data_platform.storage import save_raw
from crypto_data_platform.transform import normalize_market
from crypto_data_platform.config import load_settings

logger = logging.getLogger(__name__)


def main() -> None:
    settings = load_settings()
    configure_logging(level=settings.log_level)

    started_at = perf_counter()
    stage = "fetch"

    logger.info(
        "Pipeline started: limit=%s timeout=%s raw_dir=%s",
        settings.market_limit,
        settings.request_timeout,
        settings.raw_data_dir,
    )

    try:
        payload = fetch_market(
            limit=settings.market_limit,
            timeout=settings.request_timeout,
        )

        stage = "save_raw"
        output_file = save_raw(
            payload,
            output_dir=settings.raw_data_dir,
        )

        stage = "normalize"
        records = normalize_market(payload)

    except Exception:
        logger.exception("Pipeline failed at stage=%s", stage)
        raise

    elapsed = perf_counter() - started_at

    logger.info(
        "Pipeline completed: records=%s raw_file=%s duration_seconds=%.3f",
        len(records),
        output_file,
        elapsed,
    )


if __name__ == "__main__":
    main()
