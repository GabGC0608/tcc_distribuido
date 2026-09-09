from django.urls import path
from .views import RegisterView,LoginView,MeView,AuditView
urlpatterns=[path("auth/register/",RegisterView.as_view()),path("auth/login/",LoginView.as_view()),path("auth/me/",MeView.as_view()),path("auth/audit/",AuditView.as_view())]
