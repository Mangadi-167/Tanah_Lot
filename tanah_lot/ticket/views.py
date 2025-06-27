from django.shortcuts import render


def index(request):
    context={
        'judul':'Ticket',
    }
    return render(request,"payment/purchase_page.html", context)