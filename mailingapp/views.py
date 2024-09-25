from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView

from blogapp.models import Article
from mailingapp.forms import MailingForm, ClientForm, MessageForm
from mailingapp.models import Mailing, Message, Client, Attempt


class IndexView(TemplateView):
    """
    Контроллер для вывода главной страницы.
    """

    template_name = "mailingapp/index.html"

    def get_context_data(self, **kwargs):
        """
        Возвращает кол-во всего рассылок, активных рассылок, уникальных клиентов и 3 случайных статьи из блога.
        """

        context = super().get_context_data(**kwargs)
        context['mailing_count'] = Mailing.objects.all().count()
        context['mailing_active_count'] = Mailing.objects.all().filter(status_mailing='launched')\
            .filter(is_disabled=False).count()
        context['client_count'] = Client.objects.all().count()
        context["article_order_list"] = Article.objects.order_by('?')[:3]
        return context


class MailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Контроллер для вывода списка рассылок.
    """

    model = Mailing
    permission_required = 'mailingapp.view_mailing'

    def get_queryset(self, *args, **kwargs):
        """
        Фильтрует рассылки в зависимости от прав доступа пользователя.
        """

        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            if not user.is_superuser and not user.has_perm('usersapp.сan_block_user') \
                    and user.has_perm('mailingapp.view_mailing'):
                queryset = queryset.filter(user=user)
            return queryset
        raise PermissionDenied


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Контроллер для создания рассылки.
    """

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailingapp:mailing_list')
    permission_required = 'mailingapp.add_mailing'

    def get_form(self, form_class=None):
        """
        Возвращает в форму создания рассылки список клиентов и список сообщений
        в зависимости прав доступа пользователя.
        """

        user = self.request.user
        form = super().get_form(form_class)
        if user.is_superuser:
            form.fields['message'].queryset = Message.objects
            form.fields['clients'].queryset = Client.objects
        else:
            form.fields['message'].queryset = Message.objects.filter(user=user)
            form.fields['clients'].queryset = Client.objects.filter(user=user)

        return form

    def form_valid(self, form, **kwargs):
        """
        Привязывает пользователя к рассылке.
        """

        mailing = form.save()
        mailing.user = self.request.user
        mailing.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Контроллер для изменения рассылки.
    """

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailingapp:mailing_list')
    permission_required = 'mailingapp.change_mailing'

    def get_form(self, form_class=None):
        """
        Возвращает в форму изменений рассылки список клиентов и список сообщений
        в зависимости прав доступа пользователя.
        """

        user = self.request.user
        form = super().get_form(form_class)
        if user.is_superuser:
            form.fields['message'].queryset = Message.objects
            form.fields['clients'].queryset = Client.objects
        else:
            form.fields['message'].queryset = Message.objects.filter(user=user)
            form.fields['clients'].queryset = Client.objects.filter(user=user)

        return form


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Контроллер для просмотра рассылки.
    """

    model = Mailing
    permission_required = 'mailingapp.view_mailing'

    def get_context_data(self, **kwargs):
        """
        Отображает попытки рассылок.
        """

        user = self.request.user
        context_data = super().get_context_data(**kwargs)
        if user.is_authenticated:
            if user.is_superuser \
                    or user.has_perm('mailingapp.view_mailing') \
                    or user.id == self.object.user_id:
                context_data['attempts'] = Attempt.objects.filter(mailing=self.object).order_by('-last_attempt')
                return context_data
        raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер для удаления рассылки.
    """

    model = Mailing
    permission_required = 'mailingapp.delete_mailing'
    success_url = reverse_lazy('mailingapp:client_list')


@login_required
@permission_required('mailingapp.сan_disabled_mailings')
def disabled_mailing(request, pk):
    """
    Контроллер для отключения рассылки.
    """

    mailing_item = get_object_or_404(Mailing, pk=pk)
    if mailing_item.is_disabled:
        mailing_item.is_disabled = False
    else:
        mailing_item.is_disabled = True

    mailing_item.save()

    return redirect(reverse('mailingapp:mailing_detail', args=[pk])) # возвращает страницу измененной рассылки


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Контроллер для вывода списка клиентов.
    """

    model = Client
    permission_required = 'mailingapp.view_client'

    def get_queryset(self, *args, **kwargs):
        """
        Фильтрует клиентов в зависимости от прав доступа пользователя.
        """

        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            if not user.is_superuser or not user.has_perm('mailingapp.view_client'):
                queryset = queryset.filter(user=self.request.user)
            return queryset
        raise PermissionDenied


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Контроллер для создания клиента.
    """

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailingapp:client_list')
    permission_required = 'mailingapp.add_client'

    def form_valid(self, form, **kwargs):
        """
        Привязывает клиента к пользователю.
        """

        client = form.save()
        client.user = self.request.user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Контроллер для изменения сведений о клиенте.
    """

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailingapp:client_list')
    permission_required = 'mailingapp.change_client'


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Контроллер для просмотра информации о клиенте.
    """

    model = Client
    permission_required = 'mailingapp.view_client'


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Контроллер для удаления клиента.
    """

    model = Client
    success_url = reverse_lazy('mailingapp:client_list')
    permission_required = 'mailingapp.delete_mailing'


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Контроллер для вывода списка сообщений.
    """

    model = Message
    permission_required = 'mailingapp.view_message'

    def get_queryset(self, *args, **kwargs):
        """
        Фильтрует сообщения в зависимости от прав доступа пользователя.
        """

        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            if not user.is_superuser or not user.has_perm('mailingapp.view_message'):
                queryset = queryset.filter(user=self.request.user)
            return queryset
        raise PermissionDenied


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Контроллер для создания сообщения.
    """

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailingapp:message_list')
    permission_required = 'mailingapp.add_message'

    def form_valid(self, form, **kwargs):
        """
        Привязывает сообщение к пользователю.
        """

        message = form.save()
        message.user = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Контроллер для изменения сообщения.
    """

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailingapp:message_list')
    permission_required = 'mailingapp.change_message'


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Контроллер для просмотра информации о клиенте.
    """

    model = Message
    permission_required = 'mailingapp.view_message'


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Контроллер для удаления клиента.
    """

    model = Message
    success_url = reverse_lazy('mailingapp:message_list')
    permission_required = 'mailingapp.delete_mailing'


class AttemptDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Контроллер для просмотра информации о попытке.
    """

    model = Attempt
    permission_required = 'mailingapp.view_mailing'


class AttemptListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Контроллер для вывода списка попыток.
    """

    model = Attempt
    permission_required = 'mailingapp.view_mailing'
