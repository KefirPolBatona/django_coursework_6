from django.urls import path
from django.views.decorators.cache import cache_page

from mailingapp.apps import MailingappConfig
from mailingapp.views import MailingListView, MailingCreateView, MailingUpdateView, MailingDetailView, \
    MailingDeleteView, ClientListView, ClientCreateView, ClientUpdateView, ClientDetailView, ClientDeleteView, \
    MessageListView, MessageCreateView, MessageUpdateView, MessageDetailView, MessageDeleteView, IndexView, \
    disabled_mailing, AttemptDetailView, AttemptListView

app_name = MailingappConfig.name

urlpatterns = [
    path("", cache_page(10)(IndexView.as_view()), name='index'),

    path("mailing/list/", MailingListView.as_view(), name='mailing_list'),
    path("mailing/create/", MailingCreateView.as_view(), name='mailing_create'),
    path("mailing/update/<int:pk>/", MailingUpdateView.as_view(), name='mailing_update'),
    path("mailing/detail/<int:pk>/", MailingDetailView.as_view(), name='mailing_detail'),
    path("mailing/delete/<int:pk>/", MailingDeleteView.as_view(), name='mailing_delete'),

    path('disabled/<int:pk>/', disabled_mailing, name='mailing_disabled'),

    path("client/list/", ClientListView.as_view(), name='client_list'),
    path("client/create/", ClientCreateView.as_view(), name='client_create'),
    path("client/update/<int:pk>/", ClientUpdateView.as_view(), name='client_update'),
    path("client/detail/<int:pk>/", ClientDetailView.as_view(), name='client_detail'),
    path("client/delete/<int:pk>/", ClientDeleteView.as_view(), name='client_delete'),

    path("message/list/", MessageListView.as_view(), name='message_list'),
    path("message/create/", MessageCreateView.as_view(), name='message_create'),
    path("message/update/<int:pk>/", MessageUpdateView.as_view(), name='message_update'),
    path("message/detail/<int:pk>/", MessageDetailView.as_view(), name='message_detail'),
    path("message/delete/<int:pk>/", MessageDeleteView.as_view(), name='message_delete'),

    path("attempt/list/", AttemptListView.as_view(), name='attempt_list'),
    path("attempt/detail/<int:pk>/", AttemptDetailView.as_view(), name='attempt_detail'),
]

