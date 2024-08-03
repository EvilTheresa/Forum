from django.contrib.auth import get_user_model

from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')

    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'