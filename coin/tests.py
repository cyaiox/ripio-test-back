from django.test import TestCase
from .models import Coin


class CoinTest(TestCase):

    def setUp(self):
        self.c = Coin.objects.create(
            name='Test Coin', description='Is a test coin', symbol='TC')

    def test_coin_creation(self):
        self.assertTrue(isinstance(self.c, Coin))
        self.assertEqual(self.c.__str__(), self.c.name)
