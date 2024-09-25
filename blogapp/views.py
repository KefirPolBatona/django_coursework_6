from django.views.generic import ListView, DetailView

from blogapp.models import Article
from blogapp.services import get_cached_article


class ArticleListView(ListView):
    """
    Контроллер для вывода списка статей.
    """

    model = Article

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['categories'] = get_cached_article()
        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class ArticleDetailView(DetailView):
    """
    Контроллер для вывода статьи с информацией.
    """
    model = Article

    def get_object(self, queryset=None):
        """
        Увеличивает кол-во просмотров статьи.
        """

        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object
