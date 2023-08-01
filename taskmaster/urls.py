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
      title="Task Master API",
      default_version='v1',
      description="An API for managing tasks in Task Master application. It allows users to create, update, and delete tasks. Users can set daily and weekly tasks with reminders.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@dummy.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Create a router for the Task API views
router = DefaultRouter()
router.register(r'tasks', api.TaskViewSet, basename='task')

# Define URL patterns for the app
urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth_view, name='auth'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dailytask/', views.dailytask, name='dailytask'),
    path('weeklytask/', views.weeklytask, name='weeklytask'),
    path('monthlytask/', views.monthlytask, name='monthlytask'),
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('mark-complete/<int:task_id>/', views.mark_task_complete, name='mark_task_complete'),
    path('export/', views.export_task_to_excel, name='export'),

    # API endpoints
    path('api/', include(router.urls)),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('set-timezone/', api.set_timezone, name='set_timezone'),
    path('check_username_availability/', api.check_username_availability, name='check_username_availability'),

    # API documentation views
    path('api/playground/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
