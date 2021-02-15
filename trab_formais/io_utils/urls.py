from django.urls import path

from io_utils.views import UserViewSet, GroupViewSet, index

urlpatterns = [
    path('index/', index ),
    path('user-view-set/', UserViewSet, name='user-view-set'), # just a test url
    path('group-view-set/', GroupViewSet, name='group-view-set'), # just a test url
]