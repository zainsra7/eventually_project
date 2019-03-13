import datetime
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventually_project.settings')
django.setup()

from django.contrib.auth.models import User
from eventually.models import UserProfile, Event, Attendee, Tag


def populate():
    users = [{
        'username': 'Zain',
        'email': '2418596U@student.gla.ac.uk',
        'password': 'Zain12345',
    },{
        'username': 'Smriti',
        'email': '2418004K@student.gla.ac.uk',
        'password': 'Smriti12345',
    },
	{
        'username': 'Sam',
        'email': '2370844A@student.gla.ac.uk',
        'password': 'Sam12345',
    },
	{
        'username': 'Yasser',
        'email': '2420419O@student.gla.ac.uk',
        'password': 'Yasser12345',
    },
	{
        'username': 'Norah',
        'email': '2363680A@student.gla.ac.uk',
        'password': 'Norah12345',
    },]

    events = [{
        'title': 'DUELLING PIANOS',
        'description': 'Enjoy an arrival drink at 7:30pm and then take your seats to enjoy a delicious two course meal at 8:00pm whilst the show begins.. Be prepared for two hours of live music, sing - alongs aswell as pure comedy mixed into this fantastic evening with our two well known home grown talents John Rankin (Glasgows piano man) and the fabulous Stevie Devine! Watch the two battle it out on the keys as fellow musician Michelle Elii hosts the night and makes sure the evening delivers all round good craic',
        'location': 'G11PA',
        'address': '62 Albion Street , Glasgow',
        'capacity': '30',
        'host': users[0]["username"],
    },{
        'title': 'Offer Holders Day - 26 March 2019',
        'description': 'If you are considering accepting your offer to study with us at the University of Glasgow, we would be delighted to welcome you and your family along to our undergraduate Offer Holders’ Day on Tuesday 26 March 2019. Our 2019 Offer Holders’ Day will run between 9.30am and 3.00pm with talks, tours and activities scheduled within these times. You can come and go as you please, and check out everything which interests you. This is the perfect opportunity for undergraduate offer holders to get more detailed information about your chosen courses, speak to academic and services staff, meet current students and see our great facilities. This will also allow you to explore our amazing city, and experience what student life is like at Glasgow!',
        'location': 'G128QQ',
        'address': 'University Avenue,Glasgow',
        'capacity': '100',
        'host': users[0]["username"],
    },{
        'title': 'An Orchestral Rendition of Dr. Dre: 2001 - Glasgow',
        'description': 'This is no ordinary Orchestral event. Expect a full standing crowd, with performances from various DJ’s, lyricists and singers as well as a full Orchestral Rendition of Dr. Dre’s: 2001 album, followed by other of Dre’s west coast classics. This is the combination of a traditional Orchestra merging with a modern live hip-hop music event.',
        'location': 'G38QG',
        'address': '100 Eastvale Place,Glasgow',
        'capacity': '50',
        'host': users[1]["username"],
    },{
        'title': 'The Greatest Showman Singalong Club Tour - GLASGOW',
        'description': 'The Greatest singalong clubnight of all time.',
        'location': 'G59NT',
        'address': '121 Eglinton Street,Glasgow',
        'capacity': '50',
        'host': users[1]["username"],

    },{
        'title': 'Rewind To The 90s-Glasgow Quay',
        'description': 'Rewind To The Nineties for this one off spectacular with live performances from 90s sensations B*Witched, S Club and Ultrabeat Doors open at 5:30pm with a line up of your favorite acts but not forgetting about Bonkers Bingo to start your night with a bang. We dont bring the party, we are the party!',
        'location': 'G58NP',
        'address': 'Springfield Quay,Paisley Road ,Glasgow',
        'capacity': '150',
        'host': users[2]["username"],
    },{
        'title': 'GLASGOW COFFEE FESTIVAL 2019',
        'description': 'Year five and Scotland biggest coffee party is go! Dear Green are bringing back the Glasgow Coffee Festival to showcase Scotlands speciality coffee culture in a two day event. Saturday 4th - Sunday 5th May 2019 at The Briggait, Glasgow.',
        'location': 'G15HZ',
        'address': '141 Bridgegate,Glasgow',
        'capacity': '50',
        'host': users[2]["username"],
    },{
        'title': 'Global Azure Bootcamp 2019 - Glasgow',
        'description': 'All around the world user groups and communities want to learn about Azure and Cloud Computing! The Glasgow Azure User Group is pleased to host the second Global Azure Bootcamp event in Glasgow and join the other communities for a full day event of Azure related sessions.',
        'location': 'G11RE',
        'address': 'Collabor8te,22 Montrose Street,Glasgow',
        'capacity': '80',
        'host': users[3]["username"],

    },{
        'title': 'PLAY Expo Glasgow 2019',
        'description': 'Scotlands favourite celebration of gaming is returning in June 2019 for its fourth year.Play Expo Glasgow features a whole host of video gaming-related treats ',
        'location': 'G514BN',
        'address': 'intu Braehead Arena,Kings Inch Rd,Glasgow',
        'capacity': '100',
        'host': users[3]["username"],
    },{
        'title': 'Winner Stays On - Retro Console Gaming Event',
        'description': 'There’s very little in life more satisfying than beating a loved one or friend senseless at a video game. How about doing just that with a drink in your hand! Winner Stays On is Glasgow’s newest local multiplayer gaming night. There’s a big a focus on retro games so you will be able to finally figure out who amongst you is the king of Street Fighter. With consoles ranging from the 8-bit era right up to modern day it’s a fireball of nostalgia straight to the face.',
        'location': 'G412AB',
        'address': '657 - 659 Pollokshaws Road,Glasgow',
        'capacity': '50',
        'host': users[4]["username"],
    },{
        'title': 'Glasgow Photography Workshop for Beginners',
        'description': '',
        'location': 'City Centre,Glasgow',
        'address': 'G23DZ',
        'capacity': '85',
        'host': users[4]["username"],

    },]

    tags = [
        {
            'tag': 'ThingsToDoInGlasgow',
            'event': events[0]["title"],
        },
        {
            'tag': 'Performances',
            'event': events[0]["title"],
        },
        {
            'tag': 'Music',
            'event': events[0]["title"],
        },
        {
            'tag': 'ThingsToDoInGlasgow',
            'event': events[1]["title"],
        },
        {
            'tag': 'Conventions',
            'event': events[1]["title"],
        },
        {
            'tag': 'FamilyAndEducation',
            'event': events[1]["title"],
        },
		{
            'tag': 'ThingsToDoInGlasgow',
            'event': events[2]["title"],
        },
        {
            'tag': 'Performances',
            'event': events[2]["title"],
        },
        {
            'tag': 'Music',
            'event': events[2]["title"],
        },
		{
            'tag': 'ThingsToDoInGlasgow',
            'event': events[3]["title"],
        },
        {
            'tag': 'Party',
            'event': events[3]["title"],
        },
		{
            'tag': 'FilmAndMedia',
            'event': events[3]["title"],
        },
        {
            'tag': 'Music',
            'event': events[3]["title"],
        },
        {
            'tag': 'ThingsToDoInGlasgow',
            'event': events[4]["title"],
        },
		{
            'tag': 'Party',
            'event': events[4]["title"],
        },
        {
            'tag': 'Festivals',
            'event': events[4]["title"],
        },
		{
            'tag': 'Music',
            'event': events[4]["title"],
        },
		{
            'tag': 'ThingsToDoInGlasgow',
            'event': events[5]["title"],
        },
        {
            'tag': 'Party',
            'event': events[5]["title"],
        },
        {
            'tag': 'Festivals',
            'event': events[5]["title"],
        },
		{
            'tag': 'FoodAndDrink',
            'event': events[5]["title"],
        },
        {
            'tag': 'ThingsToDoInGlasgow',
            'event': events[6]["title"],
        },
        {
            'tag': 'Networking',
            'event': events[6]["title"],
        },
		{
            'tag': 'Course',
            'event': events[6]["title"],
        },
		{
            'tag': ' ScienceANdTech',
            'event': events[6]["title"],
        },
		 {
            'tag': 'ThingsToDoInGlasgow',
            'event': events[7]["title"],
        },
        {
            'tag': 'Games',
            'event': events[7]["title"],
        },
		{
            'tag': ' ScienceANdTech',
            'event': events[7]["title"],
        },
		{
            'tag': ' Hobbies',
            'event': events[7]["title"],
        },
		{
            'tag': 'FilmAndMedia',
            'event': events[8]["title"],
        },
		{
            'tag': 'ThingsToDoInGlasgow',
            'event': events[8]["title"],
        },
        {
            'tag': 'Games',
            'event': events[8]["title"],
        },
		{
            'tag': 'Hobbies',
            'event': events[9]["title"],
        },
		{
            'tag': 'ThingsToDoInGlasgow',
            'event': events[9]["title"],
        },
        {
            'tag': 'Course',
            'event': events[9]["title"],
        },
    ]

    attendees = [
        {
            'user': users[0]["username"],
            'event':  events[0]["title"],
        },
        {
            'user': users[0]["username"],
            'event': events[1]["title"],
        },
		 {
            'user': users[0]["username"],
            'event': events[3]["title"],
        },
		{
            'user': users[0]["username"],
            'event': events[5]["title"],
        },
		{
            'user': users[0]["username"],
            'event': events[7]["title"],
        },
		{
            'user': users[0]["username"],
            'event': events[9]["title"],
        },
        {
            'user': users[1]["username"],
            'event': events[2]["title"],
        },
        {
            'user': users[1]["username"],
            'event': events[3]["title"],
        },
		{
            'user': users[1]["username"],
            'event': events[4]["title"],
        },
		{
            'user': users[1]["username"],
            'event': events[6]["title"],
        },
		{
            'user': users[1]["username"],
            'event': events[8]["title"],
        },
        {
            'user': users[2]["username"],
            'event': events[4]["title"],
        },
        {
            'user': users[2]["username"],
            'event': events[5]["title"],
        },
		 {
            'user': users[2]["username"],
            'event': events[7]["title"],
        },
		 {
            'user': users[2]["username"],
            'event': events[9]["title"],
        },
		 {
            'user': users[2]["username"],
            'event': events[1]["title"],
        },
		{
            'user': users[3]["username"],
            'event': events[6]["title"],
        },
        {
            'user': users[3]["username"],
            'event': events[7]["title"],
        },
		 {
            'user': users[3]["username"],
            'event': events[8]["title"],
        },
		 {
            'user': users[3]["username"],
            'event': events[4]["title"],
        },
		{
            'user': users[4]["username"],
            'event': events[8]["title"],
        },
        {
            'user': users[4]["username"],
            'event': events[9]["title"],
        },
		{
            'user': users[4]["username"],
            'event': events[6]["title"],
        },
		{
            'user': users[4]["username"],
            'event': events[2]["title"],
        },
    ]

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