import json
import logging

from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)


def save_raw(payload: dict, output_dir: Path) -> Path:
    """
    Save the raw payload to a JSON file in the specified output directory.

    Args:
        payload (dict): The payload to save.
        output_dir (Path): The directory where the file will be saved.

    Returns:
        Path: The path to the saved file.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output_file = output_dir / f"coinlore_market_{timestamp}.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    logger.info("Saved raw payload to %s", output_file)

    return output_file
