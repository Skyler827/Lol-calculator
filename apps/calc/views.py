from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "calc/base.html")
def initializedb(request):
    pass