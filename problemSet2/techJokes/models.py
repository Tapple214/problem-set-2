from django.db import models


class Joke(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['text', 'author', 'category'],
                name='unique_joke_text_author_category',
            ),
        ]

    @property
    def display_category(self):
        return self.category.strip() or 'Uncategorized'

    def __str__(self):
        return f'{self.text[:50]} — {self.author}'


# Q6: my_stocks
class MyStock(models.Model):
    symbol = models.CharField(max_length=20)
    n_shares = models.IntegerField()
    date_acquired = models.DateField()

    class Meta:
        db_table = 'my_stocks'

    def __str__(self):
        return f'{self.symbol} ({self.n_shares} shares)'


# Q7 Part A: stock_prices
class StockPrice(models.Model):
    symbol = models.CharField(max_length=20, primary_key=True)
    quote_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        db_table = 'stock_prices'

    def __str__(self):
        return f'{self.symbol} @ {self.price}'


# Q7 Part B: newly_acquired_stocks
class NewlyAcquiredStock(models.Model):
    symbol = models.CharField(max_length=20)
    n_shares = models.IntegerField()
    date_acquired = models.DateField()

    class Meta:
        db_table = 'newly_acquired_stocks'

    def __str__(self):
        return f'{self.symbol} ({self.n_shares} shares)'
