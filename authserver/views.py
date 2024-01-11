from django.shortcuts import render, redirect
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import views as auth_views
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from .models import User

from .forms import SignUpForm, LoginForm

# Create your views here.

@csrf_exempt
def signup(request):
    if request.method == "POST":
        value = request.POST['email'].split("@")
        username = value[0]
        body = {
            'email': request.POST['email'],
            'username': username,
            'password1': request.POST['password'],
            'password2': request.POST['password'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name']
        }
        form = SignUpForm(body)
        if form.is_valid():
            user = form.save()
            user.email_code = uuid.uuid4()
            user.graduating_year = request.POST['graduating_year']
            user.save()
            response_data = {
                'email-code': f"http://127.0.0.1:8000/users/verify/?code={user.email_code}"
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'errors': form.errors})
    else:
        raise PermissionDenied


@csrf_exempt
def verify(request):
    code = request.GET.get('code', '')
    user = User.objects.get(email_code=code)
    if user:
        user.verified = True
        user.email_code = ''
        user.save()
        response_data = {
            'verified': True
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'errors': 'User does not exist'})

    # if request.method == "GET":
    #     code = request.GET.get('code', '')
    #     user = User.objects.get(email_code=code)
    #     user.verified = True
    #     user.save()
    #     return JsonResponse({'verified': True})
    # else:
    #     raise PermissionDenied


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
