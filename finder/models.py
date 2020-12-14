'''***************************************************************************************
*  Title: Python Django Tutorial: Full-Featured Web App Part 9 - Update User Profile
*  Author: Corey Schafer
*  Date: 2/18/19
*  URL_1: https://www.youtube.com/watch?v=CQ90L5jfldw&t
*  URL_2: https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog
*  Software License: MIT

*  Title: Python Django Tutorial: Full-Featured Web App Part 8 - User Profile and Picture
*  Author: Corey Schafer
*  Date: 2/18/19
*  URL_1: https://www.youtube.com/watch?v=FdVuKt_iuSI&t
*  URL_2: https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog
*  Software License: MIT
***************************************************************************************'''

from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
from .data import LIST_MAJORS, GRADUATION_YEARS, LIST_GENDERS



# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
        
class ProfileManager(models.Manager):
    def create_profile(self, user, name='', image='', phone='', major='', minor='', graduation='', gender='', age='', zoom_link=''):
        user_created = self.create(user=user, name=name, image=image, phone=phone, major=major, minor=minor, graduation=graduation, gender=gender, age=age, zoom_link=zoom_link)
        return user_created


class Group(models.Model):
    group_name = models.CharField(max_length=255, default='',null=True)
    group_zoom_link = models.CharField(max_length=255, default='',null=True)
    members = models.ForeignKey("Profile", related_name="members", on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return f'{self.group_name}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    phone = PhoneField(default='', blank=True, null=True)
    major = models.CharField(max_length=255, choices=LIST_MAJORS, default='', null=True)
    minor = models.CharField(max_length=255, choices=LIST_MAJORS, default='', null=True, blank=True)
    graduation = models.CharField(max_length=255, choices=GRADUATION_YEARS, default='',null=True )
    gender = models.CharField(max_length=255, choices=LIST_GENDERS, default='', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    friends = models.ManyToManyField("Profile", blank=True)

    group = models.CharField(max_length=255, default='', null=True)
    group_leader = False
    group_valid = True
    group_zoom_link = models.URLField(max_length=255, default='', null=True)
    group_members = models.ForeignKey(User, related_name="group_members", on_delete=models.CASCADE, blank=True, null=True)
    # group = models.ForeignKey("Group", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'

class FriendRequest(models.Model):
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From {self.from_user.username}, to {self.to_user.username}'

class GroupRequest(models.Model):
    to_user = models.ForeignKey(User, related_name='group_to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='group_from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Group request from {self.from_user.username}, to {self.to_user.username}'