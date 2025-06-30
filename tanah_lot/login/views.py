# login/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from dashboard.models import UserProfile
from django.contrib.auth.models import User

def register(request):
    if request.user.is_authenticated:
     
        try:
           
            if request.user.profile.role == 'admin':
               
                return redirect('dashboard:dashboard')
            else:
               
                return redirect('/')
        except UserProfile.DoesNotExist:
            
            return redirect('/')
     


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
    
    # --- BAGIAN 1: Pengalihan untuk pengguna yang sudah login ---
    if request.user.is_authenticated:
        # Cek role dari UserProfile yang terhubung dengan user
        # 'hasattr' digunakan untuk keamanan, jika ada user yang belum punya profil
        if hasattr(request.user, 'profile') and request.user.profile.role == 'admin':
            # Jika rolenya 'admin', arahkan ke dashboard
            return redirect('dashboard:dashboard')
        else:
            # Jika rolenya 'pengguna' atau tidak punya profil, arahkan ke halaman utama
            return redirect('/')

    # --- BAGIAN 2: Logika saat login baru ---
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
                
                # Cek lagi role dari UserProfile setelah login berhasil
                if hasattr(user, 'profile') and user.profile.role == 'admin':
                    # Jika rolenya 'admin', arahkan ke dashboard
                    messages.success(request, f'Selamat datang kembali, Admin {user.username}!')
                    return redirect('dashboard:dashboard')
                else:
                    # Jika rolenya 'pengguna', arahkan ke halaman utama
                    messages.success(request, f'Selamat datang, {user.username}!')
                    return redirect('/')
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