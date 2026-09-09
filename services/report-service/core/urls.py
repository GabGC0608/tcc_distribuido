from django.urls import path
from .views import Overview,Metrics
urlpatterns=[path("reports/overview",Overview.as_view()),path("reports/metrics",Metrics.as_view())]
