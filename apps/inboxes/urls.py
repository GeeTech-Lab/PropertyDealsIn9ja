from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from apps.inboxes import views


urlpatterns = [
    path('', views.InboxMessageView.as_view(), name='inbox_msg'),
    # path('<str:username>/', csrf_exempt(views.DirectMessage.as_view()), name='direct_msg'),
    path('get_user_and_messages/', csrf_exempt(views.GetUserAndMessages.as_view()), name='get_user_and_messages'),
    path('send_direct_msg/', csrf_exempt(views.SendDirectMessage.as_view()), name='send_direct_msg'),
]
