from django.urls import path
from .views import *

urlpatterns = [
    path('slide_list/', SlideListView.as_view()),
    path('slide/create/', SlideCreateView.as_view()),
    path('slide_detail/<uuid:uid>/', SlideRetrieveView.as_view()),
    path('update_slide/<uuid:uid>/', SlideUpdateView.as_view()),
    path('delete_slide/<uuid:uid>/', SlideDeleteView.as_view()),
]
