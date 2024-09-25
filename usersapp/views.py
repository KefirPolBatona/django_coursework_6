import secrets
import random
import string

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from usersapp.forms import UserRegisterForm, UserProfileForm, UserRecoveryPasswordForm
from usersapp.models import User

from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    """
    Контроллер для регистрации (создания) пользователя.
    """

    model = User
    form_class = UserRegisterForm
    template_name = 'usersapp/register.html'
    success_url = reverse_lazy('usersapp:login')

    def form_valid(self, form):
        """
        Создает и направляет пользователю на эл. почту токен для верификации эл. почты.
        :param:
        token - генерация токена,
        host - host пользователя, пользователь определяется через request, host через get_host(),
        url - ссылка (путь перехода) пользователю для подтверждения эл. почты,
        send_mail() - функция отправки пользователю на эл. почту.
        """

        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/usersapp/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение адреса электронной почты',
            message=f'Перейдите по ссылке для подтверждение адреса электронной почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """
    Верификация эл. почты пользователя после перехода по ссылке, отправленной через form_valid().
    """

    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("usersapp:login"))


class ProfileView(UpdateView):
    """
    Контроллер для редактирования профиля пользователя.
    """

    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('mailingapp:index')

    def get_object(self, queryset=None):
        """
        Метод для получения объекта класса (пользователя) для его редактирования.
        """

        return self.request.user


@login_required
@permission_required('usersapp.сan_block_user')
def blocked_user(request, pk):
    """
    Контроллер для блокировки пользователя.
    """

    user_item = get_object_or_404(User, pk=pk)
    if user_item.is_block:
        user_item.is_block = False
    else:
        user_item.is_block = True

    user_item.save()

    return redirect(reverse('usersapp:user_list'))


class UserRecoveryPasswordView(PasswordResetView):
    """
    Контроллер для восстановления пароля.
    """

    model = User
    form_class = UserRecoveryPasswordForm
    template_name = 'usersapp/recovery_password_form.html'
    success_url = reverse_lazy("usersapp:login")

    def form_valid(self, form):
        if self.request.method == 'POST':
            user_email = self.request.POST['email']
            try:
                user = User.objects.get(email=user_email)
                new_password = ''.join([random.choice(string.digits + string.ascii_letters) for _ in range(0, 10)])
                user.set_password(new_password)
                user.save()
                send_mail(
                    subject='Восстановление пароля',
                    message=f'Для входа используйте новый пароль: {new_password}',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
            except User.DoesNotExist:
                form.add_error(None, User.DoesNotExist(f"Пользователь {user_email} не найден"))
                return self.render_to_response(self.get_context_data(form=form))

        return redirect(reverse('usersapp:login'))


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Контроллер для вывода списка пользователей.
    """

    model = User
    permission_required = 'usersapp.view_user'


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Контроллер для удаления пользователя.
    """

    model = User
    success_url = reverse_lazy('usersapp:user_list')
    permission_required = 'usersapp.delete_user'
