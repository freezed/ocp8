from django.shortcuts import render

def index(request):
    return render(request, 'omega/home.html', {'context':'project index'})
