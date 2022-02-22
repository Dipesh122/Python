from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=100)
    budget = models.BigIntegerField(blank=True, null=True)
    genres = models.TextField(blank=True, null=True)
    favorite = models.ManyToManyField(User, related_name='favorite')

    def __str__(self):
        return self.title

class Review(models.Model):
    review = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name= 'movie')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user'
    )
    
    
