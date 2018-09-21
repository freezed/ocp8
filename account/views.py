from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. Here's the account app index.")
