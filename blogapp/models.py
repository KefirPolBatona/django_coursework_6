from django.db import models

from usersapp.models import User

NULLABLE = {'blank': True, 'null': True}


class Article(models.Model):
    """
    Модель статьи.
    """

    article_name = models.CharField(max_length=100, verbose_name="заголовок статьи")
    article_content = models.TextField(verbose_name="содержимое статьи", **NULLABLE)
    article_image = models.ImageField(upload_to="image_article/", verbose_name="изображение", **NULLABLE)

    created_at = models.DateField(auto_now_add=True, verbose_name="дата публикации")
    views_count = models.IntegerField(default=0, verbose_name='просмотры')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)

    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        **NULLABLE,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.article_name} (от {self.created_at})"

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        permissions = [
            ("can_add_article", "Can add article"),
        ]
        ordering = ['-id']
