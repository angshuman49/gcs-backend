from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Articles, Schedule, Notice
from .serializers import ArticlesSerializer, ScheduleSerializer, NoticeSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_content(request):
    content_type = request.query_params.get('type')
    if content_type == 'articles':
        queryset = Articles.objects.all().order_by('-created_at')
        serializer = ArticlesSerializer(queryset, many=True)
    elif content_type == 'schedule':
        queryset = Schedule.objects.all().order_by('day', 'timerange')
        serializer = ScheduleSerializer(queryset, many=True)
    elif content_type == 'notices':
        queryset = Notice.objects.all().order_by('-notified_at')
        serializer = NoticeSerializer(queryset, many=True)
    else:
        return Response({'error': 'Invalid type'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'data': serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check(req):
    return Response({'message':'dummy'}, status=status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dashboard_change(request):
    user = request.user
    if user.role != 'executive':
        return Response({'error': 'Permission denied. Executive role required.'},
                        status=status.HTTP_403_FORBIDDEN)

    data = request.data
    db_name = data.get('name_of_db')
    mode = data.get('mode')

    mapping = {
        'Articles': (Articles, ArticlesSerializer),
        'Schedule': (Schedule, ScheduleSerializer),
        'Notice': (Notice, NoticeSerializer),
    }
    if db_name not in mapping:
        return Response({'error': 'Invalid name_of_db'}, status=status.HTTP_400_BAD_REQUEST)

    model, serializer_class = mapping[db_name]

    if db_name == 'Schedule' and 'title' in data:
        data['event'] = data.pop('title')

    if mode == 'create':
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(serializer_class(instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif mode == 'update':
        obj_id = data.get('id')
        if not obj_id:
            return Response({'error': 'id required for update'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = model.objects.get(id=obj_id)
        except model.DoesNotExist:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializer_class(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif mode == 'delete':
        obj_id = data.get('id')
        if not obj_id:
            return Response({'error': 'id required for delete'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = model.objects.get(id=obj_id)
            instance.delete()
            return Response({'message': 'Deleted successfully'}, status=status.HTTP_200_OK)
        except model.DoesNotExist:
            return Response({'error': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({'error': 'Invalid mode'}, status=status.HTTP_400_BAD_REQUEST)
