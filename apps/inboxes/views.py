from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from apps.accounts.models import User
from apps.inboxes.models import InboxMessage


class InboxMessageView(LoginRequiredMixin, View):
    template_name = "inboxes/lobby_v2.html"

    def get(self, request, **kwargs):
        user = request.user
        received_messages = InboxMessage.objects.filter(msg_receiver=user)
        sent_messages = InboxMessage.objects.filter(msg_sender=user)

        # Combine both lists of users
        all_users = User.objects.filter(
            Q(pk__in=InboxMessage.objects.filter(msg_receiver=user).values_list('msg_sender', flat=True)) |
            Q(pk__in=InboxMessage.objects.filter(msg_sender=user).values_list('msg_receiver', flat=True))
        ).distinct()

        message_threads = []

        for other_user in all_users:
            # Get the messages sent to and received from the other user
            messages_sent = sent_messages.filter(msg_receiver=other_user)
            messages_received = received_messages.filter(msg_sender=other_user)

            # Calculate the number of "is_seen" messages
            seen_messages_count = messages_sent.filter(is_seen=False).count()

            # Get the last message
            last_message = messages_sent.union(messages_received).latest("sent_at")

            message_threads.append({
                "other_user": other_user,
                "messages_sent": messages_sent,
                "messages_received": messages_received,
                "seen_messages_count": seen_messages_count,
                "last_message": last_message,
            })
        context = {
            'received_messages': received_messages,
            'sent_messages': sent_messages,
            'all_users': all_users,
            'message_threads': message_threads
        }
        return render(request, self.template_name, context)


class GetUserAndMessages(View):

    def get(self, request):
        if request.method == 'GET':
            if sid := request.GET.get('sid', None):

                # Fetch the user based on 'sid' (replace this with your logic)
                user = User.objects.get(id=sid)

                # Fetch messages related to the current user and the fetched user
                messages = InboxMessage.objects.filter(
                    Q(msg_sender=request.user, msg_receiver=user) |
                    Q(msg_sender=user, msg_receiver=request.user)
                ).order_by('sent_at')

                # Update all messages to set is_seen=True
                messages.update(is_seen=True)

                # Prepare data to send back to the frontend
                user_data = {
                    'id': user.id,
                    'username': user.username.title(),
                    'full_name': user.full_name,
                    'img': user.profile.image_url,
                    'online_status': user.is_online,
                    'last_visit': naturaltime(user.last_visit)
                }

                messages_data = [
                    {
                        'sender_id': msg.msg_sender.id,
                        'receiver_id': msg.msg_receiver.id,
                        'message': msg.message,
                        'sent_at': naturaltime(msg.sent_at),
                    }
                    for msg in messages
                ]

                return JsonResponse({
                    'user': user_data,
                    'messages': messages_data,
                })
        return JsonResponse({'error': 'Invalid request'}, status=400)


class SendDirectMessage(View):

    # Send Direct message to user
    def post(self, request, **kwargs):
        from_user = request.user
        print(f"""
            to_user: {request.POST.get('to_user')}
            msg_content: {request.POST.get('message')}
        """)
        to_user = User.objects.get(username=request.POST.get('to_user').lower())
        if msg_content := request.POST.get('message'):
            msg = InboxMessage.objects.create(
                msg_sender=from_user,
                msg_receiver=to_user,
                message=msg_content
            )
            msg.save()
        return JsonResponse({
            "status": "success",
            "message": "Message sent successfully",
            "msg_content": msg_content,
            "msg_time": naturaltime(timezone.now())
        })
