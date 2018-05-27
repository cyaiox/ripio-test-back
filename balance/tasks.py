from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from celery import task
from django.conf import settings
from altcoin.celery import app as celery_app
from .models import Wallet, Transfers


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@celery_app.on_after_finalize.connect
def setup_periodic_task(sender, **kwargs):
    sender.add_periodic_task(15.0, process_transactions.s())

@task
def transfer_money_between_wallets(from_wallet, to_wallet, amount):
    try:
        print("Before get wallets")
        from_wallet = Wallet.objects.get(pk=from_wallet)
        to_wallet = Wallet.objects.get(pk=to_wallet)
        amount = int(amount)
        if from_wallet.balance - (from_wallet.escrow + amount) >= 0:
            transfer = Transfers(
                from_wallet=from_wallet,
                to_wallet=to_wallet,
                amount=amount,
                status='W'
            )

            transfer.save()

            cache.set(
                'pending_transactions_%s' % transfer.pk,
                transfer,
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

@task
def process_transactions():
    transactions = cache.keys('pending_transactions*')
    for transaction_key in transactions:
        transaction = cache.get(transaction_key)
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

        cache.delete(transaction_key)
