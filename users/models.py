from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    bio = models.CharField(max_length=255,blank=True,null=True)
    profile_picture = models.ImageField(upload_to='images',blank=True,null=True)

    # following = models.ManyToManyField('self')

class UserFollow(models.Model):
    following_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    follower_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')


class BlockUser(models.Model):
    blocked_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blocked_by_users')
    blocked_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blocked_users')

# class BlockUser(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blocked_by')
#     blocked_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blocked_users')
    