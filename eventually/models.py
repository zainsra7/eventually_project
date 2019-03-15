from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MinLengthValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_pic = models.URLField(blank=True)
    ver_code = models.CharField(max_length=6)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    image = models.URLField(blank=True)
    location = models.CharField(max_length=8, validators=[MinLengthValidator(6, "UK PostCode is 6-8 Characters")])  # PostalCode
    address = models.CharField(max_length=2000)   # Complete Address
    date = models.DateField(default=now, blank=False)
    time = models.TimeField(default=now, blank=True)
    capacity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1, "Number of Attendees must be a positive number!")])
    fb_page = models.CharField(blank=True, max_length=200) #Event FB_Page Name
    host = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    attendees = models.IntegerField(default=0, blank=True)
    
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
    tag = models.CharField(max_length=200)
    event = models.ManyToManyField(Event)

    def __str__(self):
        return self.tag

