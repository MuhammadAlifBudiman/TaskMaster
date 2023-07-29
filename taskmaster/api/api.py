from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Case, When, Value
import json
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from ..forms.forms import *
from ..models import *
from ..serializers.serializers import *

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        user_id = self.request.query_params.get('user_id')
        daily = self.request.query_params.get('daily')
        weekly = self.request.query_params.get('weekly')
        monthly = self.request.query_params.get('monthly')
        completed = self.request.query_params.get('completed')
        days = self.request.query_params.get('days')
        date = self.request.query_params.get('days')

        if user_id:
            queryset = queryset.filter(user=user_id)
        if daily == 'true':
            queryset = queryset.filter(daily=True)
            queryset = queryset.order_by('completed', 'execution_time')
        if weekly == 'true':
            queryset = queryset.filter(weekly=True)
            day_order = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}
            queryset = queryset.order_by('completed', 
                                         Case(
                                             *[When(execution_day=day, then=Value(order)) for day, order in day_order.items()],
                                             default=8,
                                             output_field=models.IntegerField()
                                         ),
                                         'execution_time',
                                         )
        if monthly == 'true':
            queryset = queryset.filter(monthly=True)
            queryset = queryset.order_by('completed','execution_date', 'execution_time')
        if completed == 'true':
            queryset = queryset.filter(completed=True)
        if days:
            queryset = queryset.filter(execution_day=days.capitalize())
        if date:
            queryset = queryset.filter(execution_date=date)

        return queryset

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.completed = not task.completed  # Toggle the 'completed' field
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data)


def set_timezone(request):
    """
    docstirng for documentations
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

        # Set the time zone for the current request
        timezone.activate(time_zone)
        return JsonResponse({'success': True})


def check_username_availability(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        response_data = {'is_available': not User.objects.filter(username=username).exists()}
        return JsonResponse(response_data)
    return JsonResponse({'is_available': False})