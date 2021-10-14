from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=CASCADE)

    def get_absolute_url(self): # especificamos la ruta a cada post ('post-detail/3')
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.title} by {self.author}'
