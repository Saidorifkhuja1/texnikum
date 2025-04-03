from django.urls import path
from .views import *



urlpatterns = [
    path('register/', SendVerificationCodeAPIView.as_view(), name='send-code'),
    path('verify_code/', VerifyCodeAPIView.as_view(), name='verify-code'),
    path('user/reset-password/', PasswordResetRequestView.as_view(), name='reset-password'),
    path('user/reset-password/confirm/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),


    path('login/', CustomTokenObtainPairView.as_view()),
    path('profile_details/', RetrieveProfileView.as_view()),
    path('update_profile/<uuid:uid>/', UpdateProfileView.as_view()),
    path('update_password/', PasswordUpdate.as_view()),
    path('delete_profile/<uuid:uid>/', DeleteProfileAPIView.as_view()),

]


