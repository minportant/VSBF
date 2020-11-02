from django.db import models
from django.contrib.auth.models import User
from PIL import Image
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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True, blank=True)
    phone = PhoneField(default='', blank=True, null=True)
    major = models.CharField(max_length=255, choices=LIST_MAJORS, default='', null=True)
    minor = models.CharField(max_length=255, choices=LIST_MAJORS, default='', null=True, blank=True)
    graduation = models.CharField(max_length=255, choices=GRADUATION_YEARS, default='',null=True )
    gender = models.CharField(max_length=255, choices=LIST_GENDERS, default='', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    zoom_link = models.URLField(max_length=255, default='', null=True, blank=True)
    friends = models.ManyToManyField("Profile", blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class FriendRequest(models.Model):
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From {self.from_user.username}, to {self.to_user.username}'