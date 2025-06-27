from django.db import models
from django.contrib.auth.models import User 

# ==================================
# MODEL UNTUK DATA USER TAMBAHAN
# ==================================


ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('pengguna', 'Pengguna'),
    
]


class UserProfile(models.Model):
  
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Menambahkan kolom 'role' kustom Anda
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='pengguna')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    

    def _str_(self):
       
        return self.user.username

    class Meta:
        verbose_name = "Profil Pengguna"
        verbose_name_plural = "Profil Pengguna"


# ==================================
# MODEL UNTUK TABEL CONTENT
# ==================================


CONTENT_TYPE_CHOICES = [
    ('news', 'News & Events'),
    ('attraction', 'Attraction & Accommodation'),
]

class Content(models.Model):
  
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='contents')

    title = models.CharField(max_length=255)

    
    description = models.TextField()

    
    image = models.ImageField(upload_to='content_images/', blank=True, null=True)

  
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES)

   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.title

    class Meta:
        verbose_name = "Konten"
        verbose_name_plural = "Semua Konten"



# Calender
class Event(models.Model):
    event_date = models.DateField()
    event_name = models.CharField(max_length=255) # Pastikan ini ada dan ejaannya benar
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.event_name