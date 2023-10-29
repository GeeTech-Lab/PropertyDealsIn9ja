from django.db import models
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.common.models import TimeStampedUUIDModel
from apps.notifications.models import Notification


class InboxMessage(TimeStampedUUIDModel):
    # user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='user')
    msg_sender = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='from_user')
    msg_receiver = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='to_user')
    message = models.TextField(null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.msg_sender} -> {self.msg_receiver}"


@receiver(post_save, sender=InboxMessage)
def user_recieve_message(sender, instance, *args, **kwargs):
    msg = instance
    user = msg.msg_receiver
    sender = msg.msg_sender
    text_preview = msg.message[:50]
    message = f"You have a new message from {sender}..."
    notify = Notification(
        inbox_message=msg,
        from_user=sender,
        to_user=user,
        text_preview=text_preview,
        notification_type=3,
        message=message,
    )
    notify.save()
