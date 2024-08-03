from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        related_name="topics",
        on_delete=models.SET_DEFAULT,
        default=1
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('webapp:topic_detail', kwargs={'pk': self.pk})

class Reply(models.Model):
    topic = models.ForeignKey(Topic, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        related_name="replies",
        on_delete=models.SET_DEFAULT,
        default=1
    )

    def __str__(self):
        return f'Reply by {self.author} on {self.topic.title}'
