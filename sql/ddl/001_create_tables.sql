CREATE TABLE coins (
    coin_id TEXT PRIMARY KEY,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,

    CONSTRAINT coins_id_not_blank
        CHECK (btrim(coin_id) <> ''),

    CONSTRAINT coins_symbol_not_blank
        CHECK (btrim(symbol) <> ''),

    CONSTRAINT coins_name_not_blank
        CHECK (btrim(name) <> '')
);


CREATE TABLE market_observations (
    coin_id TEXT NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    price_usd NUMERIC NOT NULL,

    CONSTRAINT market_observations_pk
        PRIMARY KEY (coin_id, observed_at),

    CONSTRAINT market_observations_coin_fk
        FOREIGN KEY (coin_id)
        REFERENCES coins (coin_id),

    CONSTRAINT market_observations_price_valid
        CHECK (
            price_usd > 0
            AND price_usd < 'Infinity'::NUMERIC
        )
);