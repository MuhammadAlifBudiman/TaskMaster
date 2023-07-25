from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')

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

    #api
    path('api/', include(router.urls)),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('set-timezone/', views.set_timezone, name='set_timezone'),
    path('check_username_availability/', views.check_username_availability, name='check_username_availability'),
]
