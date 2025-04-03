from django.urls import path
from .views import *

urlpatterns = [
    path('comments_create/', CommentCreateAPIView.as_view()),
    path('comments/list/', CommentListAPIView.as_view()),
    path('comments/delete/<uuid:uid>/', CommentDeleteAPIView.as_view()),



]
