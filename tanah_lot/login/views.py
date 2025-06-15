# login/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from dashboard.models import UserProfile
from django.contrib.auth.models import User

def register(request):
    if request.user.is_authenticated:
       
        return redirect('dashboard:dashboard') 

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            
            UserProfile.objects.create(
                user=new_user,
                phone_number=form.cleaned_data.get('phone_number')
            )
            
            messages.success(request, 'Akun berhasil dibuat! Silakan login.')
            return redirect('login:login')
    else:
        form = RegistrationForm()
        
    context = { 'judul': 'Register', 'form': form }
    return render(request, "register.html", context)





def index(request): 
    
    if request.user.is_authenticated:
      
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
               
                return redirect('dashboard:dashboard') 
            else:
                messages.error(request, 'Email atau password salah.')
    else:
        form = LoginForm()

    context = { 'judul': 'Login', 'form': form }
    return render(request, "login.html", context)


def user_logout(request):
    logout(request)
    messages.info(request, 'Anda telah berhasil logout.')
    return redirect('login:login')