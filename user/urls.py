from django.contrib import admin
from django.urls import path, include
from .views import SignUpView, SignInView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



# user/
urlpatterns = [
    path('sign-up', SignUpView.as_view()),
    path('sign-in', SignInView.as_view()),
    
    path('api/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    
]
