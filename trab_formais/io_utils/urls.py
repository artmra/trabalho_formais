from django.urls import path
# from io_utils.views import UserViewSet, GroupViewSet
from io_utils import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('af', views.finite_automata),
    path('af/upload_file', views.upload_file, name='upload_file'),
    path('af/download_file', views.download_file, name='download_file'),
    path('af/update_af_file/', views.update_af_file, name='update_af_file'),
    path('gr', views.gramatics),
    path('er', views.regex)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
