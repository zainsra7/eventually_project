from django.contrib import admin
from eventually.models import UserProfile, Tag, Attendee, Event

admin.site.register(UserProfile)
admin.site.register(Tag)
admin.site.register(Attendee)
admin.site.register(Event)

