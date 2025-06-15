# dashboard/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Content, UserProfile
from .forms import ContentForm, UserCreationFormByAdmin, UpdateUserForm
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# ===================================================================
# CRUD UNTUK ARTICLE / CONTENT
# ===================================================================

from django.db.models import Q # Pastikan ini diimpor

@login_required(login_url='/login/')
def article(request): # Nama fungsi tetap 'index' sesuai kode Anda
    """Menampilkan semua data konten di tabel, dan menangani pencarian."""
 

    # --- LOGIKA PENCARIAN DIMASUKKAN DI SINI ---
    query = request.GET.get('q')
    
    # Mulai dengan mengambil semua konten
    content_queryset = Content.objects.all()

    if query:
        # Jika ada kata kunci pencarian, filter queryset-nya
        # Cari di title, description, DAN content_type
        content_queryset = content_queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(content_type__icontains=query)
        ).distinct()
    # --- AKHIR LOGIKA PENCARIAN ---

    # Urutkan hasilnya
    all_content_items = content_queryset.order_by('-created_at')

    context = {
        'judul': 'Data Content',
        'all_content_items': all_content_items,
        'search_query': query, # Kirim kembali kata kunci ke template
    }
    return render(request, "article/data.html", context)


@login_required(login_url='/login/')
def addArticle(request):
    """Menangani form untuk menambah konten baru."""
  

    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            new_content = form.save(commit=False)
            new_content.author = request.user
            new_content.save()
            messages.success(request, f'Konten "{new_content.title}" berhasil ditambahkan!')
            return redirect('dashboard:article_data')
    else:
        form = ContentForm()
    context = {'judul': 'Add Content', 'form': form}
    return render(request, "article/add.html", context)


@login_required(login_url='/login/')
def update_content(request, pk):
    """Menangani form untuk mengedit konten yang sudah ada."""
    

    # Ambil objek konten yang mau diedit berdasarkan pk (ID) dari URL
    content_instance = get_object_or_404(Content, pk=pk)

    if request.method == 'POST':
        # Saat form disubmit, isi form dengan data baru DAN instance lama
        # Ini memberitahu Django untuk meng-update objek yang ada, bukan membuat baru
        form = ContentForm(request.POST, request.FILES, instance=content_instance)
        if form.is_valid():
            form.save()
            messages.success(request, f'Konten "{content_instance.title}" berhasil diperbarui.')
            return redirect('dashboard:article_data')
        else:
            messages.error(request, 'Gagal memperbarui konten. Periksa kembali isian Anda.')
    else:
        # Saat halaman pertama kali dibuka, isi form dengan data dari instance yang ada
        form = ContentForm(instance=content_instance)

    context = {
        'judul': 'Update Content',
        'form': form,
        'is_update_page': True, # Penanda bahwa ini adalah halaman update
    }
    # Kita akan buat template baru bernama update.html
    return render(request, 'article/edit.html', context)


# dashboard/views.py

@login_required(login_url='/login/')
def delete_content(request, pk):
    """
    Menampilkan halaman konfirmasi dan menghapus objek konten.
    """
  
    # --- AKHIR BLOK PENJAGA ---

    content_to_delete = get_object_or_404(Content, pk=pk)

    # Ini berjalan jika user menekan tombol "Ya, Hapus" di halaman konfirmasi
    if request.method == 'POST':
        title = content_to_delete.title
        content_to_delete.delete()
        messages.success(request, f'Konten "{title}" telah berhasil dihapus.')
        return redirect('dashboard:article_data') # Kembali ke daftar konten

    # Jika user baru mengklik tombol delete di tabel, tampilkan halaman konfirmasi
    context = {
        'judul': 'Konfirmasi Hapus Konten',
        'item': content_to_delete
    }
    return render(request, 'article/delete.html', context)
# ===================================================================
# CRUD UNTUK USER
# ===================================================================

@login_required(login_url='/login/')
def user(request): # Nama fungsi tetap 'user' sesuai keinginan Anda
    """
    Menampilkan semua data user di tabel, DAN menangani logika pencarian.
    """
    

    # --- LOGIKA PENCARIAN DIMASUKKAN DI SINI ---
    # Ambil kata kunci dari URL, contoh: /users/data/?q=admin
    query = request.GET.get('q')
    
    # Mulai dengan mengambil semua user
    user_queryset = User.objects.select_related('profile').all()

    if query:
        # Jika ada kata kunci pencarian, filter queryset-nya
        # Cari di username, nama depan, nama belakang, email, dan role dari profil
        user_queryset = user_queryset.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(profile_role_icontains=query)
        ).distinct()
    # --- AKHIR LOGIKA PENCARIAN ---

    # Urutkan hasilnya
    all_users = user_queryset.order_by('username')

    context = {
        'judul': 'Data User',
        'all_users': all_users,
        'search_query': query, # Kirim kembali kata kunci ke template
    }
    return render(request, "users/data.html", context)


