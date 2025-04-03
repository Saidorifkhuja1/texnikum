from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser

from core.paginations import CustomPageNumberPagination
from .models import *
from .serializers import *


class NewsCreateView(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # Automatically set the author field to the current authenticated user
        news_instance = serializer.save(author=self.request.user)
        return news_instance

    def create(self, request, *args, **kwargs):
        # Call the default create method to save the new instance
        response = super().create(request, *args, **kwargs)

        # The response now includes the 'uid' because it's part of the serializer's fields
        return response

class NewsRetrieveView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'uid'
    # permission_classes = [IsAdminUser]


class NewsUpdateView(generics.UpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'uid'
    parser_classes = [MultiPartParser, FormParser]


class NewsDeleteView(generics.DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'uid'
    permission_classes = [IsAdminUser]


class NewsListView(generics.ListAPIView):
    queryset = News.objects.all().order_by('-uploaded_at')
    serializer_class = NewsSerializer
    pagination_class = CustomPageNumberPagination
    # permission_classes = [IsAdminUser]
