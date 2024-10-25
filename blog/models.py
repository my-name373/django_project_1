from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    info = models.TextField()

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk':self.pk})
