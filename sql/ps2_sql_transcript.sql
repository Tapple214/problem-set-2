CREATE TABLE my_stocks (
    symbol VARCHAR(20) NOT NULL,
    n_shares INTEGER NOT NULL,
    date_acquired DATE NOT NULL
);

\copy my_stocks FROM 'my_stocks.txt' WITH (FORMAT text);

SELECT * FROM my_stocks;

CREATE TABLE stock_prices AS
SELECT DISTINCT
    symbol,
    CURRENT_DATE AS quote_date,
    31.415 AS price
FROM my_stocks;

SELECT * FROM stock_prices;

-- Expected output:
--  symbol | quote_date |  price
-- --------+------------+---------
--  AAPL   | 2026-09-24 | 31.415
--  GOOG   | 2026-09-24 | 31.415
--  META   | 2026-09-24 | 31.415
--  MSFT   | 2026-09-24 | 31.415
--  NVDA   | 2026-09-24 | 31.415

-- Part B
CREATE TABLE newly_acquired_stocks (
    symbol VARCHAR(20) NOT NULL,
    n_shares INTEGER NOT NULL,
    date_acquired DATE NOT NULL
);

INSERT INTO newly_acquired_stocks (symbol, n_shares, date_acquired)
SELECT symbol, n_shares, date_acquired
FROM my_stocks
WHERE date_acquired >= DATE '2026-04-01';

SELECT * FROM newly_acquired_stocks;

-- Expected output:
--  symbol | n_shares | date_acquired
-- --------+----------+---------------
--  NVDA   |        8 | 2026-04-12
--  META   |       12 | 2026-05-05

SELECT
    ms.symbol,
    ms.n_shares,
    sp.price AS price_per_share,
    ms.n_shares * sp.price AS current_value
FROM my_stocks ms
JOIN stock_prices sp ON ms.symbol = sp.symbol;

-- Expected output:
--  symbol | n_shares | price_per_share | current_value
-- --------+----------+-----------------+---------------
--  AAPL   |       10 |          31.415 |       314.150
--  MSFT   |       20 |          31.415 |       628.300
--  GOOG   |        5 |          31.415 |       157.075
--  NVDA   |        8 |          31.415 |       251.320
--  META   |       12 |          31.415 |       376.980

INSERT INTO my_stocks (symbol, n_shares, date_acquired)
VALUES ('AIT', 10, CURRENT_DATE);

SELECT
    ms.symbol,
    ms.n_shares,
    sp.price AS price_per_share,
    ms.n_shares * sp.price AS current_value
FROM my_stocks ms
LEFT OUTER JOIN stock_prices sp ON ms.symbol = sp.symbol;

-- Expected output includes AIT with NULL price and current_value:
--  symbol | n_shares | price_per_share | current_value
-- --------+----------+-----------------+---------------
--  AAPL   |       10 |          31.415 |       314.150
--  MSFT   |       20 |          31.415 |       628.300
--  GOOG   |        5 |          31.415 |       157.075
--  NVDA   |        8 |          31.415 |       251.320
--  META   |       12 |          31.415 |       376.980
--  AIT    |       10 |                 |
-- (5 rows)

CREATE OR REPLACE FUNCTION stock_value(p_symbol VARCHAR)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    total INTEGER := 0;
    i INTEGER;
BEGIN
    FOR i IN 1..length(p_symbol) LOOP
        total := total + ascii(substring(p_symbol FROM i FOR 1));
    END LOOP;
    RETURN total;
END;
$$;

SELECT stock_value('IBM');
-- Expected: 216

UPDATE stock_prices
SET price = stock_value(symbol);

SELECT * FROM stock_prices;

CREATE OR REPLACE FUNCTION portfolio_value()
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
DECLARE
    total NUMERIC := 0;
    row RECORD;
BEGIN
    FOR row IN
        SELECT ms.n_shares, sp.price
        FROM my_stocks ms
        JOIN stock_prices sp ON ms.symbol = sp.symbol
    LOOP
        total := total + (row.n_shares * row.price);
    END LOOP;
    RETURN total;
END;
$$;

SELECT portfolio_value();

INSERT INTO my_stocks (symbol, n_shares, date_acquired)
SELECT ms.symbol, ms.n_shares, CURRENT_DATE
FROM my_stocks ms
JOIN stock_prices sp ON ms.symbol = sp.symbol
WHERE sp.price > (
    SELECT AVG(price) FROM stock_prices
);

-- Report A
SELECT symbol, SUM(n_shares) AS total_shares
FROM my_stocks
GROUP BY symbol
ORDER BY symbol;

-- Report B
SELECT
    ms.symbol,
    SUM(ms.n_shares) AS total_shares,
    sp.price AS price_per_share,
    SUM(ms.n_shares) * sp.price AS total_current_value
FROM my_stocks ms
JOIN stock_prices sp ON ms.symbol = sp.symbol
GROUP BY ms.symbol, sp.price
ORDER BY ms.symbol;

-- Report C
SELECT
    ms.symbol,
    SUM(ms.n_shares) AS total_shares,
    SUM(ms.n_shares) * sp.price AS total_current_value
FROM my_stocks ms
JOIN stock_prices sp ON ms.symbol = sp.symbol
GROUP BY ms.symbol, sp.price
HAVING COUNT(*) >= 2
ORDER BY ms.symbol;

CREATE VIEW stocks_i_like AS
SELECT
    ms.symbol,
    SUM(ms.n_shares) AS total_shares,
    SUM(ms.n_shares) * sp.price AS total_current_value
FROM my_stocks ms
JOIN stock_prices sp ON ms.symbol = sp.symbol
GROUP BY ms.symbol, sp.price
HAVING COUNT(*) >= 2;

SELECT * FROM stocks_i_like;
