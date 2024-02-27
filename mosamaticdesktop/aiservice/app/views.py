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
    """
    This endpoint returns a list of task configurations. Each task configuration
    contains the task name and its parameters (names and types). 
    """
    manager = TaskWidgetManager(None)
    taskNames = manager.taskNames()
    taskWidgets = manager.taskWidgets()
    data = {}
    for taskName in taskNames:
        data[taskName] = []
        for taskParameter in taskWidgets[taskName].taskParameterWidgets():
            data[taskName].append(taskParameter.toDict())
    return Response({'tasks': data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task(request, name):
    manager = TaskWidgetManager(None)
    taskWidget = manager.taskWidget(name=name)
    data = {name: []}
    for taskParameter in taskWidget.taskParameterWidgets():
        data[name].append(taskParameter.toDict())
    return Response(data, status=status.HTTP_200_OK)


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