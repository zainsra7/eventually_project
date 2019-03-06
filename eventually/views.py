from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    events = range(5)
    context_dict = {'events': events, }
    response = render(request, 'eventually/index.html', context=context_dict)
    return response

def about(request):
    return HttpResponse("WHY")
