from django.db import models


# =============================================================================
# Q1: Web-Enabled Tech Jokes Database
# Store joke text, author/comedian, and an optional category.
# Jokes without a category should display under "Uncategorized".
# Bonus (+0.5): Django adds an implicit `id` primary key via DEFAULT_AUTO_FIELD
#   (BigAutoField); PostgreSQL stores it as BIGSERIAL and auto-increments it.
# =============================================================================


# =============================================================================
# Q2: Joke Category (form behavior lives in forms.py / views.py)
# Existing categories come from distinct DB values; user may pick one OR enter
# a new category, but not both at once.
# =============================================================================


# =============================================================================
# Q5 Extra2 (+1 pt): Database-Level Duplicate Protection
# Enforce uniqueness on (joke text, author, category) with a DB constraint,
# not Python-only checks. Handle duplicate attempts gracefully in views/forms.
# =============================================================================
