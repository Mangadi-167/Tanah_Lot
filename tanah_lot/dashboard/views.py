from django.shortcuts import render


def index(request):
    context={
        'judul':'Data Content',
    }
    return render(request,"article/data.html", context)