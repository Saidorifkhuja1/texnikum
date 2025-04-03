from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from core.paginations import CustomPageNumberPagination
from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser

class WorkerCreateView(generics.CreateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class WorkerRetrieveView(generics.RetrieveAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    lookup_field = 'uid'
    # permission_classes = [IsAdminUser]


class WorkerUpdateView(generics.UpdateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    lookup_field = 'uid'
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class WorkerDeleteView(generics.DestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    lookup_field = 'uid'
    permission_classes = [IsAdminUser]


class WorkerListView(generics.ListAPIView):
    queryset = Worker.objects.all().order_by('-uid')
    serializer_class = WorkerSerializer
    pagination_class = CustomPageNumberPagination
    # permission_classes = [IsAdminUser]
