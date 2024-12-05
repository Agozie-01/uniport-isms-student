# api/mixins.py
from django.utils.timezone import now
from .utils import log_activity
from django.contrib.auth.models import AnonymousUser

class ActivityLogMixin:
    """
    Mixin to log user activity before view actions.
    This will log the HTTP method, path, and user performing the action.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Intercepts the request and logs the activity before
        calling the actual view logic.
        """
        self.log_activity(request)
        return super().dispatch(request, *args, **kwargs)

    def log_activity(self, request):
        """
        Logs the activity for every request.
        Logs the HTTP method, URL, and user performing the action.
        """
        user = request.user if not isinstance(request.user, AnonymousUser) else None  # Only log the user if authenticated
        print(request.user)
        if user:
            action = f"{request.method} request to {request.path}"
            title = f"Activity: {request.method} {request.path}"
            log_activity(user, title, action)
