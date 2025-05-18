from django.shortcuts import render


# khusus article
def index(request):
    context={
        'judul':'Data Content',
    }
    return render(request,"article/data.html", context)


# khusus users
def user(request):
    context={
        'judul':'Data User',
    }
    return render(request,"users/data.html", context)