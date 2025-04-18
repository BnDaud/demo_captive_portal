from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class UserProfile(models.Model):
    RegNo = models.CharField(max_length= 100 , blank=False ,unique=True)
    display_pic = models.ImageField(upload_to="images" , blank=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Log_Usage(models.Model):
    profile = models.ForeignKey(UserProfile , on_delete=models.CASCADE , related_name="profile")
    #A user can have more than one ip address becauses it changes with time
    ip_address_used = models.CharField(max_length=50 , blank=False)
    date = models.DateField( auto_now_add=True)
    device_used = models.CharField(max_length=20)
    website_visited = models.URLField(blank=False)

    def __str__(self):
        return self.profile.user.username


