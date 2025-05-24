from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth import login, logout
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout


def signup_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username taken...")
                return redirect('accounts:signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email taken...")
                return redirect('accounts:signup')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()
                messages.info(request, "user created...")
                return redirect('accounts:login')
        else:
            messages.info(request, "password not matched...")
            return redirect('accounts:signup')
    else:
        return render(request, 'accounts/signup.html')



def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('tour:main_page')
        else:
            messages.info(request, 'invalid credentials...')
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')





def logout_page(request):
    if request.method == "POST":
        logout(request)
        return redirect('tour:main_page')
