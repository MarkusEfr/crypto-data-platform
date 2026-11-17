from crypto_data_platform.config import load_settings


def test_load_settings_reads_environment(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    monkeypatch.setenv("MARKET_LIMIT", "5")
    monkeypatch.setenv("REQUEST_TIMEOUT", "10")
    monkeypatch.setenv("RAW_DATA_DIR", "custom/raw")
    monkeypatch.setenv("LOG_LEVEL", "debug")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "crypto_data")
    monkeypatch.setenv("DB_USER", "crypto_user")
    monkeypatch.setenv("DB_PASSWORD", "crypto_password")

    settings = load_settings()

    assert settings.market_limit == 5
    assert settings.request_timeout == 10
    assert settings.raw_data_dir == tmp_path.__class__("custom/raw")
    assert settings.log_level == "DEBUG"
