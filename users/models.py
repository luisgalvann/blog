from django.db import models
from django.contrib.auth.models import User


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='unknown.jpeg', upload_to='avatar_img')

    def __str__(self):
        return f'Avatar ({self.user.username})'
