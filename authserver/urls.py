from django.urls import path
from .views import signup, verify, LoginView
from .forms import LoginForm

urlpatterns = [
    path('signup', signup, name='signup'),
    path('verify/', verify, name='verify'),
    path('login', LoginView.as_view(authentication_form=LoginForm), name="login")
]
