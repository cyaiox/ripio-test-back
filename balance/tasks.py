from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .models import Wallet, Transfers
from celery import shared_task
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@shared_task
def transfer_money_between_wallets(from_wallet, to_wallet, amount):
    try:
        from_wallet = Wallet.objects.get(pk=from_wallet)
        to_wallet = Wallet.objects.get(pk=to_wallet)

        if from_wallet.balance - (from_wallet.escrow + amount) >= 0:
            transfer = Transfers(
                from_wallet=from_wallet,
                to_wallet=to_wallet,
                amount=amount,
                status='W'
            ).save()

            #from_wallet.escrow += amount
            #from_wallet.balance -= amount
            #from_wallet.save()

            cache.set(
                'pending_transactions',
                cache.get('pending_transactions').append(transfer),
                timeout=CACHE_TTL)

            cache.set(from_wallet.pk, from_wallet, timeout=CACHE_TTL)

            return {"data": "success"}

        Transfers(
            from_wallet=from_wallet,
            to_wallet=to_wallet,
            amount=amount,
            status='C'
        ).save()

        return {"error": "404 NOT FUNDS FOUND"}
    except:
        return {"error": "ALIENS! D:"}

def schedule_transactions():
    transactions = cache.get('pending_transactions')
    for transaction in transactions:

        from_wallet = cache.get(transaction.from_wallet.pk)

        if from_wallet.balance - transaction.amount >= 0:
            transaction.status = 'A'
            transaction.save()

            from_wallet.balance -= transaction.amount
            from_wallet.save()

            cache.set(from_wallet.pk, from_wallet, timeout=CACHE_TTL)
        else:
            transaction.status = 'C'
            transaction.save()

    cache.set(
        'pending_transactions',
        cache.get('pending.transactions').remove(transactions),
        timeout=CACHE_TTL)