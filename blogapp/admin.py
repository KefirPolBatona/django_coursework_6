from django.contrib import admin

from blogapp.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'article_name', 'article_content', 'article_image',
        'created_at', 'views_count', 'user',
    )