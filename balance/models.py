from django.contrib.auth.models import User
from django.db import models
from coin.models import Coin
import datetime


# Create your models here.
class Wallet(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    user = models.ForeignKey(User, related_name='account_user', on_delete=None)
    balance = models.IntegerField()
    escrow = models.IntegerField()
    coin = models.ForeignKey(Coin, related_name='wallet_coin', on_delete=None)

    def __str__(self):
        return self.id

STATUS = (
    ('A', 'APPROVED'),
    ('C', 'CANCELED'),
    ('W', 'WAITING APPROBATION')
)


class Transfers(models.Model):
    id = models.CharField(primary_key=True, max_length=12)
    from_wallet = models.ForeignKey(Wallet, related_name='transfer_from_wallet', on_delete=None)
    to_wallet = models.ForeignKey(Wallet, related_name='transfer_to_wallet', on_delete=None)
    amount = models.IntegerField()
    status = models.CharField(max_length=1, choices=STATUS, default='W')
    date_time = models.DateTimeField(default=datetime.datetime.now)