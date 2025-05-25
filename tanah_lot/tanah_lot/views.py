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
        'judul' : 'Pakendungan Temple',
    }
    return render(request, "pakendungan.html", context)

def penataranmadya(request):
    context={
        'judul' : 'Penataran Madya Temple',
    }
    return render(request, "penataranmadya.html", context)

def jrokandang(request):
    context={
        'judul' : 'Jro Kandang Temple'
    }
    return render(request,"jrokandang.html", context)

def njunggaluh(request):
    context={
        'judul' : 'Njung Galuh Temple '
    }
    return render(request,"njunggaluh.html", context)

def batubolong(request):
    context={
        'judul' : 'Batu Bolong Temple '
    }
    return render(request,"batubolong.html", context)

def batumejan(request):
    context={
        'judul' : 'Batu Mejan Temple '
    }
    return render(request,"batumejan.html", context)