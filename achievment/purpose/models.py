from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, unique=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True, verbose_name='Изображение')
    subscribe_to_user = models.ManyToManyField('auth.User', blank=True, related_name='sub')

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.user.id})










