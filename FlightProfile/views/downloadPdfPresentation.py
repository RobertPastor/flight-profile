'''
Created on 1 juin 2023

@author: robert
'''
import os

from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse , Http404 
from django.http import JsonResponse


@csrf_protect
def downloadPdfPresentation(request):
    pass
    if request.method == 'GET':
        
        fileName = 'AirlineServicesPresentation.pdf'
        #fileName = fileName + '-{0}.pdf'.format(datetime.now().strftime("%d-%b-%Y-%Hh%Mm%S"))
        filePath = os.path.join( os.path.dirname(__file__) , fileName)
        #print ( filePath )
        if os.path.exists(filePath):
            
            with open(filePath, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'attachment; filename=' + (fileName)
                return response
        
        else:
            raise Http404
    else:
        response_data = { 'errors' : 'expecting a GET - received something else = {0}'.format(request.method) }
        return JsonResponse(response_data)