from django.contrib import admin

from usersapp.models import User

""" Отображает раздел "Пользователи" в админке """
admin.site.register(User)
