from django.shortcuts import render

# Create your views here.
def index(request):
    context={
        'judul' : 'Login',
    }
    return render(request, "login.html", context)

def register(request):
    context={
        'judul' : 'Register',
    }
    return render(request, "register.html", context)