from django.urls import path
# from io_utils.views import UserViewSet, GroupViewSet
from io_utils import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),

    path('af', views.finite_automata),
    path('er', views.regular_expression),

    path('af/upload_af_file', views.upload_af_file, name='upload_af_file'),
    path('af/upload_er_file', views.upload_er_file, name='upload_er_file'),

    path('af/download_af_file', views.download_af_file, name='download_af_file'),
    path('af/download_er_file', views.download_er_file, name='download_er_file'),

    path('af/update_af_file/', views.update_af_file, name='update_af_file'),
    path('af/update_er_file/', views.update_er_file, name='update_er_file'),

    path('gr', views.gramatics),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
