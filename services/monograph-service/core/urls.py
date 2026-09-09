from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import *
r=DefaultRouter(); r.register("courses",CourseViewSet); r.register("professors",ProfessorViewSet); r.register("students",StudentViewSet); r.register("monographs",MonographViewSet)
urlpatterns=[path("",include(r.urls))]
