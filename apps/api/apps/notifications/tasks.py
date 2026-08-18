from celery import shared_task
from .models import Notification
from apps.accounts.models import User

@shared_task
def send_notification_task(user_id: str, title: str, message: str, link: str = "", notification_type: str = "SYSTEM"):
    try:
        user = User.objects.get(id=user_id)
        Notification.objects.create(
            recipient=user,
            title=title,
            message=message,
            link=link,
            notification_type=notification_type
        )
        # Email dispatch could be added here
        return True
    except User.DoesNotExist:
        return False
