from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm

from mailingapp.forms import StyleFormMixin
from usersapp.models import User


class UserRegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    """
    Форма профиля пользователя.
    """

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone',)

    def __init__(self, *args, **kwargs):
        """
        Исключает из формы профиля техническое сообщение о паролях:
        'Пароль не задан. Пароли хранятся в зашифрованном виде...'.
        """
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserRecoveryPasswordForm(StyleFormMixin, PasswordResetForm):
    """
    Форма для восстановления пароля пользователя.
    """

    class Meta:
        model = User
        fields = ('email',)
