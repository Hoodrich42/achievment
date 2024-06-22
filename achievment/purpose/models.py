from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True, verbose_name='Изображение')
    subscribe_to_user = models.ManyToManyField('auth.User', blank=True, related_name='sub')

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)










