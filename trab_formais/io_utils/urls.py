from django.urls import path
# from io_utils.views import UserViewSet, GroupViewSet
from .views import index, finite_automata, gramatics, regex


urlpatterns = [
    path('', index),
    path('af', finite_automata),
    path('gr', gramatics),
    path('er', regex)
]