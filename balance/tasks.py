from django.contrib.auth.models import User
from .models import Wallet, Transfers
from celery import shared_task


@shared_task
def transfer_money_between_wallets(from_wallet, to_wallet, amount):
    if from_wallet.balance - from_wallet.escrow >= amount:
        Transfers(
            from_wallet=from_wallet.id, 
            to_wallet=to_wallet.id, 
            amount=amount,
            status='A'
        ).save()

        return True
    
    Transfers(
        from_wallet=from_wallet.id, 
        to_wallet=to_wallet.id, 
        amount=amount,
        status='C'
    ).save()
    
    return False
