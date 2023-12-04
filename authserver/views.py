from django.shortcuts import render, redirect
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
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
            'password2': request.POST['password']
        }
        form = SignUpForm(body)
        if form.is_valid():
            user = form.save()
            user.email_code = uuid.uuid4()
            user.save()
            response_data = {
                'email-code': f"http://127.0.0.1:8000/users/verify/{user.email_code}"
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'errors': form.errors})
    else:
        raise PermissionDenied


@csrf_exempt
def verify(request, code):
    user = User.objects.get(email_code=code)
    user.verified = True
    user.save()
    return JsonResponse({'verified': True})





# def signup(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#             # this should redirect to the login page.
#             # not sure how that would work with django-oauth-toolkit
#             # have to worry about original redirect link
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/signup.html', {'form': form})
