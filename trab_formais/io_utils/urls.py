from django.urls import path
# from ine5421.views import UserViewSet, GroupViewSet
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),

    path('af', views.finite_automata),
    path('af/update_or_upload', views.update_or_upload_af, name='options_af'),
    path('af/upload_af_file', views.upload_af_file, name='upload_af'),
    path('af/download_af_file', views.download_af_file, name='download_af'),
    path('af/update_af_file/', views.update_af_file, name='update_af'),
    path('af/convert_to_gr/', views.download_converted_gr, name='convert_to_gr'),
    path('af/determinize/', views.determinize, name='determinize'),
    path('af/minimize/', views.minimize, name='minimize'),
    path('af/recognize/', views.recognize, name='recognize'),

    path('er', views.regular_expression),
    path('er/update_or_upload', views.update_or_upload_er, name='options_er'),
    path('er/upload_er_file', views.upload_er_file, name='upload_er'),
    path('er/download_er_file', views.download_er_file, name='download_er'),
    path('er/update_er_file/', views.update_er_file, name='update_er'),
    path('er/convertER_to_af/', views.convertER_to_af, name='convertER_to_af'),

    path('gr', views.regular_grammar),
    path('gr/update_or_upload', views.update_or_upload_gr, name='options_gr'),
    path('gr/upload_gr_file', views.upload_gr_file, name='upload_gr'),
    path('gr/download_gr_file', views.download_gr_file, name='download_gr'),
    path('gr/update_gr_file/', views.update_gr_file, name='update_gr'),
    path('gr/convert_to_af/', views.download_converted_af, name='convert_to_af'),
    path('gr/parse/', views.parseGrammar, name='parse_grammar'),

    path('al', views.lexic_recognition),
    path('al/update_or_upload', views.update_or_upload_al, name='options_al'),
    path('al/upload_al_file', views.upload_al_file, name='upload_al'),
    path('al/download_al_file', views.download_al_file, name='download_al'),
    path('al/update_al_file/', views.update_al_file, name='update_al'),
    path('al/analyze_pseudocode/', views.analyze_pseudocode, name='analyze_pseudocode'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
