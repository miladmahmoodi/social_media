from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User as UserModel

from .models import Profile as ProfileModel


@receiver(signals.post_save, sender=UserModel)
def create_profile(sender, **kwargs):
    signal_created = kwargs['created']
    user = kwargs['instance']

    if signal_created:
        ProfileModel.objects.create(
            user=user,
        )
