from django.db import models

class KnowledgeItem(models.Model):
    """
    Model untuk menyimpan item pengetahuan spesifik untuk chatbot.
    """
    topic = models.CharField(
        max_length=200,
        unique=True,
        help_text="Topik utama dari item pengetahuan ini (e.g., 'Lokasi Parkir Utama')"
    )
    
    keywords = models.TextField(
        help_text="Kata kunci yang relevan untuk memicu topik ini, dipisahkan koma (e.g., parkir, mobil, motor, tempat parkir)"
    )
    
    information = models.TextField(
        help_text="Informasi detail yang akan diberikan sebagai jawaban oleh chatbot."
    )

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        
        return self.topic

    class Meta:
        
        ordering = ['topic']
        verbose_name = "Item Pengetahuan"
        verbose_name_plural = "Item-item Pengetahuan"