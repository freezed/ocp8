from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    visitor = 'world'
    if request.user.is_authenticated:
        visitor = request.user.username

    return render(request, 'home.html', {
        'visitor':visitor,
        'context':'account app index',
    })
