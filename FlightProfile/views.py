
# import Http Response from django
from django.shortcuts import render


def index(request):
    # create a function
    # create a dictionary to pass
    # data to the template
    context ={}
    # return response with template and context
    #return render(request, "index-og.html", context)
    return render(request, "index-maplibre.html", context)