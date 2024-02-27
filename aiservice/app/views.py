from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRegistrationSerializer

from mosamaticdesktop.tasks.taskwidgetmanager import TaskWidgetManager

User = get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
def api(request):
    return render(request, 'api.html')


@api_view(['POST'])
@permission_classes([AllowAny])
def registerUser(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tasks(request):
    manager = TaskWidgetManager(None)
    taskNames = manager.taskNames()
    print(taskNames)
    return Response({'tasks': taskNames}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createTask(request, name):
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadDataToTask(request, taskId):
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taskStatus(request, taskId):
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def downloadResultsFromTask(request, taskId):
    pass