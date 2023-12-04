from django.urls import path
from .views import signup, verify

urlpatterns = [
    path('signup', signup, name='signup'),
    path('verify/<int:code>/', verify, name='verify')
]
