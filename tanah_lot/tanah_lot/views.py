from django.shortcuts import render

def index(request):
    context={
        'judul':'Tanah Lot',
    }
    return render(request,"index.html", context)


def calender(request):
    context={
        'judul' : 'Event Calender',
    }
    return render(request, "calender.html", context)


def pakendungan(request):
    context={
        'judul' : 'Pakendungan',
    }
    return render(request, "pakendungan.html", context)

def penataranmadya(request):
    context={
        'judul' : 'Penataran Madya',
    }
    return render(request, "penataranmadya.html", context)