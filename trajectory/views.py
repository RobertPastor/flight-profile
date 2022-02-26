from django.shortcuts import render
from django.template import loader
from django.core import serializers
from django.http import HttpResponse

#from trajectory.models import SiteMessage


def index(request):
    return HttpResponse("Hello, world. You're at the trajectory index.")

# Create your views here.
def indexTrajectory(request):
    # return HttpResponse('Hello from Python!')
    template = loader.get_template('./index.html')

    siteMessages = []
    '''    for siteMessage in SiteMessage.objects.all().order_by("event_date"):
        if siteMessage.active == True:
            siteMessages.append(siteMessage)
    '''            
    siteMessages = serializers.serialize('json', siteMessages)
    
    context = {'siteMessages' : siteMessages}
    return HttpResponse(template.render(context, request))