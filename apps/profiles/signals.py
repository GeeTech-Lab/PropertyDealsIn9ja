import logging

from django.core.files.storage import default_storage
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from propertyDealsIn9ja.settings import AUTH_USER_MODEL
from propertyDealsIn9ja.utils import get_phone_country
from apps.profiles.models import Profile
import requests
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    # phone = get_phone_country(f"{instance.phone}")
    if created:
        Profile.objects.create(user=instance)
        print("Profile created!")

    if instance.socialaccount_set.exists():
        social_account = instance.socialaccount_set.first()

        # Update profile image, phone, country, state, address, etc.
        image_url = social_account.extra_data.get('picture', '')
        image_filename = f"profile_image_{instance.id}.jpg"  # Or use a dynamic filename

        # Download the image and save it to the profile image field
        response = requests.get(image_url)
        if response.status_code == 200:
            instance.profile.image.save(image_filename, ContentFile(response.content), save=True)
            print("Profile image downloaded and saved!")
            print(social_account.extra_data.get('name', ''))
        instance.full_name = social_account.extra_data.get('name', '')
        # instance.profile.phone = social_account.extra_data.get('phone', '')
        # instance.profile.country = social_account.extra_data.get('country', '')
        # instance.profile.state = social_account.extra_data.get('state', '')
        # instance.profile.address = social_account.extra_data.get('address', '')

        instance.profile.save()
        print("Profile updated!")


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    logger.info(f"{instance}'s profile created")


@receiver(pre_delete, sender=Profile)
def profile_image_delete(sender, instance, **kwargs):
    if instance.image:
        default_storage.delete(instance.image)
