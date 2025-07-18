from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from ticket.models import Transaction  
from django.db.models import Sum, F      
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Content, UserProfile
from .forms import ContentForm, UserCreationFormByAdmin, UpdateUserForm
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EventForm
import json 
from .models import Event
from ticket.models import TicketType
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse


# ===================================================================
# CRUD UNTUK ARTICLE / CONTENT
# ===================================================================

from django.db.models import Q 

@login_required(login_url='/login/')
def article(request): 
    
    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')
    
    """Menampilkan semua data konten di tabel, dan menangani pencarian."""
 
    
    query = request.GET.get('q')
    
   
    content_queryset = Content.objects.all()

    if query:
        
        content_queryset = content_queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(content_type__icontains=query)
        ).distinct()
 
    all_content_items = content_queryset.order_by('-created_at')

    context = {
        'judul': 'Data Content',
        'all_content_items': all_content_items,
        'search_query': query, # Kirim kembali kata kunci ke template
    }
    return render(request, "article/data.html", context)


@login_required(login_url='/login/')
def addArticle(request):
    
    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')


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


    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')

    """Menangani form untuk mengedit konten yang sudah ada."""
    

   
    content_instance = get_object_or_404(Content, pk=pk)

    if request.method == 'POST':
      
        form = ContentForm(request.POST, request.FILES, instance=content_instance)
        if form.is_valid():
            form.save()
            messages.success(request, f'Konten "{content_instance.title}" berhasil diperbarui.')
            return redirect('dashboard:article_data')
        else:
            messages.error(request, 'Gagal memperbarui konten. Periksa kembali isian Anda.')
    else:
      
        form = ContentForm(instance=content_instance)

    context = {
        'judul': 'Update Content',
        'form': form,
        'is_update_page': True, 
    }
   
    return render(request, 'article/edit.html', context)


# dashboard/views.py

@login_required(login_url='/login/')
def delete_content(request, pk):

    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')

    """
    Menampilkan halaman konfirmasi dan menghapus objek konten.
    """
  

    content_to_delete = get_object_or_404(Content, pk=pk)

  
    if request.method == 'POST':
        title = content_to_delete.title
        content_to_delete.delete()
        messages.success(request, f'Konten "{title}" telah berhasil dihapus.')
        return redirect('dashboard:article_data') 

    
    context = {
        'judul': 'Konfirmasi Hapus Konten',
        'item': content_to_delete
    }
    return render(request, 'article/data.html', context)
# ===================================================================
# CRUD UNTUK USER
# ===================================================================

@login_required(login_url='/login/')
def user(request): 

    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')


    """
    Menampilkan semua data user di tabel, DAN menangani logika pencarian.
    """
    
    query = request.GET.get('q')
    
  
    user_queryset = User.objects.select_related('profile').all()

    if query:
       
        user_queryset = user_queryset.filter(
            Q(username__icontains=query) |
            Q(first__name__icontains=query) |
            Q(last__name__icontains=query) |
            Q(email__icontains=query) |
            Q(profile__role__icontains=query)
        ).distinct()
   

    # Urutkan hasilnya
    all_users = user_queryset.order_by('username')

    context = {
        'judul': 'Data User',
        'all_users': all_users,
        'search_query': query, 
    }
    return render(request, "users/data.html", context)


# ===================================================================
# UPDATE USER 
# ===================================================================

@login_required(login_url='/login/')
def addUser(request):

    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')


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

    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')
 
    
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

    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')



    """Menghapus user setelah ada konfirmasi."""
  

 
    user_to_delete = get_object_or_404(User, pk=pk)

   
    if request.user.pk == user_to_delete.pk:
        messages.error(request, "Anda tidak bisa menghapus akun Anda sendiri.")
        return redirect('dashboard:users_data')

    if request.method == 'POST':
       
        username = user_to_delete.username
        user_to_delete.delete() # Perintah untuk menghapus user dari database
        messages.success(request, f"User '{username}' berhasil dihapus.")
        return redirect('dashboard:users_data')
    
   
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


    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')
  
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
           
            user = form.save()
            
          
            update_session_auth_hash(request, user)
          

            messages.success(request, 'Password Anda berhasil diperbarui!')
            
            return redirect('dashboard:users_data') 
        else:
            messages.error(request, 'Gagal mengubah password. Silakan periksa kembali isian Anda.')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'judul': 'Change Password',
        'form': form
    }
    return render(request, "users/reset-password.html", context)

#----------------------------------------------------------------------------------

@login_required(login_url='/login/') 
def index(request):


    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')
    
    content_count = Content.objects.count()
    user_count = User.objects.count()

    successful_transactions = Transaction.objects.filter(status='success')

    total_income_data = successful_transactions.aggregate(total=Sum('total_price'))
    total_income = total_income_data['total'] or 0

    total_tickets_data = successful_transactions.aggregate(total=Sum(F('adult_tickets') + F('child_tickets')))
    total_tickets_sold = total_tickets_data['total'] or 0

    search_query = request.GET.get('q', None)

    # --- Logika untuk Tabel Transaksi dengan Paginasi ---
    # Ambil semua transaksi untuk dipaginasi
    all_transactions_list = Transaction.objects.all().order_by('-created_at')

    if search_query:
        all_transactions_list = all_transactions_list.filter(
            Q(order_id__icontains=search_query) |
            Q(full_name__icontains=search_query)
        )

   
    paginator = Paginator(all_transactions_list, 5) 
    page_number = request.GET.get('page')

   
    transactions_page_obj = paginator.get_page(page_number)

   
    context = {
        'judul': 'Dashboard | Tanah Lot',
        'content_count': content_count,
        'user_count': user_count,
        'calendar_count': Event.objects.count(), 
        'total_income': total_income,
        'total_tickets_sold': total_tickets_sold,

        
        'transactions_on_dashboard': transactions_page_obj, 
    }
    return render(request, "index-dashboard.html", context)



