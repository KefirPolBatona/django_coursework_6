from django import forms
from django.forms import BooleanField

from mailingapp.models import Mailing, Client, Message


class StyleFormMixin:
    """
    Класс для стилизации форм.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


class MailingForm(StyleFormMixin, forms.ModelForm):
    """
    Форма создания/изменения рассылки.
    """

    class Meta:
        model = Mailing
        fields = ('start_mailing', 'end_mailing', 'periodic_mailing',
                  'status_mailing', 'clients', 'message',
                  )


class ClientForm(StyleFormMixin, forms.ModelForm):
    """
    Форма создания/изменения клиента.
    """

    class Meta:
        model = Client
        fields = ('email_client', 'first_name', 'last_name', 'middle_name', 'comment_client',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    """
    Форма создания/изменения сообщения.
    """

    class Meta:
        model = Message
        fields = ('message_title', 'message_text')
