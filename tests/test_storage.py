import json

from crypto_data_platform.storage import save_raw


def test_save_raw_writes_payload(tmp_path):
    payload = {
        "data": [
            {
                "id": "90",
                "name": "Bitcoin",
                "price_usd": "100.00",
            }
        ],
        "info": {"coins_num": 1},
    }

    output_dir = tmp_path / "raw"

    output_file = save_raw(payload, output_dir)

    assert output_file.parent == output_dir
    assert output_file.is_file()

    saved_payload = json.loads(output_file.read_text(encoding="utf-8"))

    assert saved_payload == payload
