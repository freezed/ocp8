from django.shortcuts import render

def index(request):
    return render(request, 'ersatz/home.html')

def search(request):
    msg = 'GET request content : '
    for key, val in request.GET.items():
        msg += "\n{}:{},".format(key, val)

    return HttpResponse(msg)
