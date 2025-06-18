from django.shortcuts import render, get_object_or_404 

from dashboard.models import Content 

def index(request):
  
    latest_attractions = Content.objects.filter(content_type='attraction').order_by('-created_at')[:20]

    context = {
        'judul': 'Tanah Lot',
        'attraction_list': latest_attractions,
    }
    return render(request, "index.html", context)



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