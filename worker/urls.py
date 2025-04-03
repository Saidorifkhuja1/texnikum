from django.urls import path
from .views import *



urlpatterns = [
    path('worker_list/', WorkerListView.as_view()),
    path('create_worker/', WorkerCreateView.as_view()),
    path('worker_detail/<uuid:uid>/', WorkerRetrieveView.as_view()),
    path('update_worker/<uuid:uid>/', WorkerUpdateView.as_view()),
    path('delete_worker/<uuid:uid>/', WorkerDeleteView.as_view()),

]
