"""
This module defines the URL patterns for the TaskMaster application. It includes routes for both the web application and the API endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .api import api
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define the API schema view for documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Task Master API",  # Title of the API documentation
        default_version='v1',  # Version of the API
        description="An API for managing tasks in Task Master application. It allows users to create, update, and delete tasks. Users can set daily and weekly tasks with reminders.",  # Description of the API
        terms_of_service="https://www.google.com/policies/terms/",  # Terms of service URL
        # Contact information for the API
        contact=openapi.Contact(email="alifm2101@gmail.com"),
        license=openapi.License(name="BSD License"),  # License information
    ),
    public=True,  # Indicates that the schema is publicly accessible
    # Permissions for accessing the schema
    permission_classes=(permissions.AllowAny,),
)

# Create a router for the Task API views
router = DefaultRouter()
# Register the TaskViewSet with the router
router.register(r'tasks', api.TaskViewSet, basename='task')

# Define URL patterns for the app
urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('auth/', views.auth_view, name='auth'),  # Authentication page
    path('auth/login/', views.login_view, name='login'),  # Login page
    path('auth/register/', views.register_view,
         name='register'),  # Registration page
    path('logout/', views.logout_view, name='logout'),  # Logout functionality
    path('dailytask/', views.dailytask, name='dailytask'),  # Daily tasks page
    path('weeklytask/', views.weeklytask,
         name='weeklytask'),  # Weekly tasks page
    path('monthlytask/', views.monthlytask,
         name='monthlytask'),  # Monthly tasks page
    path('add/', views.add_task, name='add_task'),  # Add a new task
    path('edit/<int:task_id>/', views.edit_task,
         name='edit_task'),  # Edit an existing task
    path('delete/<int:task_id>/', views.delete_task,
         name='delete_task'),  # Delete a task
    path('mark-complete/<int:task_id>/', views.mark_task_complete,
         name='mark_task_complete'),  # Mark a task as complete
    # Export tasks to an Excel file
    path('export/', views.export_task_to_excel, name='export'),

    # API endpoints
    path('api/', include(router.urls)),  # Include API routes from the router
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),  # Refresh JWT token
    path('set-timezone/', api.set_timezone,
         name='set_timezone'),  # Set user timezone
    path('check_username_availability/', api.check_username_availability,
         name='check_username_availability'),  # Check if a username is available

    # API documentation views
    path('api/playground/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  # Swagger UI for API documentation
    path('api/docs/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),  # Redoc UI for API documentation
]
