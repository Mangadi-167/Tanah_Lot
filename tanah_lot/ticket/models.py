from django.db import models
from django.contrib.auth.models import User
import uuid

# Pilihan untuk status pembayaran
PAYMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('success', 'Success'),
    ('failed', 'Failed'),
]

# Pilihan untuk kewarganegaraan
NATIONALITY_CHOICES = [
    ('domestik', 'Domestik'),
    ('asing', 'Asing'),
]

class Transaction(models.Model):
    """
    Model ini akan menyimpan setiap transaksi pembelian tiket.
    """
    # ID Unik untuk setiap pesanan, ini yang akan di kirim ke Midtrans
    order_id = models.CharField(max_length=100, unique=True, primary_key=True, editable=False)
    
    # Menghubungkan ke user yang login (jika ada)
    # on_delete=models.SET_NULL berarti jika user dihapus, transaksinya tidak ikut terhapus.
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Data dari form pembeli
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    
    # Data dari pilihan tiket
    nationality = models.CharField(max_length=10, choices=NATIONALITY_CHOICES)
    adult_tickets = models.PositiveIntegerField(default=0)
    child_tickets = models.PositiveIntegerField(default=0)
    
    # Data keuangan dan status
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    # Data dari Midtrans (gunakan nanti)
    midtrans_token = models.CharField(max_length=255, blank=True, null=True)
    midtrans_redirect_url = models.CharField(max_length=255, blank=True, null=True)

    # Waktu transaksi dibuat
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Membuat Order ID unik secara otomatis jika belum ada
        if not self.order_id:
            self.order_id = f"ORD-{str(uuid.uuid4()).split('-')[0].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaksi {self.order_id} oleh {self.full_name}"

    class Meta:
        verbose_name = "Transaksi Tiket"
        verbose_name_plural = "Semua Transaksi Tiket"
        ordering = ['-created_at'] # Mengurutkan dari yang terbaru

class TicketType(models.Model):
    NATIONALITY_CHOICES = [('domestik', 'Domestik'), ('asing', 'Asing')]
    AGE_CHOICES = [('adult', 'Adult'), ('child', 'Child')]

    nationality = models.CharField(max_length=10, choices=NATIONALITY_CHOICES)
    age_group = models.CharField(max_length=5, choices=AGE_CHOICES)
    price = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        # Membuat kombinasi nationality dan age_group menjadi unik
        unique_together = ('nationality', 'age_group')
        verbose_name = "Tipe Tiket"
        verbose_name_plural = "Semua Tipe Tiket"

    def __str__(self):
        # Mengambil nama yang mudah dibaca dari choices
        return f"{self.get_nationality_display()} - {self.get_age_group_display()}"