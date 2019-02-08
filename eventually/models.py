from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    max_length = 200
    user = models.OneToOneField(User)

    # email = models.CharField(max_length=max_length) # Email is already in the USER object
    ver_code = models.CharField(max_length=max_length - 194)
    profile_pic = models.ImageField(upload_to='profile_images', blank=True)
    approved = models.BooleanField(default=False)
    fullname = models.CharField(max_length=max_length)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    max_length = 200

    title = models.CharField(max_length=max_length)
    description = models.CharField(max_length=max_length * 5)
    image = models.ImageField(upload_to='event_images', blank=True)
    location = models.CharField(max_length=max_length * 3) # GPS Coordinates
    address = models.CharField(max_length=max_length * 5) # Actual Address
    date = models.DateField(auto_now=False)
    capacity = models.IntegerField(default=0)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Attendee(models.Model):

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event', 'user')
        verbose_name_plural = 'Attendees'

    def __str__(self):
        return self.user_id.username + " -> " + self.event_id.title


class Tag(models.Model):
    max_length = 200
    name = models.CharField(max_length=max_length)
    event = models.ManyToManyField(Event)

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.event_id.title + " has tag: " + self.name

