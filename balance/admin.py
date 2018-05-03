from django.contrib import admin
from .models import Wallet, Transfers


# Register your models here.
class WalletAdmin(admin.ModelAdmin):
    pass


admin.site.register(Wallet, WalletAdmin)


class TransferAdmin(admin.ModelAdmin):
    pass


admin.site.register(Transfers, TransferAdmin)