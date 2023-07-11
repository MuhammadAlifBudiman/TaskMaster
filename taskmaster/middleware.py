from django.utils import timezone
from .models import UserProfile

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            userprofile = UserProfile.objects.get(user=request.user)
            user_timezone = userprofile.timezone

            # Activate the user's timezone
            timezone.activate(user_timezone)

        response = self.get_response(request)

        return response
