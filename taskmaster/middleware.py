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
        # Initialize the middleware with the next middleware or view function in the chain.
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
        # Check if the user is authenticated.
        if request.user.is_authenticated:
            # Retrieve or create a UserProfile for the authenticated user.
            userprofile, _ = UserProfile.objects.get_or_create(
                user=request.user)

            # Get the timezone from the user's profile.
            user_timezone = userprofile.timezone

            # Activate the user's timezone for the current request.
            timezone.activate(user_timezone)

        # Pass the request to the next middleware or view function and get the response.
        response = self.get_response(request)

        # Return the response to the client.
        return response
