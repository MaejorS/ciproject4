from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Project 4 is going to be so fun and I'm going to learn so much!")
