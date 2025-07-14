from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
import midtransclient
from .models import Transaction
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .email_utils import send_eticket_email
from .models import Transaction, TicketType



def login_required_redirect(request):
    
    if request.user.is_authenticated:
        return redirect('ticket:ticket')
    else:
      
        messages.warning(request, 'Anda harus login terlebih dahulu untuk memesan tiket.')
        return redirect('login:login')

# ____________________________________________________________________
#
#                   KHUSUS TAMPILAN PEMBELIAN USER
# ____________________________________________________________________





def index(request):
    # Logika untuk mengambil harga dari database
    try:
        ticket_prices_db = TicketType.objects.filter(is_active=True)
        prices = {
            'domestik': {
                'adult': ticket_prices_db.get(nationality='domestik', age_group='adult').price,
                'child': ticket_prices_db.get(nationality='domestik', age_group='child').price
            },
            'asing': {
                'adult': ticket_prices_db.get(nationality='asing', age_group='adult').price,
                'child': ticket_prices_db.get(nationality='asing', age_group='child').price
            }
        }
    except TicketType.DoesNotExist:
        prices = { 
            'domestik': {'adult': 30000, 'child': 20000},
            'asing': {'adult': 75000, 'child': 40000}
        }

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        nationality = request.POST.get('nationality')
        adult_tickets = int(request.POST.get('adult_tickets'))
        child_tickets = int(request.POST.get('child_tickets'))
        total_price = float(request.POST.get('total_price'))

       
        # Membuat objek transaksi dengan menyebutkan setiap field secara eksplisit
        transaction = Transaction.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            nationality=nationality,
            adult_tickets=adult_tickets,
            child_tickets=child_tickets,
            total_price=total_price,
            status='pending'
        )
        # ==========================================================

        # Konfigurasi Midtrans 
        snap = midtransclient.Snap(
            is_production=settings.MIDTRANS_IS_PRODUCTION,
            server_key=settings.MIDTRANS_SERVER_KEY,
            client_key=settings.MIDTRANS_CLIENT_KEY
        )

        # Siapkan detail item untuk Midtrans 
        item_details = []
        if adult_tickets > 0:
            item_details.append({
                "id": f"TICKET-ADULT-{transaction.order_id}",
                "price": prices[nationality]['adult'],
                "quantity": adult_tickets,
                "name": f"Adult Ticket ({nationality.capitalize()})"
            })
        if child_tickets > 0:
            item_details.append({
                "id": f"TICKET-CHILD-{transaction.order_id}",
                "price": prices[nationality]['child'],
                "quantity": child_tickets,
                "name": f"Child Ticket ({nationality.capitalize()})"
            })
        
        
        params = {
            "transaction_details": {
                "order_id": transaction.order_id,
                "gross_amount": int(total_price)
            },
            "item_details": item_details,
            "customer_details": {
                "first_name": full_name,
                "email": email,
                "phone": phone_number
            }
        }
        try:
            snap_transaction = snap.create_transaction(params)
            transaction.midtrans_token = snap_transaction['token']
            transaction.midtrans_redirect_url = snap_transaction['redirect_url']
            transaction.save()
            return JsonResponse({'token': snap_transaction['token']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Untuk method GET 
    context = {
        'judul': 'Ticket',
        'midtrans_client_key': settings.MIDTRANS_CLIENT_KEY,
        'ticket_prices': prices,
        'ticket_prices_json': json.dumps(prices),
    }
    return render(request, "payment/purchase_page.html", context)



def order_confirmation(request, order_id):
    """
    View baru untuk menampilkan halaman konfirmasi setelah pesanan berhasil dibuat.
    """
    transaction = get_object_or_404(Transaction, order_id=order_id)
    context = {
        'judul': 'Order Confirmation',
        'transaction': transaction
    }
    return render(request, 'payment/order_confirmation.html', context)


# ____________________________________________________________________
#
#                   KHUSUS TAMPILAN DATA DI DASHBOARD
# ____________________________________________________________________


from django.db.models import Sum, F

def data(request):
    search_query = request.GET.get('q', None)

    # 1. Mulai dengan queryset dasar. belum mengambil data dari database.
    transactions_queryset = Transaction.objects.all().order_by('-created_at')

    # 2. Filter queryset JIKA ada kata kunci pencarian.
    if search_query:
        transactions_queryset = transactions_queryset.filter(
            Q(order_id__icontains=search_query) |
            Q(full_name__icontains=search_query)
        )

    # 3. LAKUKAN PAGINASI SETELAH SEMUA FILTER SELESAI.
    
    paginator = Paginator(transactions_queryset, 10) # 10 item per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 4. Hitung statistik berdasarkan queryset SEBELUM dipaginasi
   
    total_transactions_count = transactions_queryset.count()
    successful_transactions_count = transactions_queryset.filter(status='success').count()
    pending_transactions_count = transactions_queryset.filter(status='pending').count()
    successful_sells = transactions_queryset.filter(status='success')
    total_tickets_sold = successful_sells.aggregate(
        total=Sum(F('adult_tickets') + F('child_tickets'))
    )['total'] or 0

    # 5. Kirim 'page_obj' ke template, bukan queryset utuh.
    context = {
        'judul': 'Data Transaction',
        'transactions': page_obj, 
        'search_query': search_query,
        'total_transactions_count': total_transactions_count,
        'successful_transactions_count': successful_transactions_count,
        'pending_transactions_count': pending_transactions_count,
        'total_tickets_sold': total_tickets_sold,
    }
    return render(request, "transaction-list/transaction_list.html", context)


def detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    context = {
        'judul': f'Detail Transaction {transaction.order_id}',
        'transaction': transaction,
    }
    return render(request, "transaction-list/transaction_detail.html", context)


# ====================================================================
# ==> STEP 6: BUAT VIEW UNTUK MENANGANI WEBHOOK NOTIFIKASI <==
# ====================================================================
@csrf_exempt # <-- untuk menonaktifkan CSRF protection untuk view ini
def midtrans_webhook(request):
    """
    Menerima notifikasi pembayaran dari Midtrans.
    """
    if request.method == 'POST':
        try:
            # 1. Terima data notifikasi dalam format JSON
            notification_data = json.loads(request.body)
            order_id = notification_data.get('order_id')
            transaction_status = notification_data.get('transaction_status')
            fraud_status = notification_data.get('fraud_status')

            payment_type = notification_data.get('payment_type')

            print(f"Webhook Diterima: Order ID {order_id}, Status {transaction_status}") # Untuk debugging

            # 2. Ambil transaksi dari database 
            try:
                transaction = Transaction.objects.get(order_id=order_id)
            except Transaction.DoesNotExist:
                return HttpResponse(status=404)

            # 3. Verifikasi keamanan 
            # verifikasi signature key di sini
            # https://docs.midtrans.com/en/development/sandbox-notification-validation

            # 4. Perbarui status transaksi berdasarkan notifikasi
            if transaction_status == 'capture' or transaction_status == 'settlement':
                # Kondisi untuk pembayaran yang berhasil
                if fraud_status == 'accept':
                    # Hanya lakukan aksi jika statusnya memang belum 'success'
                    if transaction.status != 'success':
                        transaction.status = 'success'
                        transaction.payment_method = payment_type
                        transaction.save()  # Simpan perubahan di sini
                        send_eticket_email(transaction) # Kirim email setelah disimpan
    
            elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
                # Kondisi untuk pembayaran yang gagal atau dibatalkan
                transaction.status = 'failed'
                transaction.save() # Simpan perubahan status 'failed'

                # Pindahkan print ke luar agar selalu memberi laporan status terakhir
                print(f"Status untuk Order ID {order_id} sekarang adalah {transaction.status}")

            # 5. Beri tahu Midtrans bahwa notifikasi sudah diterima
            return HttpResponse(status=200)

        except json.JSONDecodeError:
            return HttpResponse(status=400)
    
    return HttpResponse(status=405) # Method Not Allowed jika bukan POST



# ==========================================================
#  VIEW HALAMAN VERIFIKASI TIKET 
# ==========================================================
def verify_ticket(request, order_id):
    """
    Memeriksa validitas tiket berdasarkan order_id dan menampilkannya.
    """
    try:
        # 1. Cari transaksi di database berdasarkan order_id dari URL
        transaction = Transaction.objects.get(pk=order_id)

        # 2. Tentukan apakah tiket valid atau tidak
        #    Tiket dianggap valid jika statusnya 'success'.
        is_valid = transaction.status == 'success'

        # Siapkan pesan untuk ditampilkan
        if is_valid:
            message = "TIKET VALID"
        else:
            message = f"TIKET TIDAK VALID (Status: {transaction.status.capitalize()})"

    except Transaction.DoesNotExist:
        # Jika Order ID tidak ditemukan di database
        transaction = None
        is_valid = False
        message = "TIKET TIDAK DITEMUKAN"

    # 3. Kirim semua data ke template
    context = {
        'judul': 'Verifikasi Tiket',
        'transaction': transaction,
        'is_valid': is_valid,
        'message': message,
    }

    # Render template baru yang akan kita buat
    return render(request, 'ticket/verify_page.html', context)


# ==========================================================
#  VIEW BARU UNTUK MENGIRIM ULANG E-TICKET 
# ==========================================================
def resend_eticket(request, order_id):
    """
    Mencari transaksi dan mengirim ulang email E-Ticket.
    """
    # Gunakan get_object_or_404 untuk cara yang lebih bersih dalam menangani error
    transaction = get_object_or_404(Transaction, pk=order_id)

    try:
        
        send_eticket_email(transaction)
        # Buat pesan sukses untuk ditampilkan di halaman
        messages.success(request, f"E-Ticket untuk Order ID {order_id} berhasil dikirim ulang ke {transaction.email}.")
    except Exception as e:
        # Jika ada error saat mengirim, buat pesan error
        messages.error(request, f"Gagal mengirim ulang E-Ticket: {e}")

    # Setelah selesai, kembalikan pengguna ke halaman detail transaksi semula
    return redirect('ticket:transaction_detail', pk=order_id)