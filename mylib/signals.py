from django.core.cache import cache

from .models import User, Invitation, Book
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        if instance.is_publisher:
            inv = Invitation.objects.create(user=instance)
            inv.send()


# @receiver(post_save, sender=Book)
# def book_post_save_handler(sender, **kwargs):
#     cache.delete()


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if instance.is_publisher:
#         if created:
#             Publisher.objects.get_or_create(user=instance)
#         else:
#             instance.publisher_profile.save()
