from django.shortcuts import render, redirect
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
import json
import uuid
from .models import User

from .forms import SignUpForm

# Create your views here.


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email_code = uuid.uuid4()
            user.save()
            response_data = {
                'user': user,
                'email-code': user.email_code
            }
            return JsonResponse(response_data)


def verify(request, code):
    user = User.objects.get(email_code=code)




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
