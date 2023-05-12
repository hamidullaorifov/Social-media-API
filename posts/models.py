from django.db import models
from taggit.managers import TaggableManager
from users.models import User
from datetime import datetime
# Create your models here.


class Post(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='liked_posts')
    tags = TaggableManager()
    class Meta:
        ordering = ('-created','-updated')

    
    @property
    def likes_count(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    text = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
