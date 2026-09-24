# AI Usage Disclosure

## Tool used

- Cursor (Composer AI assistant)

## Where AI was used

### 1. Joke seed data (`problemSet2/techJokes/fixtures/seed_jokes.json`)

The assignment provides three example jokes. AI helped draft the additional jokes in the fixture so the app has enough records to demonstrate pagination (at least two pages).

### 2. SQL scripts (`sql/ps2_sql_transcript.sql`)

AI helped draft the PostgreSQL commands for Q6–Q12, including:

- Q6–Q7: stock table setup, data load, and copy queries
- Q8–Q9: inner join and left outer join reports
- Q10: `stock_value()` and `portfolio_value()` PL/pgSQL functions
- Q11: buy-more-winners insert and GROUP BY / HAVING reports
- Q12: `stocks_i_like` view

Note: Q6–Q7 table creation is also handled by Django models/migrations (`MyStock`, `StockPrice`, `NewlyAcquiredStock`). The SQL transcript is kept for the assignment’s required PostgreSQL session record and for running Q8–Q12 queries in `psql`.

## How the output was verified

### Seed data

- Loaded the fixture with `python manage.py loaddata seed_jokes`.
- Opened `/jokes/` and confirmed jokes appear grouped by category.
- Checked that pagination works with the seeded record count.

### SQL scripts

- Reviewed each query against the Problem Set 2 requirements (Q6–Q12).
- Ran commands in `psql` against the `problemSet2` database and compared results to the expected outputs in the transcript.
- Confirmed PL/pgSQL functions return expected values (e.g. `SELECT stock_value('IBM');` returns 216).
