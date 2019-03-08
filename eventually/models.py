from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    max_length = 200
    user = models.OneToOneField(User)
    profile_pic = models.ImageField(upload_to='profile_images', blank=True)
    ver_code = models.CharField(max_length=6)
    fullname = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    max_length = 200
    title = models.CharField(max_length=max_length)
    description = models.CharField(max_length=max_length * 5)
    image = models.ImageField(upload_to='event_images', blank=True)
    location = models.CharField(max_length=max_length * 3)  # GPS Coordinates
    address = models.CharField(max_length=max_length * 5)   # Actual Address
    date = models.DateField(auto_now=False)
    capacity = models.IntegerField(default=0)
    host = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Attendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return self.user.user.username + " -> " + self.event.title


class Tag(models.Model):
    max_length = 200
    tag = models.CharField(max_length=max_length)
    event = models.ManyToManyField(Event)

    def __str__(self):
        return self.tag

