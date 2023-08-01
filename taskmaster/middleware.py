from django.utils import timezone
from .models import UserProfile

class TimezoneMiddleware:
    """
    Middleware to activate the user's timezone based on their UserProfile settings.

    This middleware checks if the user is authenticated and has a UserProfile.
    If a UserProfile exists for the user, it activates the user's timezone
    using Django's timezone.activate() method.

    This allows subsequent code to work with datetimes in the user's timezone.

    Parameters:
        get_response (function): The next middleware in the chain or the view function.

    Returns:
        function: The response from the next middleware or the view function.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Middleware process for activating the user's timezone.

        If the user is authenticated and has a UserProfile, the middleware
        activates the user's timezone using Django's timezone.activate() method.

        Parameters:
            request (HttpRequest): The current request object.

        Returns:
            HttpResponse: The response from the next middleware or the view function.
        """
        if request.user.is_authenticated:
            userprofile, _ = UserProfile.objects.get_or_create(user=request.user)
            user_timezone = userprofile.timezone

            # Activate the user's timezone
            timezone.activate(user_timezone)

        response = self.get_response(request)

        return response
