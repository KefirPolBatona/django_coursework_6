from django.urls import path

from blogapp.apps import BlogappConfig
from blogapp.views import ArticleListView, ArticleDetailView

app_name = BlogappConfig.name

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('detail/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),

]

