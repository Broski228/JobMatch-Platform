from .models import Notification

def ui_context(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications_count': Notification.objects.filter(worker=request.user, is_read=False).count()
        }
    return {'unread_notifications_count': 0}
