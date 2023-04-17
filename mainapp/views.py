import requests
from django.http import HttpResponse, FileResponse
import json
from django.shortcuts import render,redirect
from django.http import JsonResponse
import openai
from dotenv import load_dotenv
import os
from .models import Type, Question, Feedback
from .openai_api import generate_prompt
from elevenlabslib.helpers import *
from elevenlabslib import *
from .finalize_video import  complete_video_v1, register_user_voice_to_elevenlabs
from django.shortcuts import render, redirect
from django.contrib import messages
from .validation import validate_register, validate_login, validate_contact
from .models import CustomUser
from .enumClass import StatusChoice, RoleChoice
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .main_proc import *

from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.core.mail import EmailMessage  

from elevenlabslib.helpers import *
from elevenlabslib import *

import io


def home(request):
    context = {}
    context["innerPage"] = False
    types = Type.objects.all().values()
    context["types"] = types
    return render(request, 'mainapp/pages/home.html', context)

def back_to_home(request):
   if request.method == "POST":
        answers = []
        type = request.session.get("type")
        for key, value in request.POST.items():
           if key.startswith("answer"):
               answers.append(value)
        #store answers - answers1 for type1, answers2 for type2 ... into sessions
        request.session["answers"+str(type)] = answers
        print(answers)
        return HttpResponse('Success') 

def back_to_questions(request):
   if request.method == "POST":
        script = request.POST["script"]
        #store answers - answers1 for type1, answers2 for type2 ... into sessions
        request.session["script"] = script
        return HttpResponse('Success') 

@login_required
def answer_questions(request, type):
    context = {}
    context["innerPage"] = True
    types = Type.objects.all().values()
    print(request.user.status)
    context["types"] = types
    if request.method == 'GET':
        request.session["type"] = type
        selectedType = Type.objects.get(id=type)
        types = Type.objects.all().values()
        questions = enumerate(Question.objects.filter(type = type))
        
        context["type"] = selectedType
        context["types"] = types
        context["questions"] = questions
        #retrieve answers1 for type 1, answers2 for type2 ... from sessions
        answers = request.session.get('answers'+str(type), []) 
        context["answers"] = answers
        return render(request, 'mainapp/pages/answer_questions.html', context)
    if request.method == 'POST':
        answers = []
        type = request.session.get("type")
        for key, value in request.POST.items():
           if key.startswith("answer"):
               answers.append(value)
        #store answers1 for type1 answers2 for type2 ... into session
        request.session[("answers"+str(type))] = answers
        prompt = generate_prompt(type, answers)
        print(prompt)
        openai.api_key = os.environ.get("GPT3_KEY")

        # response = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=prompt,
        #     max_tokens=1200,
        # )
        # script = response['choices'][0]['text']
        # print(script)
        script = "Dear Mom,\
\
Today I am 32 years old, and have you to thank for so much in my life. I remember being so young, and you were already so old – 59 years ago! You grew up in Kyiv but you pushed through the difficulties of life and managed to bring us all the \
way to the UK.\
\
Through the years I have seen your true strength, kindness and extreme generosity. When I was sick, you nursed me back to health. When we had lost a pet, you stayed strong and comforted us. Despite the challenge of growing up with poverty, you provided more than enough for our family. And I will never forget your bravery when you beat Covid-19.\
\
One of my most treasured memories with you was when you taught me how to be a strong man with courage in the face of adversity. That moment remains in my heart forever.\
\
Mom, I know it wasn't always easy for you but I want you to know that I love you and I am so blessed to have you in my life. Throughout all these years, you have given me so much love, strength and guidance. The love and care that you have showered on me is the greatest gift anybody could have. Thank you, Mom.\
\
Love always,\
Alex"        
        
        request.session["script"] = script
        return redirect(review_script)
        # return render(request, 'mainapp/pages/review_script.html', context)

@login_required
def regenerate_script(request):
    context = {}
    context["innerPage"] = True
    types = Type.objects.all().values()
    context["types"] = types
    if request.method == 'GET':
        type = request.session.get("type")
        answers = request.session.get('answers'+str(type), []) 
        print(answers)
        prompt = generate_prompt(type, answers)
        print(prompt)

        openai.api_key = os.environ.get("GPT3_KEY")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1200,
        )
        script = response['choices'][0]['text']
