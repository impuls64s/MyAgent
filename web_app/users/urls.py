from django.urls import path
from .views import SignUp


urlpatterns = [
    path('create/', SignUp.as_view(), name='create_user'),
]