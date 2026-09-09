from django.urls import path
from .views import PublicList,PublicDetail,Download
urlpatterns=[path("repository/monographs",PublicList.as_view()),path("repository/monographs/<uuid:pk>",PublicDetail.as_view()),path("repository/monographs/<uuid:pk>/download",Download.as_view())]
