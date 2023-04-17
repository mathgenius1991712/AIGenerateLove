import os
import shutil
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string  
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site  

#create media/users/[user] directory
def create_user_directory(user):
  user_directory = os.path.join(settings.USERS_ROOT,  user.email)
  if not os.path.isdir(user_directory):
    os.makedirs(user_directory)
  create_user_temp_directory(user)
  create_result_video_directory(user)
  create_user_voice_directory(user)

#get media/users/[user] directory
def get_user_directory(user):
  user_directory = os.path.join(settings.USERS_ROOT,  user.email)
  return user_directory

#clear media/users/[user] directory
def clear_user_directory(user):
  user_directory = get_user_directory(user)
  if os.path.isdir(user_directory):
    shutil.rmtree(user_directory)

#create media/users/[user]/temp
def create_user_temp_directory(user):
  user_directory = get_user_directory(user)
  user_temp_directory = os.path.join(user_directory,  "temp")
  if not os.path.isdir(user_temp_directory):
    os.makedirs(user_temp_directory)

#get media/users/[user]/temp
def get_user_temp_directory(user):
  user_directory = get_user_directory(user)
  user_temp_directory = os.path.join(user_directory,  "temp")
  return user_temp_directory

#clear media/users/[user]/temp
def clear_user_temp_directory(user):
  user_temp_directory = get_user_temp_directory(user)
  if os.path.isdir(user_temp_directory):
    shutil.rmtree(user_temp_directory)

#creatre media/users/[user]/result_video
def create_result_video_directory(user):
  user_directory = get_user_directory(user)
  user_result_video_directory = os.path.join(user_directory,  "result_video")
  if not os.path.isdir(user_result_video_directory):
    os.makedirs(user_result_video_directory)

#get media/users/[user]/result_video
def get_result_video_directory(user):
  user_directory = get_user_directory(user)
  user_result_video_directory = os.path.join(user_directory,  "result_video")
  return user_result_video_directory

#get array of videos [media/users/[user]/result_video/]
def get_result_videos(user):
  user_result_video_directory = get_result_video_directory(user)
  return os.listdir(user_result_video_directory)


#create media/users/[user]/voice
def create_user_voice_directory(user):
  user_directory = get_user_directory(user)
  user_voice_directory = os.path.join(user_directory,  "voice")
  if not os.path.isdir(user_voice_directory):
    os.makedirs(user_voice_directory)

#get media/users/[user]/voice
def get_user_voice_directory(user):
  user_directory = get_user_directory(user)
  user_voice_directory = os.path.join(user_directory,  "voice")
  return user_voice_directory


#get media/video/
def get_video_directory():
  video_directory = os.path.join(settings.MEDIA_ROOT, "video")
  return video_directory

#get media/music/
def get_music_directory():
  music_directory = os.path.join(settings.MEDIA_ROOT, "music")
  return music_directory

#get media/video/[type]/
def get_video_type_directory(type):
  video_directory = get_video_directory()
  user_video_directory = video_directory
  if type == 1:
    user_video_directory = os.path.join(video_directory, "for_mum")
  elif type == 2:
    user_video_directory = os.path.join(video_directory, "for_dad")
  elif type == 3:
    user_video_directory = os.path.join(video_directory, "for_wife")
  elif type == 4:
    user_video_directory = os.path.join(video_directory, "for_husband")
  elif type == 5:
    user_video_directory = os.path.join(video_directory, "for_grandma")
  elif type == 6:
    user_video_directory = os.path.join(video_directory, "for_grandad")
  elif type == 7:
    user_video_directory = os.path.join(video_directory, "for_girlfriend")
  elif type == 8:
    user_video_directory = os.path.join(video_directory, "for_boyfriend")
  else:
      return 'Unknown type'
  return user_video_directory



#convert url to abspath
def get_url(path):
  return path[len(str(settings.BASE_DIR)):]

#convert path to url
def get_path(url):
  if url.startswith("/"):
    url = url[1:]
  if url.startswith("\\"):
    url = url[1:]    
  return str(os.path.join(settings.BASE_DIR, url))

#returns the number of files in the directory
def get_file_num(directory):
  count = 0
  for path in os.listdir(directory):
    # check if current path is a file
    if os.path.isfile(os.path.join(directory, path)):
      count += 1
  return count

#get sample filename for type
def get_sample_filename(type):
  if type == 1:
    return 'for_mum'
  elif type == 2:
    return 'for_dad'
  elif type == 3:
    return 'for_wife'
  elif type == 4:
    return 'for_husband'
  elif type == 5:
    return 'for_grandma'
  elif type == 6:
    return 'for_grandad'
  elif type == 7:
    return 'for_girlfriend'
  elif type == 8:
    return 'for_boyfriend'
  else:
    return 'Unknown type'

#get elevenlabs apikey
def load_elevenlabs_voice_id(voice_type, user):
  if voice_type == "1":
    return "mLx8QBsnfJgNSeETWY1J"
  elif voice_type == "2":
    return "r2JPkp9BBtQxghWPAPcg"
  elif voice_type == "3":
    return "aorimdREazZxwWqmt9m4"
  elif voice_type == "4":
    return "CfPq0sCLLep99Shsw1Xl"
  else:
    if user.voice_id is not None:
      return user.voice_id
    else: 
      return "mLx8QBsnfJgNSeETWY1J"
    
def transport_result_to_user(request, user, result_video_path):
  subject = 'Email with Video Attachment You Generated On Our Site'
  sender = 'company@gmail.com'
  receiver = [user.email]

  # Load the email body template and render it with the provided message
  email_body = render_to_string('pages/send_video_in_email.html', {'user': user})

  # Create an EmailMessage object with the subject, sender, and receiver emails
  email = EmailMessage(subject, email_body, sender, receiver)

  # Attach the video to the email message
  with open(result_video_path, 'rb') as attachment:
    email.attach('result_video.mp4', attachment.read(), 'video/mp4')
  
  # Send the email
  email.send()

#get v1 image for static video directory
def get_v1_video_directory():
  return os.path.join(settings.MEDIA_ROOT, "v1/horizontal")