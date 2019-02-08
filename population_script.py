import datetime
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventually_project.settings')
django.setup()

from django.contrib.auth.models import User
from eventually.models import UserProfile, Event, Attendee, Tag


def populate():
    users = [{
        'username': 'Test1',
        #'fullname': 'Test1',
        'email': 'test1@gmail.com',
        'password': 'test11234',
    },{
        'username': 'Test2',
        #'fullname': 'Test2',
        'email': 'test2@gmail.com',
        'password': 'test21234',
    },{
        'username': 'Test3',
        #'fullname': 'Test3',
        'email': 'test3@gmail.com',
        'password': 'test31234',
    },]

    events = [{
        'title': 'Event1',
        'description': 'This is for UOG Club',
        'location': '',
        'address': '',
        'capacity': '200',
        'host': users[0]["username"],
    },{
        'title': 'Event2',
        'description': 'This is for SAWB',
        'location': '',
        'address': '',
        'capacity': '100',
        'host': users[0]["username"],
    },{
        'title': 'Event3',
        'description': 'This is for POSTGRAD',
        'location': '',
        'address': '',
        'capacity': '50',
        'host': users[1]["username"],
    },{
        'title': 'Event4',
        'description': '',
        'location': '',
        'address': '',
        'capacity': '4',
        'host': users[2]["username"],

    },{
        'title': 'Event5',
        'description': '',
        'location': '',
        'address': '',
        'capacity': '',
        'host': users[2]["username"],
    },]

    tags = [
        {
            'tag': 'T',
            'event': events[0]["title"],
        },
        {
            'tag': 'T',
            'event': events[1]["title"],
        },
        {
            'tag': 'B',
            'event': events[0]["title"],
        },
        {
            'tag': 'B',
            'event': events[3]["title"],
        },
        {
            'tag': 'C',
            'event': events[1]["title"],
        },
        {
            'tag': 'P',
            'event': events[4]["title"],
        },
        {
            'tag': 'Q',
            'event': events[4]["title"],
        },
        {
            'tag': 'L',
            'event': events[2]["title"],
        },
        {
            'tag': 'L',
            'event': events[3]["title"],
        },
    ]

    attendees = [
        {
            'user': users[0]["username"],
            'event':  events[1]["title"],
        },
        {
            'user': users[0]["username"],
            'event': events[3]["title"],
        },
        {
            'user': users[1]["username"],
            'event': events[0]["title"],
        },
        {
            'user': users[1]["username"],
            'event': events[2]["title"],
        },
        {
            'user': users[2]["username"],
            'event': events[0]["title"],
        },
        {
            'user': users[2]["username"],
            'event': events[4]["title"],
        },
    ]

    # Create Users
    #for user in users:
        #add_user_profile(user)

    # Create Events
    #for event in events:
        #add_event(event)

    # Create Tags
    for tag in tags:
        add_tag(tag)

    # Create Attendees
    for attendee in attendees:
        event = Event.objects.get_or_create(title=attendee["event"])[0]
        user = UserProfile.objects.get_or_create(username=attendee["user"])[0]
        add_attendee(event, user)


def add_event(event):
    u = User.objects.get(username=event["host"])
    up = UserProfile.objects.get_or_create(user=u)[0]
    e = Event.objects.get_or_create(title=event["title"], host=up, date=datetime.datetime.now())[0]
    e.save()
    return e


def add_user_profile(user):
    u = User.objects.create_user(username=user["username"], email=user["email"], password=user["password"])
    u.save()
    user_profile = UserProfile.objects.get_or_create(user=u)[0]
    user_profile.save()
    return user_profile


def add_tag(tag):
    event = Event.objects.get_or_create(title=tag["event"])[0]
    t = Tag.objects.get_or_create(tag=tag["tag"], event=event)[0]
    t.save()
    return t


def add_attendee(event, user):
    a = Attendee.objects.get_or_create(event=event, user=user)[0]
    a.save()
    return a


if __name__ == '__main__':
    print("Starting eventually population script...")
    populate()