# ===================================================================
# UPDATE USER 
# ===================================================================

@login_required(login_url='/login/')
def addUser(request):
    """Menangani form untuk menambah user baru oleh admin."""
  

    if request.method == 'POST':
        form = UserCreationFormByAdmin(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            UserProfile.objects.create(user=new_user, role=cd['role'], phone_number=cd['phone_number'])
            messages.success(request, f"User '{cd['username']}' berhasil ditambahkan.")
            return redirect('dashboard:users_data')
    else:
        form = UserCreationFormByAdmin()
    context = {'judul': 'Add User', 'form': form}
    return render(request, "users/add.html", context)


@login_required(login_url='/login/')

# ===================================================================
# UPDATE USER 
# ===================================================================

def update_user(request, pk):
 
    
    user_to_update = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user_to_update)
        if form.is_valid():
            cd = form.cleaned_data
            user_to_update.username = cd['username']
            user_to_update.email = cd['email']
            if cd.get('password'):
                user_to_update.set_password(cd['password'])
            user_to_update.save()

            if hasattr(user_to_update, 'profile'):
                user_to_update.profile.role = cd['role']
                user_to_update.profile.phone_number = cd['phone_number']
                user_to_update.profile.save()
            
            messages.success(request, f"Data user '{cd['username']}' berhasil diperbarui.")
            return redirect('dashboard:users_data') # Pastikan nama URL ini benar
    else:
        initial_data = {
            'username': user_to_update.username,
            'email': user_to_update.email,
            'role': user_to_update.profile.role if hasattr(user_to_update, 'profile') else '',
            'phone_number': user_to_update.profile.phone_number if hasattr(user_to_update, 'profile') else '',
        }
        form = UpdateUserForm(initial=initial_data, instance=user_to_update)
        
    context = {
        'judul': f'Update User: {user_to_update.username}',
        'form': form,
    }
    return render(request, 'users/edit.html', context)
@login_required(login_url='/login/')


# ===================================================================
# DELETE USER 
# ===================================================================

def delete_user(request, pk):
    """Menghapus user setelah ada konfirmasi."""
  

    # Ambil objek user yang akan dihapus
    user_to_delete = get_object_or_404(User, pk=pk)

    # Keamanan tambahan: jangan biarkan admin menghapus akunnya sendiri
    if request.user.pk == user_to_delete.pk:
        messages.error(request, "Anda tidak bisa menghapus akun Anda sendiri.")
        return redirect('dashboard:users_data')

    if request.method == 'POST':
        # Blok ini hanya berjalan jika user menekan tombol "Ya, Hapus" di halaman konfirmasi
        username = user_to_delete.username
        user_to_delete.delete() # Perintah untuk menghapus user dari database
        messages.success(request, f"User '{username}' berhasil dihapus.")
        return redirect('dashboard:users_data')
    
    # Jika methodnya GET, tampilkan halaman konfirmasi
    context = {
        'judul': 'Konfirmasi Hapus User',
        'item': user_to_delete
    }
    return render(request, 'users/data.html', context)
# ===================================================================
# RESET PASSWORD (STUB)
# ===================================================================


@login_required(login_url='/login/')
def resetPassword(request):
  
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Simpan user dengan password baru
            user = form.save()
            
            # --- INI BARIS KUNCINYA ---
            # Memperbarui sesi login agar Anda tidak ter-logout
            update_session_auth_hash(request, user)
            # ---------------------------

            messages.success(request, 'Password Anda berhasil diperbarui!')
            # Arahkan kembali ke halaman daftar user
            return redirect('dashboard:users_data') 
        else:
            messages.error(request, 'Gagal mengubah password. Silakan periksa kembali isian Anda.')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'judul': 'Change Password',
        'form': form
    }
    return render(request, "users/reset_password.html", context)

#----------------------------------------------------------------------------------


# khusus dashboard
def index(request):
    context={
        'judul':'Dashboard | Tanah Lot',
    }
    return render(request,"index-dashboard.html", context)


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