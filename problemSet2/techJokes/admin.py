from django.contrib import admin

from .models import Joke, MyStock, NewlyAcquiredStock, StockPrice

admin.site.register(Joke)
admin.site.register(MyStock)
admin.site.register(StockPrice)
admin.site.register(NewlyAcquiredStock)
