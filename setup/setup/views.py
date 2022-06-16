# from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    # return HttpResponse("<h1>This is the home page</h1>")
    context = {}
    return render(request, 'base.html', context)