#         script = "Dear Mom,\
# \
# Today I am 32 years old, and have you to thank for so much in my life. I remember being so young, and you were already so old – 59 years ago! You grew up in Kyiv but you pushed through the difficulties of life and managed to bring us all the \
# way to the UK.\
# \
# Through the years I have seen your true strength, kindness and extreme generosity. When I was sick, you nursed me back to health. When we had lost a pet, you stayed strong and comforted us. Despite the challenge of growing up with poverty, you provided more than enough for our family. And I will never forget your bravery when you beat Covid-19.\
# \
# One of my most treasured memories with you was when you taught me how to be a strong man with courage in the face of adversity. That moment remains in my heart forever.\
# \
# Mom, I know it wasn't always easy for you but I want you to know that I love you and I am so blessed to have you in my life. Throughout all these years, you have given me so much love, strength and guidance. The love and care that you have showered on me is the greatest gift anybody could have. Thank you, Mom.\
# \
# Love always,\
# Alex"        
        request.session["script"] = script
        return redirect(review_script)
        # return render(request, 'mainapp/pages/review_script.html', context)

@login_required
def review_script(request):
    context = {}
    context["innerPage"] = True
    types = Type.objects.all().values()
    context["types"] = types
    type = request.session.get("type")
    selectedType = Type.objects.get(id=type)
    context["type"] = selectedType
    if request.method == 'GET':
        context["script"] = request.session.get("script", "")
        return render(request, 'mainapp/pages/review_script.html', context)
    if request.method == 'POST':
        request.session["script"] = request.POST["script"]
        return redirect(generate_voiceover)

@cache_control(public=True, max_age=3600)
@login_required
def generate_voiceover(request):
    context = {}
    context["innerPage"] = True
    types = Type.objects.all().values()
    context["types"] = types
    type = request.session.get("type")
    selectedType = Type.objects.get(id=type)
    context["type"] = selectedType
    context["script"] = request.session["script"]
    
    if request.method == 'GET':
        if request.path.endswith("voice.mp3"):
            # Serve the audio file
            print("request voice.mp3")
            audio_file_path = get_user_voice_directory(request.user)
            audio_file_path = os.path.join(audio_file_path, "voice.mp3")
            response = FileResponse(open(audio_file_path, 'rb'), content_type='audio/mp3')
            # Set cache control headers for audio file
            response['Cache-Control'] = 'public, max-age=0, no-store'
            return response
        context["voiceover_generated"] = False 
        voice_register_num = request.user.voice_register_num
        context["voice_register_num"] = voice_register_num
        return render(request, 'mainapp/pages/generate_voiceover.html', context)
    if request.method == 'POST':
        apiKey = "a5c72bce272d05f9664d791a057ddcdb"
        voice_type=request.POST["voice_type"]
        voice_id = load_elevenlabs_voice_id(voice_type, request.user)
        text = context["script"]
        voice = 'en-US'
        url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
        headers = {
            'xi-api-key': apiKey,
            'Content-Type': 'application/json'
        }
        body = {
            'text': text,
            'voice': voice
        }
        filepath = os.path.join(get_user_temp_directory(request.user), "voiceover.mp3")
        response = requests.post(url, headers=headers, json=body)
        filepath = str(filepath)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
                print('File saved successfully')
            request.session["voiceover_path"] = filepath
            request.session["voiceover_url"] = get_url(filepath)
            return JsonResponse({}, status=200)
        else:
            return JsonResponse({"message":'Error: failed to convert text to speech'}, status=404)

@login_required
def generate_video(request):
    context = {}
    type = request.session.get("type")
    selectedType = Type.objects.get(id=type)
    context["type"] = selectedType
    context["innerPage"] = True
    types = Type.objects.all().values()
    context["types"] = types
    if request.method == 'GET':
        context["video_generated"] = False 
        context["voiceover_url"] = request.session.get("voiceover_url", "")
        print("aaaaa" + context["voiceover_url"] )
        return render(request, 'mainapp/pages/generate_video.html', context)
    if request.method == 'POST':
        return render(request, 'mainapp/pages/generate_video.html', context)

