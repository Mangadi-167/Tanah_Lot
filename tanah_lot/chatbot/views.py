from django.shortcuts import render

# Create your views here.
def index(request):
    context= {
    'judul' : 'Chat AI | Tanah Lot',
    }
    return render (request, 'chatbot.html', context)