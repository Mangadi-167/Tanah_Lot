from django.shortcuts import render, get_object_or_404 

from dashboard.models import Content 

def index(request):
    
    all_news_articles = Content.objects.filter(content_type='news').order_by('-created_at')


    context = {
        'judul': 'News | Event Tanah Lot',
        'news_articles': all_news_articles, 
    }
    return render(request,"news/index.html", context)


def detail(request, pk):
    """Menampilkan detail satu artikel dan daftar artikel terbaru di sidebar."""
    
    single_article = get_object_or_404(Content, pk=pk)
    
    recent_posts = Content.objects.filter(content_type='news').exclude(pk=pk).order_by('-created_at')[:5]
    
    context = {
        'judul': single_article.title, 
        'article': single_article,
        'recent_posts': recent_posts,
    }
    return render(request, 'news/detail.html', context)