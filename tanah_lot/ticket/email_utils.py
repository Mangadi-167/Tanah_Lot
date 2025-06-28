import qrcode
from io import BytesIO
from django.core.mail import EmailMessage 
from django.template.loader import render_to_string

from django.conf import settings

def send_eticket_email(transaction):
    """
    Membuat QR code, dan mengirimkannya sebagai inline attachment di email.
    """
    try:
        # 1. Buat gambar QR Code di memori (tetap sama)
        # qr_img = qrcode.make(transaction.order_id)
        # Membuat URL lengkap untuk verifikasi tiket
        verification_url = f"https://tanahlot.id/ticket/verify/{transaction.order_id}/"
        qr_img = qrcode.make(verification_url)
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
       
       
        buffer.seek(0) 

        # 2. Siapkan context untuk template (tanpa QR code base64)
        context = {
            'transaction': transaction,
            
        }

        # 3. Siapkan email menggunakan EmailMessage
        subject = f"Your E-Ticket for Tanah Lot - Order ID: {transaction.order_id}"
        html_message = render_to_string('email/eticket_template.html', context)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = transaction.email

        # Buat objek email
        email = EmailMessage(
            subject,
            html_message,
            from_email,
            [to_email]
        )
        # Set tipe konten menjadi HTML
        email.content_subtype = "html"

        # 4. LAMPIRKAN GAMBAR QR CODE SECARA INLINE
        # nama file 'qrcode.png' dan berikan Content-ID <qrcode_image>
        # Content-ID ini yang akan panggil di template HTML
        email.attach('qrcode.png', buffer.getvalue(), 'image/png')

        # 5. Kirim email
        email.send()

        print(f"Email E-Ticket untuk {transaction.order_id} berhasil dikirim ke {to_email}.")

    except Exception as e:
        print(f"Gagal mengirim email untuk {transaction.order_id}: {e}")