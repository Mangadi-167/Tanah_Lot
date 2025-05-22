from django.shortcuts import render

# Create your views here.
def index(request):
    context={
        'judul' : 'Login',
    }
    return render(request, "login.html", context)