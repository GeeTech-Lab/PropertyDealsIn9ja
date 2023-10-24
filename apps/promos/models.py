from datetime import timedelta

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from apps.accounts.models import User
from apps.agents.models import Agent
from propertyDealsIn9ja.settings import AUTH_USER_MODEL


class Promo(models.Model):

    PROMO_TYPE_CHOICES = (
        ("basic", "Basic"),
        ("premium", "Premium"),
        ("enterprise", "Enterprise"),
    )

    promo_for = models.OneToOneField("accounts.User", on_delete=models.CASCADE, related_name="my_promo")
    promo_type = models.CharField(max_length=20, choices=PROMO_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    promo_duration = models.PositiveIntegerField(default=30)  # Default promo duration in days
    promo_start_date = models.DateTimeField(blank=True, null=True)
    promo_end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_promo_for_display()} - {self.get_promo_type_display()}"

    def calculate_remaining_duration(self):
        current_time = timezone.now()
        if current_time < self.promo_end_date:
            remaining_duration = (self.promo_end_date - current_time).days
            if remaining_duration < 0:
                remaining_duration = 0
            self.promo_duration = remaining_duration
            self.save()


@receiver(post_save, sender=Agent)
def create_promo_for_new_user(sender, instance, created, **kwargs):
    if created:
        promo_type = "enterprise" if instance.business_user.is_staff else "premium"
        # Create the promo instance
        promo = Promo(
            promo_for=instance.business_user,
            promo_type=promo_type,
            description=f"Promo for {instance.business_user.username}",
            is_active=True
        )
        promo.promo_start_date = timezone.now() if promo.is_active else None
        promo.promo_duration = 360 if promo_type == 'enterprise' else (180 if promo_type == 'premium' else 30)
        promo.promo_end_date = promo.promo_start_date + timedelta(days=promo.promo_duration)
        promo.save()
