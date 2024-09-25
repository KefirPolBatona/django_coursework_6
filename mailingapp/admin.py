from django.contrib import admin

from mailingapp.models import Client, Mailing, Message, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email_client', 'first_name', 'last_name',
        'middle_name', 'comment_client', 'user',
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'created_at', 'start_mailing', 'end_mailing',
        'periodic_mailing', 'status_mailing', 'user', 'is_disabled', 'message',
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'message_title', 'message_text', 'user',
    )


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'last_attempt', 'status_attempt', 'answer_mail_server', 'mailing',
    )