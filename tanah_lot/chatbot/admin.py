from django.contrib import admin
from .models import KnowledgeItem

@admin.register(KnowledgeItem)
class KnowledgeItemAdmin(admin.ModelAdmin):
    """
    Kustomisasi tampilan model KnowledgeItem di halaman admin Django.
    """
    list_display = ('topic', 'updated_at')
    search_fields = ('topic', 'keywords', 'information')
    list_filter = ('updated_at',)