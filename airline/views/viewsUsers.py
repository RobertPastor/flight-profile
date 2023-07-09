'''
Created on 9 juil. 2023

@author: robert

track guest users to the web site index page
https://www.youtube.com/watch?v=hm9PcJwgqJg

'''

from airline.models import User
from django.http import  JsonResponse


def viewUsers(request):
    
    usersList = []
    for user in User.objects.all():
        usersList.append({
                    "IpAddress" : user.getUserIpAddress(),
                    "nbConnexions" : user.getNbConnexions(),
                    "firstConnexionUTC" : user.getFirstCnxDateTime(),
                    "lastConnexionUTC" : user.getLastCnxDateTime()
                    })
        
    response_data = {'users': usersList}
    return JsonResponse(response_data)