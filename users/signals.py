from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from dashboard.models import Wallet, CoinTransaction

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        wallet, wallet_created = Wallet.objects.get_or_create(
            user=instance,
            defaults={"balance": 100},
        )

        if wallet_created:
            CoinTransaction.objects.create(
                user=instance,
                transaction_type="credit",
                amount=100,
                description="Welcome bonus",
            )