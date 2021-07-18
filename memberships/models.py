from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class MembershipChoices(models.TextChoices):
    Enterprise = 'ent'
    Professional = 'pro'
    Free = 'free'


class Membership(models.Model):
    title = models.CharField(max_length=25)
    type = models.CharField(
        max_length=4,
        choices=MembershipChoices.choices,
        default=MembershipChoices.Free,
    )
    price = models.IntegerField()
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.type


class UserMembership(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='membership'
    )
    stripe_customer_id = models.CharField(max_length=40)
    stripe_Subscription_id = models.CharField(max_length=40, blank=True)
    active = models.BooleanField(default=True)
    membership = models.ForeignKey(
        Membership, related_name='members', on_delete=models.SET_NULL, null=True
    )

    def __str__(self) -> str:
        return str(self.user)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_usermembership(sender, instance, created, *args, **kwargs):
    if created:
        customer = stripe.Customer.create(
            email=instance.email
        )
        free_membership = Membership.objects.get(type=MembershipChoices.Free)
        UserMembership.objects.create(
            user=instance,
            stripe_customer_id=customer['id'],
            membership=free_membership
        )
