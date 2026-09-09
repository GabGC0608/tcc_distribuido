from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns=[path("admin/",admin.site.urls),path("accounts/",include("allauth.urls")),path("api/",include("core.urls")),path("api/auth/refresh/",TokenRefreshView.as_view())]