@login_required
def generate_video_ajax(request):
    context = {}
    context["innerPage"] = True
    type = request.session.get("type")
    selectedType = Type.objects.get(id=type)
    context["type"] = selectedType
    types = Type.objects.all().values()
    context["types"] = types
    if request.method == 'POST':
        user = request.user
        result_video_path, result = complete_video_v1(user, type)
        curUser = CustomUser.objects.get(email = request.user.email)
        print(curUser.is_online)
        if result == True:
            if curUser.is_online == True:  #The user is remaining on the site.
                print("User is online")
                request.session["result_video_path"] = result_video_path
                request.session["result_video_url"] = get_url(result_video_path) 
                return JsonResponse({}, status=200)
            else:   #user leaved the site
                print("User has leaved")
                transport_result_to_user(request, curUser, result_video_path)
                return redirect(final_result)
        else: #error occurred while generating
            return JsonResponse({}, status=500)
def activate(request, uidb64, token):    
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = CustomUser.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_online= True
        #user.set_status(StatusChoice.ALLOWED)
        user.status = StatusChoice.ALLOWED
        user.save()
        print(user)
        user = auth_login(request, user)  
        return redirect(home) 
    else:  
        return HttpResponse('Activation link is invalid!')  

@login_required
def final_result(request):
    context = {}
    type = request.session.get("type")
    selectedType = Type.objects.get(id=type)
    context["type"] = selectedType
    context["innerPage"] = True
    types = Type.objects.all().values()
    context["types"] = types
    if request.method == 'GET':
        context["result_video_url"] = request.session.get("result_video_url") 
        return render(request, 'mainapp/pages/final_result.html', context)
    if request.method == 'POST':
        return render(request, 'mainapp/pages/final_result.html', context)


@login_required
def upload_voice_record(request):
    context = {}
    context["innerPage"] = True
    type = request.session.get("type")
    selectedType = Type.objects.get(id=type)
    context["type"] = selectedType
    types = Type.objects.all().values()
    context["types"] = types
    if request.method == 'POST':
        audio_file = request.FILES['audio']
        # Convert the audio file from its original format to an MP3 file
        audio_data = io.BytesIO(audio_file.read())
        audio_path = os.path.join(get_user_voice_directory(request.user), "voice.mp3")
        with open(audio_path, mode='wb') as file:
            file.write(audio_data.read())
        result, clonedVoiceID = register_user_voice_to_elevenlabs(request.user, str(audio_path))
        if result is False:
            return JsonResponse({'message': 'Cannot register your voice.'}, status=500)
        else:
            currentUser = CustomUser.objects.filter(email=request.user.email).first()
            currentUser.voice_register_num = currentUser.voice_register_num - 1
            currentUser.voice_id = clonedVoiceID
            currentUser.save()              
        return JsonResponse({'message': 'Audio file uploaded and saved as MP3 successfully!'}, status=200)
    return JsonResponse({'message': 'Invalid request.'}, status=404 )

