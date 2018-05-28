from django.contrib import admin
from .models import Coin
# Register your models here.


class CoinAdmin(admin.ModelAdmin):
    pass


admin.site.register(Coin, CoinAdmin)