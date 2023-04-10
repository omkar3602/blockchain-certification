from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

# Create your views here.
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        next_url = data['next_url']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url == '':
                return redirect('home')
            else:
                return redirect(next_url)
        else:
            messages.error(request, "Couldn't Login. Please check your credentials.")
    return render(request, 'login.html')

def logout_user(request):
    if request.method == 'POST' and request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('home')
    if not request.user.is_authenticated:
        return redirect('home')
    return redirect('home') 