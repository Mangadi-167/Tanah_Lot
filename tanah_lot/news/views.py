from django.shortcuts import render

# Create your views here.
# def index (request):
#     return render(request, "news/index.html")

def index(request):
    context={
        'judul':'News | Event Tanah Lot',
    }
    return render(request,"news/index.html", context)

# def detail_artikel(request, artikel_id):
#     artikel = get_object_or_404(Artikel, pk=artikel_id)
#     return render(request, 'news/detail/detail.html', {'artikel': artikel})

def detail(request):

    context={
        'judul' : 'News | Event Tanah Lot',
    }
  
    return render(request, 'news/detail.html', context)