
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('admin_feedback/', views.admin_feedback, name='admin_feedback'),
    path('admin_update_feedback_status_ajax/', views.admin_update_feedback_status_ajax, name='admin_update_feedback_status_ajax'),
    path('admin_feedback/<str:type>', views.admin_feedback, name='admin_feedback'),
    path('admin_feedback_detail/<int:id>', views.admin_feedback_detail, name='admin_feedback_detail'),
    #video
    path('admin_videos', views.admin_videos, name='admin_videos'),
    path('admin_videos/<int:type>', views.admin_videos, name='admin_videos'),
    path('admin_upload_video', views.admin_upload_video, name='admin_upload_video'),
    path('admin_delete_video_ajax', views.admin_delete_video_ajax, name='admin_delete_video_ajax'),
    #background music
    path('admin_music', views.admin_music, name='admin_music'),
    path('admin_upload_music', views.admin_upload_music, name='admin_upload_music'),
    path('admin_delete_music_ajax', views.admin_delete_music_ajax, name='admin_delete_music_ajax'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
