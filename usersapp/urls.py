from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from usersapp.apps import UsersappConfig
from usersapp.views import RegisterView, ProfileView, email_verification, UserRecoveryPasswordView, UserListView, \
    blocked_user, UserDeleteView

app_name = UsersappConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='usersapp/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('blocked/<int:pk>/', blocked_user, name='user_blocked'),

    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('recovery-password/', UserRecoveryPasswordView.as_view(), name='recovery_password'),
    path("list/", UserListView.as_view(), name='user_list'),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name='user_delete'),
]
