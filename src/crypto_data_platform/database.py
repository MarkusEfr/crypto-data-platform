import logging
from datetime import datetime

import psycopg

from crypto_data_platform.config import Settings

logger = logging.getLogger(__name__)


def load_market(
    records: list[dict],
    observed_at: datetime,
    settings: Settings,
) -> None:
    if not records:
        raise ValueError("records must not be empty")

    if observed_at.utcoffset() is None:
        raise ValueError("observed_at must have a timezone")

    coin_rows = [
        (
            record["coin_id"],
            record["symbol"],
            record["name"],
        )
        for record in records
    ]

    observation_rows = [
        (
            record["coin_id"],
            observed_at,
            record["price_usd"],
        )
        for record in records
    ]

    with psycopg.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        connect_timeout=10,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO public.coins (
                    coin_id,
                    symbol,
                    name
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (coin_id)
                DO UPDATE SET
                    symbol = EXCLUDED.symbol,
                    name = EXCLUDED.name
                """,
                coin_rows,
            )

            cursor.executemany(
                """
                INSERT INTO public.market_observations (
                    coin_id,
                    observed_at,
                    price_usd
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (coin_id, observed_at)
                DO NOTHING
                """,
                observation_rows,
            )

    logger.info(
        "Market batch committed: input_records=%s observed_at=%s",
        len(records),
        observed_at.isoformat(),
    )
