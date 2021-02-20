from django.urls import path
# from io_utils.views import UserViewSet, GroupViewSet
from .views import index, finite_automata, gramatics, regex, file_upload, update_af_file
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index),
    path('af', finite_automata),
    path('af/upload_file', file_upload, name='file_upload'),
    path('af/update_af_file/', update_af_file, name='update_af_file'),
    path('gr', gramatics),
    path('er', regex)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
