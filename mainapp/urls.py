
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('answer_questions/<int:type>', views.answer_questions, name='answer_questions'),
    path('review_script', views.review_script, name='review_script'),
    path('generate_voiceover', views.generate_voiceover, name='generate_voiceover'),
    path('generate_video', views.generate_video, name='generate_video'),
    path('generate_video_ajax', views.generate_video_ajax, name='generate_video_ajax'),
    path('update_user_status_ajax', views.update_user_status_ajax, name='update_user_status_ajax'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('sample_videos/', views.sample_videos, name='sample_videos'),
    path('pricing/', views.pricing, name='pricing'),
    path('contact/', views.contact, name='contact'),
    path('regenerate_script/', views.regenerate_script, name='regenerate_script'),
    path('logout/', views.logout, name='logout'),
    path('back_to_home/', views.back_to_home, name='back_to_home'),
    path('back_to_questions/', views.back_to_questions, name='back_to_questions'),
    path('upload_voice_record/', views.upload_voice_record, name='upload_voice_record'),
    path('upload_voice_file/', views.upload_voice_file, name='upload_voice_file'),
    path('final_result/', views.final_result, name='final_result'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('activate/(?P<uidb64>)/(?P<token>)/', 
         views.activate, name='activate'),
    # path('subscribe/', views.subscribe, name='subscribe'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
