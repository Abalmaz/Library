from .models import User, Invitation
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        if instance.is_publisher:
            Invitation.objects.create(username=instance.username, email=instance.email)


@receiver(post_save, sender=Invitation)
def send_mail(sender, instance=None, created=False, **kwargs):
    if created:
        instance.send()