from pathlib import Path
import requests

from crypto_data_platform.client import fetch_market
from crypto_data_platform.storage import save_raw


def main() -> None:
    try:
        payload = fetch_market(limit=20)
    except requests.exceptions.Timeout:
        print("Request timed out. Please try again later.")
        raise

    output_file = save_raw(
        payload,
        output_dir=Path("data/raw"),
    )

    print(f"Saved {len(payload['data'])} coins to {output_file}")


if __name__ == "__main__":
    main()
