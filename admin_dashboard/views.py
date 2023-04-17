from django.shortcuts import render, redirect
from django.http import JsonResponse
from mainapp.models import Feedback, Media, Type
from mainapp.main_proc import get_video_type_directory, get_url, get_music_directory
import io
import os
# Create your views here.


def admin_home(request):
  context = {}
  selected_nav = "home"
  context["selected_nav"] = selected_nav
  return render(request, 'admin_dashboard/pages/home.html', context)

def admin_feedback(request, type = "all"):
  context = {}
  selected_nav = "feedback"
  context["selected_nav"] = selected_nav
  feedbacks = list()
  if type is "all":
    feedbacks = Feedback.objects.all()
  elif type is "read":
    feedbacks = Feedback.objects.filter(status = "read")
  else:
    feedbacks = Feedback.objects.filter(status = "unread")
  context["feedbacks"] = feedbacks
  return render(request, 'admin_dashboard/pages/feedback.html', context)

def admin_feedback_detail(request, id):
  context = {}
  selected_nav = "feedback"
  context["selected_nav"] = selected_nav
  feedback = Feedback.objects.get(id = id)
  feedback.status = "read"
  feedback.save()

  context["feedback"] = feedback
  return render(request, 'admin_dashboard/pages/feedback_detail.html', context)

def admin_update_feedback_status_ajax(request):
  id = request.POST.get("id")
  status = request.POST.get("status")
  feedback = Feedback.objects.get(id = id)
  feedback.status = status
  print(status)
  feedback.save()

  return JsonResponse({}, status=200)

#video
def admin_videos(request, type=0):
  context = {}
  selected_nav = "videos"
  context["selected_nav"] = selected_nav
  videos = list()
  if type == 0:
    videos = Media.objects.select_related('type').filter(media_type = "video")
  elif type == 1:
    videos = Media.objects.select_related('type').filter(media_type = "video", type = type)
  context["videos"] = videos
  types = Type.objects.all()
  context["types"] = types
  return render(request, 'admin_dashboard/pages/videos.html', context)

def admin_upload_video(request):
  print(request.FILES)
  video_file = request.FILES.get("video_file")

  filename = video_file.name
  type = request.POST.get("video_category")
  type = int(type)
  desc = request.POST.get("video_description")
  # Convert the audio file from its original format to an MP3 file
  video_data = io.BytesIO(video_file.read())
  video_path = os.path.join(get_video_type_directory(type=type), filename)
  print(video_path)
  if os.path.exists(video_path):
    return redirect(admin_videos)
  with open(video_path, mode='wb') as file:
    file.write(video_data.read())
  typeObject = Type.objects.get(id = type)
  url = get_url(video_path)
  video = Media(type=typeObject, filename=filename, media_type="video", file_path = video_path, desc=desc, url = url)
  video.save()
  return redirect(admin_videos)

def admin_delete_video_ajax(request):
  id = request.POST.get("id")
  video = Media.objects.get(id = str(id))
  video.delete()
  return JsonResponse({}, 200)

#music
def admin_music(request):
  context = {}
  selected_nav = "music"
  context["selected_nav"] = selected_nav

  music = Media.objects.select_related('type').filter(media_type = "music")
  context["music"] = music
  return render(request, 'admin_dashboard/pages/music.html', context)

def admin_upload_music(request):
  print(request.FILES)
  music_file = request.FILES.get("music_file")

  filename = music_file.name

  desc = request.POST.get("music_description")
  # Convert the audio file from its original format to an MP3 file
  music_data = io.BytesIO(music_file.read())
  music_path = os.path.join(get_music_directory(), filename)
  print(music_path)
  if os.path.exists(music_path):
    return redirect(admin_music)
  with open(music_path, mode='wb') as file:
    file.write(music_data.read())
  typeObject = Type.objects.get(id = 1)
  url = get_url(music_path)
  music = Media(type=typeObject, filename=filename, media_type="music", file_path = music_path, desc=desc, url = url)
  music.save()
  return redirect(admin_music)

def admin_delete_music_ajax(request):
  id = request.POST.get("id")
  music = Media.objects.get(id = str(id))
  music.delete()
  return JsonResponse({}, 200)