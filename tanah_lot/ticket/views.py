from django.shortcuts import render

# ____________________________________________________________________

#                     KHUSUS TAMPILAN PEMBELIAN USER
# ____________________________________________________________________

def index(request):
    context={
        'judul':'Ticket',
    }
    return render(request,"payment/purchase_page.html", context)



# ____________________________________________________________________

#                     KHUSUS TAMPILAN DATA DI DASHBOARD
# ____________________________________________________________________

def data(request):
    context={
        'judul':'Data Transaction',
    }
    return render(request,"transaction-list/transaction_list.html", context)