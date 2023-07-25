from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import *
from ..serializers.serializers import *

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])  # Use JWTAuthentication for token-based authentication
@permission_classes([IsAuthenticated])  # Require authentication for this view
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == 'PUT':
        # Check if the user is authorized to edit the task
        if task.user != request.user:
            return Response({"error": "You are not authorized to edit this task."}, status=403)
        
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