@login_required
def upload_voice_file(request):
    context = {}
    context["innerPage"] = True
    type = request.session.get("type")
    selectedType = Type.objects.get(id=type)
    context["type"] = selectedType
    types = Type.objects.all().values()
    context["types"] = types

    if request.method == 'POST':
        audio_file = request.FILES['audio_file']
        audio_path = os.path.join(get_user_voice_directory(request.user), "voice.mp3")
        with open(audio_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        result, clonedVoiceID = register_user_voice_to_elevenlabs(request.user, str(audio_path))
        if result is False:
            return JsonResponse({'message': 'Cannot register your voice.'}, status=500)
        else:
            currentUser = CustomUser.objects.filter(email=request.user.email).first()
            currentUser.voice_register_num = currentUser.voice_register_num - 1
            currentUser.voice_id = clonedVoiceID
            currentUser.save()              
            return JsonResponse({'message': 'Audio file uploaded and saved as MP3 successfully!'}, status=200)
    return JsonResponse({'message': 'Please upload an audio file.'})

def about(request):
    context = {}
    types = Type.objects.all().values()
    context["types"] = types
    context["innerPage"] = True
    return render(request, 'mainapp/pages/about.html', context)

def login(request):
    print("login")
    context = {}
    types = Type.objects.all().values()
    context["types"] = types
    context["innerPage"] = True
    if request.method == 'GET':
        return render(request, 'mainapp/pages/login.html',context)
    elif request.method == 'POST':
        result, message = validate_login(request)
        if result == False:
            context["login_result"] = result
            context["message"] = message
            return render(request, 'mainapp/pages/login.html', context)
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        user.is_online = True
        user.save()
        auth_login(request, user)
        return redirect(home)

def register(request):
    types = Type.objects.all().values()
    context = {}
    context["innerPage"] = True
    context["types"] = types
    if request.method == "GET":
        return render(request, 'mainapp/pages/register.html', context)
    elif request.method == "POST":
        result, message = validate_register(request)
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password= request.POST["password"]
        
        if result == False:
            context["register_result"] = result
            context["message"] = message
            return render(request, 'mainapp/pages/register.html', context)
        else:
            user = CustomUser(first_name=first_name, last_name=last_name, email=email)
            user.set_status(StatusChoice.PENDING)
            user.set_role(RoleChoice.USER)
            user.set_password(password)    
            user.is_active = True
            
            user.save()
            #todo: email verification
            current_site = get_current_site(request)  

            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('mainapp/pages/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user)  
            })  
            to_email = email
            emailMessage = EmailMessage(  
                mail_subject, message, to=[to_email]  
            )  
            emailMessage.send()
            create_user_directory(user)  
            return render(request, "mainapp/pages/confirm_email.html")  
        
def pricing(request):
    context = {}
    context["innerPage"] = True
    types = Type.objects.all().values()
    context["types"] = types
    return render(request, 'mainapp/pages/pricing.html', context)

def sample_videos(request):
    types = Type.objects.all().values()
    context = {}
    context["innerPage"] = True
    context["types"] = types
    return render(request, 'mainapp/pages/sample_videos.html', context)

def contact(request):
    context = {}
    types = Type.objects.all().values()
    context["types"] = types
    context["innerPage"] = True
    if request.method == "GET":
        return render(request, 'mainapp/pages/contact.html', context)
    else:
        result, message = validate_contact(request)
        context["contact_tried"] = True
        if result is False:
            context["message"] = message
            context["contact_success"] = result
            return render(request, 'mainapp/pages/contact.html', context)
        else:
            contact_email = request.POST.get("contact_email")
            contact_name = request.POST.get("contact_name")
            contact_message = request.POST.get("contact_message")
            contact_subject = request.POST.get("contact_subject")
            feedback = Feedback(email = contact_email, name=contact_name, feedback_text=contact_message, subject=contact_subject)
            feedback.save()
            context["message"] = "Thanks for your contact"
            context["contact_success"] = result
            return render(request, 'mainapp/pages/contact.html', context)
def logout(request):
  auth_logout(request)
  return redirect(home)

@login_required
def update_user_status_ajax(request):
    curUser = CustomUser.objects.get(email = request.user.email)
    curUser.is_online = False
    curUser.save()
    return HttpResponse('Success') 

#user profile views
def user_profile(request):
    voice_register_num = request.user.voice_register_num
    context = {}
    context["voice_register_num"] = voice_register_num
    context["innerPage"] = True
    types = Type.objects.all().values()
    context["types"] = types
    result_video_directory = get_result_video_directory(request.user)
    result_videos_name = get_result_videos(request.user)

    result_videos = []
    for result_video_name in result_videos_name:
        result_video_path = os.path.join(result_video_directory, result_video_name)
        result_videos.append(get_url(result_video_path))
    context["result_videos"] = result_videos
    voice_path =os.path.join(get_user_voice_directory(request.user), "voice.mp3")
    voice_url = get_url(voice_path)
    context["voice"] = voice_url

    return render(request, 'mainapp/pages/user_profile.html', context)