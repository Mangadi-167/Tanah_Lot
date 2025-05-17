from django.shortcuts import render

def index(request):
    context={
        'judul':'Tanah Lot',
    }
    return render(request,"index.html", context)