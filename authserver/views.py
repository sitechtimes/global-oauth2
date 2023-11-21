from django.shortcuts import render, redirect
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from .forms import SignUpForm

# Create your views here.


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
            # this should redirect to the login page.
            # not sure how that would work with django-oauth-toolkit
            # have to worry about original redirect link
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})