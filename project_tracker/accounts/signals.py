from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings
from .models import Profile

def ensure_groups():
    for g in ("Admin", "Project Manager", "Developer"):
        Group.objects.get_or_create(name=g)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        ensure_groups()
        profile = Profile.objects.create(user=instance, role='DEV')
        dev_group = Group.objects.get(name="Developer")
        instance.groups.add(dev_group)
