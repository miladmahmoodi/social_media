from django.db import models
from django.contrib.auth.models import User as UserModel


class Relation(models.Model):
    from_user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='following'
    )
    to_user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.from_user} following {self.to_user}'


class Profile(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
    )
    age = models.PositiveSmallIntegerField(
        default=0,
    )
    bio = models.TextField(
        null=True,
        blank=True,
    )
    address = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.user}'
