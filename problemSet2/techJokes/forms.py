from django import forms


# =============================================================================
# Q1: Add-Joke Form
# - Reject empty or whitespace-only joke text and author fields.
# - Optional category field (free text in Q1; replaced by Q2 select + new box).
# =============================================================================


# =============================================================================
# Q2: Joke Category
# - Show existing categories in a select box (distinct values from DB).
# - Provide a separate "New category" text box.
# - If both existing and new category are supplied, raise a validation error.
# - If new category is entered, save that; otherwise use the selected category.
# =============================================================================


# =============================================================================
# Q5: Import Jokes Form
# - Accept the XML export URL of another student's deployed application.
# Extra1 (+1 pt): Secure Remote Import — only http/https on approved host
#   (e.g. web1.cs.ait.ac.th); reject localhost, 127.0.0.1, file://, etc.
# =============================================================================
