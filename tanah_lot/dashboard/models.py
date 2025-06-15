# dashboard/models.py

from django.db import models
from django.contrib.auth.models import User # Mengimpor model User bawaan Django

# ==================================
# MODEL UNTUK DATA USER TAMBAHAN
# ==================================

# Pilihan untuk kolom 'role' (ENUM di ERD Anda)
ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('pengguna', 'Pengguna'),
    # Tambahkan role lain jika perlu, misal: ('kontributor', 'Kontributor')
]

# Ini adalah implementasi tabel 'users' Anda dengan cara yang aman dan direkomendasikan
class UserProfile(models.Model):
    # Membuat hubungan satu-ke-satu dengan User bawaan Django.
    # Setiap User akan memiliki satu UserProfile.
    # on_delete=models.CASCADE berarti jika User dihapus, profilnya juga ikut terhapus.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Menambahkan kolom 'role' kustom Anda
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='pengguna')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Anda bisa menambahkan field lain di sini jika perlu, misal foto profil, no. telepon, dll.
    # foto_profil = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def _str_(self):
        # Ini akan menampilkan username saat objek UserProfile ditampilkan di admin
        return self.user.username

    class Meta:
        verbose_name = "Profil Pengguna"
        verbose_name_plural = "Profil Pengguna"


# ==================================
# MODEL UNTUK TABEL CONTENT
# ==================================

# Pilihan untuk kolom 'content_type' (ENUM di ERD Anda)
CONTENT_TYPE_CHOICES = [
    ('news', 'News & Events'),
    ('attraction', 'Attraction & Accommodation'),
]

class Content(models.Model):
    # PK (content_id) akan dibuat otomatis oleh Django sebagai field 'id'

    # FK (user_id) ke User bawaan Django
    # on_delete=models.SET_NULL berarti jika user dihapus, kontennya tidak ikut terhapus,
    # tapi field author akan di-set menjadi NULL. Ini bagus untuk menjaga data konten.
    # null=True, blank=True mengizinkan field ini kosong.
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='contents')

    # VAR (content_name) menjadi CharField
    title = models.CharField(max_length=255)

    # VAR (content_description) menjadi TextField yang lebih cocok untuk teks panjang
    description = models.TextField()

    # VAR (content_image) menjadi ImageField untuk upload gambar.
    # Ini memerlukan instalasi Pillow: pip install Pillow
    image = models.ImageField(upload_to='content_images/', blank=True, null=True)

    # ENUM (content_type) menjadi CharField dengan choices
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES)

    # Menambahkan field waktu (best practice)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.title

    class Meta:
        verbose_name = "Konten"
        verbose_name_plural = "Semua Konten"