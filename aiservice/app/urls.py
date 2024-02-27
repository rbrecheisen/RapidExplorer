from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import api, registerUser, tasks, createTask, uploadDataToTask, taskStatus, downloadResultsFromTask


urlpatterns = [
    path('', api),
    path('api/token', TokenObtainPairView.as_view()),
    path('api/token/refresh', TokenRefreshView.as_view()),
    path('api/users/register', registerUser),
    path('api/tasks/', tasks),
    path('api/tasks/create', createTask),
    path('api/tasks/<str:taskId>/upload', uploadDataToTask),
    path('api/tasks/<str:taskId>/status', taskStatus),
    path('api/tasks/<str:taskId>/download', downloadResultsFromTask),
]