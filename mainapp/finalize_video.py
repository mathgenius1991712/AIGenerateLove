from datetime import timedelta
import os
import openai
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
from django.conf import settings
from .main_proc import *
import random
from elevenlabslib.helpers import *
from elevenlabslib import *

def transcribe_audio(path): 
    openai.api_key = os.environ.get("GPT3_KEY")
    audio_file= open(path, "rb")
    srtFilename = path.replace(".mp3", ".srt")
    response = openai.Audio.transcribe("whisper-1", audio_file, response_format="srt")
    response = response.strip()
    response += "\n\n1\
00:00:00,000 --> 00:00:06,240"
    with open(srtFilename, 'w', encoding='utf-8') as srtFile:
        srtFile.write(response)
    return  srtFilename 

def finalize_video(origin_video_path, origin_voice_path, origin_background_music_path, result_video_path, subtitle_color = 'white'):
    srt_path = transcribe_audio(origin_voice_path)    
    video = VideoFileClip(origin_video_path)
    gen = lambda txt: TextClip(
            txt, color="yellow", fontsize=60, font='Georgia-Regular',
            stroke_width=3, method='caption', align='south', size=video.size)

    voice = AudioFileClip(origin_voice_path)
    
    voice = voice.volumex(1.5)
    backgroundMusic = AudioFileClip(origin_background_music_path)
    backgroundMusic = backgroundMusic.volumex(0.3)
    voice_duration = voice.duration
    print(voice_duration)
    repeatedAudioClip = afx.audio_loop( backgroundMusic, duration=voice_duration)
    new_audioclip = CompositeAudioClip([voice, repeatedAudioClip])

    subtitles = SubtitlesClip(srt_path, gen)
    video = video.subclip(0, voice_duration)
    video = CompositeVideoClip([video, subtitles.set_pos(('center','center'))])
    
    video.audio = new_audioclip
    print(video.duration)
    print(new_audioclip.duration)
    # Remove the temp audio file
    temp_audio_path = os.path.join(os.path.dirname(origin_voice_path), "temp_audio.mp3")
    
    print("before writing video")
    video = video.set_duration(voice_duration)
    video.write_videofile(result_video_path, temp_audiofile=temp_audio_path)
    if os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)
    result = True
    return result

def complete_video(user, type):
    origin_video_directory = get_video_type_directory(type)
    origin_music_directory = get_music_directory()  
    result_video_directory = get_result_video_directory(user) #the directory where this user's result is stored
    result_video_num = get_file_num(result_video_directory) #the number of files this user generated
    result_video_path = os.path.join(result_video_directory, get_sample_filename(type) + str(result_video_num + 1) + ".mp4") 
    #select random video file in the directory
    origin_video_path = os.path.join(origin_video_directory, random.choice(os.listdir(origin_video_directory)))
    origin_voiceover_path = os.path.join(get_user_temp_directory(user),"voiceover.mp3")
    origin_background_music_path = os.path.join(origin_music_directory, random.choice(os.listdir(origin_music_directory)))
    result = finalize_video(origin_video_path, origin_voiceover_path, origin_background_music_path, result_video_path, subtitle_color = 'white')        
    return result_video_path, result



#register user voice to elevenlabs - elevenlabs api
def register_user_voice_to_elevenlabs(user, filepath):
    if user.voice_register_num == 0:
        return False
    apiKey = os.environ.get("ELEVEN_LABS_API_KEY")
    elevenLabsUser = ElevenLabsUser(apiKey)
    if elevenLabsUser.get_voice_clone_available():
        samplePath1 = [filepath]    
        newClonedVoice = elevenLabsUser.clone_voice_by_path(user.email+"Voice", samplePath1)
        return True, newClonedVoice.voiceID
    return False, ""


#v1 simply choose static image as video
def complete_video_v1(user, type):
    origin_video_directory = get_v1_video_directory()
    origin_video_path = ""
    random_value = random.randint(1,3)
    if random_value == 1:
        origin_video_path = os.path.join(origin_video_directory, "img1.jfif")
    elif random_value == 2:
        origin_video_path = os.path.join(origin_video_directory, "img2.jfif")
    else:
        origin_video_path = os.path.join(origin_video_directory, "img3.jfif")

    origin_music_directory = get_music_directory()  
    result_video_directory = get_result_video_directory(user) #the directory where this user's result is stored
    result_video_num = get_file_num(result_video_directory) #the number of files this user generated
    result_video_path = os.path.join(result_video_directory, get_sample_filename(type) + str(result_video_num + 1) + ".mp4") 
    #select random video file in the directory
    origin_video_path = os.path.join(origin_video_directory, random.choice(os.listdir(origin_video_directory)))
    origin_voiceover_path = os.path.join(get_user_temp_directory(user),"voiceover.mp3")
    origin_background_music_path = os.path.join(origin_music_directory, random.choice(os.listdir(origin_music_directory)))
    result = finalize_video_v1(origin_video_path, origin_voiceover_path, origin_background_music_path, result_video_path, subtitle_color = 'white')        
    return result_video_path, result

def finalize_video_v1(origin_video_path, origin_voice_path, origin_background_music_path, result_video_path, subtitle_color = 'white'):
    srt_path = transcribe_audio(origin_voice_path)    
    video = ImageClip(origin_video_path)
    gen = lambda txt: TextClip(
            txt, color="yellow", fontsize=60, font='Georgia-Regular',
            stroke_width=3, method='caption', align='south', size=video.size)

    voice = AudioFileClip(origin_voice_path)
    
    voice = voice.volumex(1.5)
    backgroundMusic = AudioFileClip(origin_background_music_path)
    backgroundMusic = backgroundMusic.volumex(0.3)
    voice_duration = voice.duration
    print(voice_duration)
    repeatedAudioClip = afx.audio_loop( backgroundMusic, duration=voice_duration)
    new_audioclip = CompositeAudioClip([voice, repeatedAudioClip])

    subtitles = SubtitlesClip(srt_path, gen)
    video = video.set_duration(voice_duration + 3)
    #video = video.subclip(0, voice_duration)
    video = CompositeVideoClip([video, subtitles.set_position(('center', -0.5), relative = True)])
    
    video.audio = new_audioclip
    print(video.duration)
    print(new_audioclip.duration)
    # Remove the temp audio file
    temp_audio_path = os.path.join(os.path.dirname(origin_voice_path), "temp_audio.mp3")
    
    print("before writing video")
    video = video.set_duration(voice_duration)
    video.write_videofile(result_video_path, temp_audiofile=temp_audio_path, fps=30)
    if os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)
    result = True
    return result
