from django.urls import path
from .views import NotificationList
urlpatterns=[path("notifications/",NotificationList.as_view())]
