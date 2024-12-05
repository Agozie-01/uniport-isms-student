from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import now
from ..utils import log_activity

class ActivityLoggerMiddleware:
    """
    Middleware to log activities for every request made by the user.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("ActivityLoggerMiddleware is being called!")
        # Log activity for every request
        self.log_activity(request)
        
        # Proceed with the request processing
        response = self.get_response(request)
        return response

    def log_activity(self, request):
        """
        Logs the activity for every request.
        Logs the HTTP method, URL, and user performing the action.
        If the user is not authenticated, skips logging the activity.
        """
        # Check if the user is authenticated
        if request.user and not isinstance(request.user, AnonymousUser):
            user = request.user
        else:
            user = None  # No user or anonymous user, you can set to None or any default

        # Only log if there's a valid authenticated user
        if user:
            action = f"{request.method} request to {request.path}"
            title = f"Activity: {request.method} {request.path}"
            log_activity(user, title, action)
        else:
            print("Skipping activity log for anonymous or unauthenticated user.")
