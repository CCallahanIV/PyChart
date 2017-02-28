from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class PyChartProfile(models.Model):
    """Define a Pychart Profile."""

    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE
    )

    objects = models.Manager()

    def __str__(self):
        """Return string representation of profile."""
        return self.user.username


@receiver(post_save, sender=User)
def make_profile(sender, instance, **kwargs):
    """Make a new profile for a new user after new user is saved."""
    if kwargs["created"]:
        new_profile = PyChartProfile(user=instance)
        new_profile.save()
