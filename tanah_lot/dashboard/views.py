from django.shortcuts import render


# khusus dashboard
def index(request):
    context={
        'judul':'Dashboard | Tanah Lot',
    }
    return render(request,"index-dashboard.html", context)


# ---------------------------------------------------------------------------------

# khusus article
def article(request):
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

# khusus calender
def calender(request):
    context={
        'judul':'Data Event Calender',
    }
    return render(request,"calender/data.html", context)

def addCalender(request):
    context={
        'judul':'Add Calender',
    }
    return render(request,"calender/add.html", context)


def editCalender(request):
    context={
        'judul':'Edit Calender',
    }
    return render(request,"calender/edit.html", context)


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


#----------------------------------------------------------------------------------

# khusus reset password
def resetPassword(request):
    context={
        'judul' : 'Change Password'
    }
    return render (request, "reset-password.html", context)