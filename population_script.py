import datetime
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventually_project.settings')
django.setup()

from django.contrib.auth.models import User


from eventually.models import  UserProfile, Event, Attendee, Tag


def populate():
    # Creating Users
    users = [{
        'username' : 'Test1',
        'fullname' : 'Test1',
        'email' : 'test1@gmail.com',
        'password' : 'test11234',
    },{
        'username' : 'Test2',
        'fullname' : 'Test2',
        'email' : 'test2@gmail.com',
        'password' : 'test21234',
    },{
        'username' : 'Test3',
        'fullname' : 'Test3',
        'email' : 'test3@gmail.com',
        'password' : 'test31234',
    },]

    for user in users:
        u = User.objects.create_user(username=user["username"], email=user["email"], password=user["password"])
        UserProfile.objects.get_or_create(user=u, fullname=user["fullname"])

    events = [{
        'title' : 'Event1',
        'description' : 'This is for UOG Club',
        'location': '',
        'address' : '',
        'capacity' : '200',
        'created_by' : users[0]["fullname"],
    },{
        'title' : 'Event2',
        'description' : 'This is for SAWB',
        'location': '',
        'address' : '',
        'capacity' : '100',
        'created_by' : users[0]["fullname"],
    },{
        'title' : 'Event3',
        'description' : 'This is for POSTGRAD',
        'location': '',
        'address' : '',
        'capacity' : '50',
        'created_by' : users[1]["fullname"],
    },{
        'title' : 'Event4',
        'description' : '',
        'location': '',
        'address' : '',
        'capacity' : '4',
        'created_by' : users[2]["fullname"],

    },{
        'title' : 'Event5',
        'description' : '',
        'location': '',
        'address' : '',
        'capacity' : '',
        'created_by' : users[2]["fullname"],
    },]

    # Create Events
    for e in events:
        add_event(e)


def add_event(event):
    u = UserProfile.objects.get_or_create(fullname=event["created_by"])[0]
    print(u)
    e = Event.objects.get_or_create(title=event["title"], created_by=u, date=datetime.datetime.now())[0]
    e.save()
    return e


if __name__ == '__main__':
    print("Starting eventually population script...")
    populate()