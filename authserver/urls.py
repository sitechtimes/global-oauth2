from django.urls import path
from .views import signup, verify, get_user

urlpatterns = [
    path('signup', signup, name='signup'),
    path('verify/', verify, name='verify'),
    path('get_user', get_user, name='get_user')
]
