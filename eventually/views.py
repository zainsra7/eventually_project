from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    #Fetch Popular Events from Database
    events = range(5)
    context_dict = {'events': events, }
    response = render(request, 'eventually/index.html', context=context_dict)
    return response

def dashboard(request):
    return HttpResponse("Dashboard: Showing User's Events + Search bar/Filtering")
    
def search(request):
    return HttpResponse("Search Page showing all events based on search string")
    
def host(request):
    return HttpResponse("Host Event Page to create an event")
    
def event(request):
    return HttpResponse("Event View Page to show a specific event details alongwith Sharing, maps and contacting host")

def profile(request):
    return HttpResponse("Profile page to edit user profile")

def register(request):
    return HttpResponse("Sign Up Page")

def logout(request):
    return HttpResponse("Logout")

def login(request):
    return HttpResponse("Login")

def about(request):
    return HttpResponse("About Us page showing information about Eventually")

def contact(request):
    return HttpResponse("Contact us page showing Team behind Eventually")