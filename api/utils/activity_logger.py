from django.utils.timezone import now

def log_activity(user, title, action, extra_info=None):
    """Logs activity to the ActivityLog model with optional additional info."""
    # Lazy import to avoid circular import issues
    from ..models import ActivityLog

    ActivityLog.objects.create(
        user=user,
        title=title,
        action=action,
        timestamp=now(),
        #extra_info=extra_info  # Optional field for extra information (like model details)
    )
