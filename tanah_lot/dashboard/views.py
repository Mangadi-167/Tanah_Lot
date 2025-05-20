from django.shortcuts import render


# khusus article
def index(request):
    context={
        'judul':'Data Content',
    }
    return render(request,"article/data.html", context)

def addArticle(request):
    context={
        'judul':'Add Content',
    }
    return render(request,"article/add.html", context)


# ---------------------------------------------------------------------------------

# khusus users
def user(request):
    context={
        'judul':'Data User',
    }
    return render(request,"users/data.html", context)

def addUser(request):
    context={
        'judul' : 'Add User',
    }
    return render (request, "users/add.html", context)