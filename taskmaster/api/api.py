from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Case, When, Value
import json
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from ..forms.forms import *
from ..models import *
from ..serializers.serializers import *
from drf_yasg.utils import swagger_auto_schema


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Task operations.
    """
    serializer_class = TaskSerializer

    # permission class set to be unauthenticated
    permission_classes = (permissions.AllowAny,)

    # this is where the drf-yasg gets invoked
    @swagger_auto_schema(request_body=serializer_class)
    def get_queryset(self):
        """
        Get the queryset for Task model based on query parameters.

        This method retrieves tasks from the database and filters them based on the query parameters provided in the request.
        It supports filtering by user ID, task type (daily, weekly, monthly), completion status, execution day, and execution date.

        Returns:
            QuerySet: A filtered queryset of Task objects.
        """
        # Retrieve all Task objects from the database
        queryset = Task.objects.all()

        # Extract query parameters from the request
        user_id = self.request.query_params.get(
            'user_id')  # User ID to filter tasks by user
        daily = self.request.query_params.get(
            'daily')  # Filter for daily tasks
        weekly = self.request.query_params.get(
            'weekly')  # Filter for weekly tasks
        monthly = self.request.query_params.get(
            'monthly')  # Filter for monthly tasks
        completed = self.request.query_params.get(
            'completed')  # Filter for completed tasks
        # Filter by execution day (e.g., Monday)
        days = self.request.query_params.get('days')
        # Filter by execution date (e.g., 15)
        date = self.request.query_params.get('date')

        # Ensure user_id is an integer
        if user_id is not None:
            try:
                user_id = int(user_id)  # Convert user_id to integer
            except ValueError:
                # Raise a 404 error if user_id is not a valid integer
                raise Http404

        # Ensure date is an integer
        if date is not None:
            try:
                date = int(date)  # Convert date to integer
            except ValueError:
                # Raise a 404 error if date is not a valid integer
                raise Http404

        # Ensure days is within the allowed list of weekdays
        allowed_days = ['Sunday', 'Monday', 'Tuesday',
                        'Wednesday', 'Thursday', 'Friday', 'Saturday']
        if days and days.capitalize() not in allowed_days:
            raise Http404

        # Ensure date is within the allowed range (1 to 31)
        if date and int(date) not in range(1, 32):
            raise Http404

        # Apply filters to the queryset based on query parameters
        if user_id:
            queryset = queryset.filter(user=user_id)  # Filter tasks by user ID
        if daily == 'true':
            queryset = queryset.filter(daily=True)  # Filter for daily tasks
            # Order by completion status and execution time
            queryset = queryset.order_by('completed', 'execution_time')
        if weekly == 'true':
            queryset = queryset.filter(weekly=True)  # Filter for weekly tasks
            day_order = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3,
                         'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}
            queryset = queryset.order_by(
                'completed',
                Case(
                    *[When(execution_day=day, then=Value(order))
                      for day, order in day_order.items()],
                    default=8,
                    output_field=models.IntegerField()
                ),
                'execution_time',
            )
        if monthly == 'true':
            # Filter for monthly tasks
            queryset = queryset.filter(monthly=True)
            # Order by completion status, execution date, and time
            queryset = queryset.order_by(
                'completed', 'execution_date', 'execution_time')
        if completed == 'true':
            # Filter for completed tasks
            queryset = queryset.filter(completed=True)
        if days:
            # Filter by execution day
            queryset = queryset.filter(execution_day=days.capitalize())
        if date:
            # Filter by execution date
            queryset = queryset.filter(execution_date=date)

        return queryset

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Mark a task as completed or incomplete.

        Parameters:
            request: HTTP request object.
            pk: Primary key of the task.

        Returns:
            Response with serialized task data.
        """
        task = self.get_object()
        task.completed = not task.completed  # Toggle the 'completed' field
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)


def set_timezone(request):
    """
    Set the timezone for the user's profile.

    Parameters:
        request: HTTP request object.

    Returns:
        JsonResponse with success status.
    """
    if request.method == 'POST':
        # Get the JSON data from the request body
        data = json.loads(request.body)

        # Extract the timeZone value from the JSON data
        time_zone = data.get('timeZone')
        # Get the user's profile or create it if it doesn't exist
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if created:
            profile = profile[0]  # Access the created profile from the tuple
        profile.timezone = time_zone
        profile.save()

        return JsonResponse({'success': True})


def check_username_availability(request):
    """
    Check the availability of a username.

    Parameters:
        request: HTTP request object.

    Returns:
        JsonResponse with is_available status.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        response_data = {'is_available': not User.objects.filter(
            username=username).exists()}
        return JsonResponse(response_data)
    return JsonResponse({'is_available': False})
