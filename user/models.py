from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from main.models import Catalog
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ebooks = models.ManyToManyField(Catalog, blank=True)

    def __str__(self):
        return self.user

    def get_ebooks_id(self):
        result = []
        for ebook in self.ebooks.all():
            result.append(ebook.id)
        return result


def post_save_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


post_save.connect(post_save_profile_create, sender=User)
