from django.contrib import admin
from .models import AccessToken, RefreshToken, AuthorizationCode, User

# Register your models here.

admin.site.register(AccessToken)
admin.site.register(RefreshToken)
admin.site.register(AuthorizationCode)
admin.site.register(User)
