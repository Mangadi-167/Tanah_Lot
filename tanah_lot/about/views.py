from django.shortcuts import render


# Create your views here.
# def index (request):
#     return render(request, "news/index.html")

def index(request):
    context={
        'judul':'About | History',
    }
    return render(request,"history.html", context)

def facilities(request):
    context={
        'judul':'About | Facilities',
    }
    return render(request,"facilities.html", context)

def tickets(request):
    context={
        'judul':'About | Tickets',
    }
    return render(request,"tickets.html", context)

def sitemaps(request):
    context={
        'judul':'About | Site Map',
    }
    return render(request,"sitemaps.html", context)