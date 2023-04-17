from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser

from .enumClass import RoleChoice, StatusChoice
# Create your models here.

class Type(models.Model):
  title = models.CharField(max_length=100)     #the title of type. i.e for who the video is i.e category
  desc = models.TextField(blank=True)                    #the desc of type. i.e for who the video is i.e category
  thumbnail_path = models.CharField(max_length=255) #typical thumbnail image of that type
  sample_video_path = models.CharField(max_length=255) #typical video of that type

class CustomUser(AbstractUser):
  username = None
  email = models.EmailField("email address", unique=True)
  status = models.CharField(  #status to store whether login i permitted or not
    max_length=30,
    choices=[(tag, tag.value) for tag in StatusChoice]  # Choices is a list of Tuple
  )
  role =models.CharField(
      max_length=30,
      choices=[(tag, tag.value) for tag in RoleChoice]  # Choices is a list of Tuple
  )
  voice_id=models.CharField(max_length=32, blank=True)
  voice_register_num = models.IntegerField(default=5) # the number of times that user can register his voice
  

  is_online = models.BooleanField(default=False)

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = []
  
  objects = CustomUserManager()

  def set_status(self, status):
    self.status = status
  def set_role(self, role):
    self.role = role

  def __str__(self):
    return self.email

class Media(models.Model):
  filename = models.CharField(max_length=255) #filename
  media_type = models.CharField(max_length=10) # IMAGE OR VIDEO
  file_path = models.CharField(max_length=255) # file path
  url = models.CharField(max_length=255) #url
  topic = models.CharField(max_length=255, blank=True)    #the topic of file
  type = models.ForeignKey(Type, null=True, on_delete=models.CASCADE)  #the type of media. i.e for who the media is
  desc = models.TextField(blank=True)                   #short desc

class Question(models.Model):
  type = models.ForeignKey(Type, null=True, on_delete=models.CASCADE) #the type of question. i.e for who the video is i.e category
  order = models.IntegerField()               #the order which this question is displayed
  question = models.CharField(max_length=1024)    #the question
  sample_answer = models.CharField(max_length=1024, blank=True) #the sample answers which will be displayed as the placeholder
  desc = models.TextField(blank=True)                   #short desc

class Prompt(models.Model):
  type = models.ForeignKey(Type, null=True, on_delete=models.CASCADE)  #the type of media. i.e for who the media is
  prompt = models.CharField(max_length=1024)    #the topic of file
  desc = models.TextField(blank=True)                   #short desc

class Feedback(models.Model):
  email = models.EmailField()
  name = models.CharField(max_length=32, blank=True)
  subject = models.CharField(max_length=255, blank=True)
  feedback_text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=8, default="unread")