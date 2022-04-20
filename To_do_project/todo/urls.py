from . import views 
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (TaskCreateView,TaskDeleteView,TaskUpdateView,status)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('home/', views.home,name='todo-home'),
    path('history/', views.history,name='history-page'),
    path('',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('register/', views.register,name='register'),  
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='login.html'),name='logout'),
        
    path('TaskData/new/', TaskCreateView.as_view(template_name='TaskData_form.html'), name='task-create'),
    #path('add', views.add),
    path('taskdetail/<int:pk>/', views.taskdetail, name='task-detail'),
    # path('taskdelete/<int:pk>/', views.taskdelete, name='task-delete'),
    path('taskdelete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('taskdetail/<int:pk>/update', TaskUpdateView.as_view(), name='task-update'),
    path('history/<int:pk>',status,name='history'),
    path('profile/', views.profile, name='profile'),
    path('task-csv/', views.to_csv, name='task-csv'),
    path('task-pdf/', views.to_pdf, name='task-pdf'),
 
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)