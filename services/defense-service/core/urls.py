from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import DefenseViewSet,ExternalAccessView
r=DefaultRouter(); r.register("defenses",DefenseViewSet); r.register("external-access",ExternalAccessView,basename="external")
urlpatterns=[path("",include(r.urls))]
