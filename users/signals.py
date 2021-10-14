from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Avatar


# cuando un 'user' es guardado se envía este 'signal' (doc django)
@receiver(post_save, sender=User)
def create_avatar(sender, instance, created, **kwargs):
    if created:
        Avatar.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_avatar(sender, instance, **kwargs):
    instance.avatar.save()
