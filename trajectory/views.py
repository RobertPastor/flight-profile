from django.shortcuts import render
from django.template import loader
from django.core import serializers
from django.http import HttpResponse

#from trajectory.models import SiteMessage


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

def index(request):
    # create a function
    # create a dictionary to pass
    # data to the template
    context ={}
    # return response with template and context
    return render(request, "index.html", context)