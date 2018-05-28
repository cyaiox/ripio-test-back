# Generated by Django 2.0.5 on 2018-05-03 03:49

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coin', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfers',
            fields=[
                ('id', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('status', models.CharField(choices=[('A', 'APPROVED'), ('C', 'CANCELED'), ('W', 'WAITING APPROBATION')], default='W', max_length=1)),
                ('date_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('balance', models.IntegerField()),
                ('escrow', models.IntegerField()),
                ('coin', models.ForeignKey(on_delete=None, related_name='wallet_coin', to='coin.Coin')),
                ('user', models.ForeignKey(on_delete=None, related_name='account_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='transfers',
            name='from_wallet',
            field=models.ForeignKey(on_delete=None, related_name='transfer_from_wallet', to='balance.Wallet'),
        ),
        migrations.AddField(
            model_name='transfers',
            name='to_wallet',
            field=models.ForeignKey(on_delete=None, related_name='transfer_to_wallet', to='balance.Wallet'),
        ),
    ]
