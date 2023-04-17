from .models import CustomUser
from django.core import validators
from django import forms
from django.contrib.auth import authenticate
from .models import StatusChoice

def validate_register(request):
  first_name = request.POST["first_name"]
  last_name = request.POST["last_name"]
  email = request.POST["email"]
  password = request.POST["password"]
  password2 = request.POST["password2"]
  fullname = first_name + " " + last_name
  fullname = fullname.strip()
  message = ""
  if fullname == "":
    message = "Name should be provided"
    return False, message
  try:
    validators.validate_email(email)
  except forms.ValidationError:
    message = "Invalid Email Address"
    return False, message
  if len(password) < 8:
    message = "Password should be at least 8 characters"
    return False, message
  if len(password) > 30:
    message = "Password should be at most 30 characters"
    return False, message
  first_isalpha = password[0].isalpha()
  if all(c.isalpha() == first_isalpha for c in password):
    message = "Password should containe at least one character and one none character"
    return False, message
  # if password != password2:
  #   message = "Password mismatch"
  #   return False, message
  if CustomUser.objects.filter(email = email).exists():
    message = "Already registered email"
    return False, message
  return True, "Validation Success"
  # if validators.EmailValidator.

def validate_login(request):
  email = request.POST["email"]
  password = request.POST["password"]
  print(email)
  print(password)
  try:
    validators.validate_email(email)
  except forms.ValidationError:
    message = "Invalid Email Address"
    return False, message
  if not CustomUser.objects.filter(email = email).exists():
    message = "Not Registered User"
    return False, message
  user = CustomUser.objects.filter(email = email).first()
  if user.status != StatusChoice.ALLOWED.value:
    print("aaaaaaa")
    message = "You haven't verified your email address"
    return False, message
  print(email)
  print(password)
  user = authenticate(email=email, password=password)
  if user is None:
    message = "Password is wrong"
    return False, message

  return True, "Validation Success"


def validate_contact(request):
  contact_email = request.POST["contact_email"]
  contact_message = request.POST["contact_message"]
  contact_message = contact_message.strip()
  try:
    validators.validate_email(contact_email)
  except forms.ValidationError:
    message = "Invalid Email Address"
    return False, message
  if contact_message is "":
    message = "Provide valid message"
    return False, message

  return True, "Validation Success"
  # if validators.EmailValidator.
