from django.http import HttpResponse

# import Http Response from django
from django.shortcuts import render

def indexOld(request):
    return HttpResponse("Hello, world. You're at the FlightProfile index.")


def index(request):
    # create a function
    # create a dictionary to pass
    # data to the template
    context ={}
    # return response with template and context
    return render(request, "index.html", context)