# ---------------------------------------------------------------------------------

# khusus calender
@login_required(login_url='/login/')
def calender_events_api(request):

    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')



    all_events = Event.objects.all()
    events_list = []
    for event in all_events:
        events_list.append({
            'id': event.id,
            'title': event.event_name,
            'date': event.event_date.strftime('%Y-%m-%d'),
            # Baris ini sekarang akan berfungsi karena 'reverse' sudah di-import
            'edit_url': reverse('dashboard:edit_calender', args=[event.id]),
            'delete_url': reverse('dashboard:delete_calender', args=[event.id]),
        })
    return JsonResponse(events_list, safe=False)
# --- VIEW UNTUK MENAMPILKAN HALAMAN KALENDER (DISEDERHANAKAN) ---
@login_required(login_url='/login/')
def calender_data(request):


    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')
    


    context = {'judul': "Event Calender"}
    return render(request, 'calender/data.html', context)

# --- VIEW UNTUK MENAMBAH EVENT (TETAP SAMA) ---
@login_required(login_url='/login/')
def add_calender(request):


    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')
    


    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event baru berhasil ditambahkan ke kalender.')
            return redirect('dashboard:calender_data')
    else:
        form = EventForm()
    context = {'judul': 'Add Event Calender', 'form': form}
    return render(request, 'calender/add.html', context)

@login_required(login_url='/login/')
def edit_calender(request, event_id):


    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')
    


    # Ambil data event yang ada
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        # Saat menyimpan, ikat data baru ke instance event yang ada
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save() # Ini akan melakukan UPDATE
            messages.success(request, 'Event berhasil diperbarui.')
            return redirect('dashboard:calender_data')
    else:
        # Saat menampilkan, isi form dengan data dari instance event
        form = EventForm(instance=event)
    
    context = {
        'judul': 'Edit Event',
        'form': form
    }
    # Render template KHUSUS untuk edit
    return render(request, 'calender/edit.html', context)


@login_required(login_url='/login/')
def delete_calender(request, event_id):


    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')
    


    event = get_object_or_404(Event, id=event_id)
    
    # Sebaiknya gunakan method POST untuk delete demi keamanan
    if request.method == 'POST':
        event.delete()
        messages.success(request, f"Event '{event.event_name}' telah dihapus.")
        return redirect('dashboard:calender_data')
    else:
        # Jika diakses via GET, redirect saja (atau tampilkan halaman konfirmasi)
        # Untuk keamanan, kita hanya akan mengizinkan POST
        return redirect('dashboard:calender_data')
    
    
# ____________________________________________________________________________________

#                                   Update Harga Ticket

# ____________________________________________________________________________________



@login_required(login_url='/login/')
def manage_ticket_prices(request):



    try:
        if request.user.profile.role != 'admin':
            return redirect('/')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil pengguna tidak ditemukan. Akses ditolak.')
        return redirect('/')
    

    
    # Logika untuk menangani permintaan POST (saat form disubmit)
    if request.method == 'POST':
        # Ambil semua ID tiket dan harga baru dari data POST
        prices_data = {key.split('-')[1]: value for key, value in request.POST.items() if key.startswith('price-')}

        try:
            for ticket_id, new_price in prices_data.items():
                if new_price: # Pastikan harganya tidak kosong
                    ticket = TicketType.objects.get(id=int(ticket_id))
                    ticket.price = int(new_price)
                    ticket.save()

            messages.success(request, "Ticket prices have been updated successfully!")
        except (ValueError, TicketType.DoesNotExist) as e:
            messages.error(request, f"Failed to update prices. Error: {e}")

        # Redirect kembali ke halaman yang sama untuk melihat perubahan
        return redirect('dashboard:manage_ticket_prices')

    # Logika untuk permintaan GET (saat halaman pertama kali dibuka)
    try:
        ticket_types = {
            'domestik_adult': TicketType.objects.get(nationality='domestik', age_group='adult'),
            'domestik_child': TicketType.objects.get(nationality='domestik', age_group='child'),
            'asing_adult': TicketType.objects.get(nationality='asing', age_group='adult'),
            'asing_child': TicketType.objects.get(nationality='asing', age_group='child'),
        }
    except TicketType.DoesNotExist:
        messages.error(request, "Ticket price data not found. Please add it via the Django Admin page first.")
        ticket_types = {}

    context = {
        'judul': 'Manage Ticket Prices',
        'ticket_types': ticket_types,
    }
    
    return render(request, "ticket/manage_prices.html", context)