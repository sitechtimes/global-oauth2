from django.urls import path
from .views import signup, verify, get_user, change_password, forgot_password

urlpatterns = [
    path('signup', signup, name='signup'),
    path('change_password', change_password, name='change_password'),
    path('forgot_password', forgot_password, name='forgot_password'),
    path('verify/', verify, name='verify'),
    path('get_user', get_user, name='get_user')
]
