from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth_view, name='auth'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dailytask/', views.dailytask, name='dailytask'),
    path('weeklytask/', views.weeklytask, name='weeklytask'),
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('mark-complete/<int:task_id>/', views.mark_task_complete, name='mark_task_complete'),
    path('set-timezone/', views.set_timezone, name='set_timezone'),
]
