from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from omega.forms import SignInForm

def index(request):
    return render(request, 'omega/home.html')

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect(request.GET['next'])
    else:
        form = SignInForm()
    return render(request, 'registration/signin.html', {'form': form})
