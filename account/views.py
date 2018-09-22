from django.http import HttpResponse

def index(request):
    visitor = 'world'
    if request.user.is_authenticated:
        visitor = request.user.username

    return HttpResponse("Hello, {}. Here's the account app index.".format(visitor))
