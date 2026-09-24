-- Problem Set 2 — PostgreSQL Session Transcript
-- Link this file once from the main /ps2/ index page.
-- Keep commands and outputs together; label each section by question number.


-- =============================================================================
-- Q6: Load Stock Data from a Text File into PostgreSQL (5 pts)
-- 1. Create plain-text file (tab-separated): symbol, n_shares, date_acquired
-- 2. CREATE TABLE my_stocks (...)
-- 3. Load with \copy (from psql) or COPY
-- 4. SELECT * FROM my_stocks;
-- =============================================================================


-- =============================================================================
-- Q7: Copy Data Between Tables Using SQL (5 pts)
-- Part A — CREATE TABLE stock_prices AS / INSERT ... SELECT distinct symbols
--          from my_stocks with quote_date = CURRENT_DATE, price = 31.415
-- Part B — CREATE TABLE newly_acquired_stocks; INSERT ... SELECT 2–3 rows
--          from my_stocks using a WHERE on date_acquired
-- =============================================================================


-- =============================================================================
-- Q8: JOIN my_stocks and stock_prices (4 pts)
-- Single query: symbol, n_shares, price per share, current value (n_shares * price)
-- =============================================================================


-- =============================================================================
-- Q9: OUTER JOIN and Missing Price Data (4 pts)
-- INSERT a symbol into my_stocks that is not in stock_prices (e.g. 'AIT').
-- Rerun Q8 JOIN — notice missing row.
-- Rewrite with LEFT OUTER JOIN so all my_stocks rows appear; NULL price/value
-- when no matching stock_prices row.
-- =============================================================================


-- =============================================================================
-- Q10: PL/pgSQL Functions and Portfolio Valuation (7 pts)
-- Part A — stock_value(symbol): sum of ASCII values of symbol characters;
--          UPDATE stock_prices SET price = stock_value(symbol);
-- Part B — portfolio_value(): cursor/FOR loop over join; sum n_shares * price
-- =============================================================================


-- =============================================================================
-- Q11: Buy More of the Winners (7 pts)
-- INSERT ... SELECT additional shares for stocks priced above portfolio average.
-- Report A: total shares per symbol (GROUP BY)
-- Report B: total value per symbol (JOIN + GROUP BY)
-- Report C: winners only — symbols with >= 2 purchase blocks (GROUP BY ... HAVING)
-- =============================================================================


-- =============================================================================
-- Q12: Encapsulate the Final Query in a View (3 pts)
-- CREATE VIEW stocks_i_like AS ... (Q11 part C logic)
-- SELECT * FROM stocks_i_like;
-- =============================================================================
