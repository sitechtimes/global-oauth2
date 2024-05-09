from django.shortcuts import render, redirect
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
import json
import uuid
from .models import User

from .forms import SignUpForm

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
            user.uuid = uuid.uuid4()
            user.graduating_year = request.POST['graduating_year']
            user.save()
            response_data = {
                'email-code': f"http://127.0.0.1:8000/users/verify/?code={user.uuid}"
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


@login_required()
def get_user(request, *args, **kwargs):
    user = request.user
    response_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'uuid': user.uuid
    }
    return JsonResponse(response_data)


# >>>> club attendance routes
@permission_required('authserver.club_attendance_admin')
def verify_club_admin(request, *args, **kwargs):
    response_data = {
        'is_admin': True
    }
    return JsonResponse(response_data)