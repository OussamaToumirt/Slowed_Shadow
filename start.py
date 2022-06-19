import yt_dlp
import os
import audiosfx as aud
import requests
import os
from PIL import Image, ImageFont, ImageDraw,ImageFilter
from distutils import dir_util
import os
import shutil
import time
from threading import Thread
from moviepy.editor import *
from youtube_upload import youtube
import ftplib
import cv2
import numpy as np


dir_path = os.path.dirname(os.path.realpath(__file__)) 


def start(video_url):
    def thumbnail(video_id):
        response = requests.get(f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg')
        quality = True
        if response.status_code == 404:
            response = requests.get(f'https://img.youtube.com/vi/{video_id}/hqdefault.jpg')
            quality = False
        with open(dir_path + '/thumbnails/' +  f'thumb-{video_id}.jpg', 'wb') as f:
            f.write(response.content)
            f.close()

        img = cv2.imread(dir_path + '/thumbnails/' +  f'thumb-{video_id}.jpg')
        size = 30
        # generating the kernel
        kernel_motion_blur = np.zeros((size, size))
        kernel_motion_blur[int((size-1)/2), :] = np.ones(size)
        kernel_motion_blur = kernel_motion_blur / size

        # applying the kernel to the input image
        output = cv2.filter2D(img, -1, kernel_motion_blur)
        
        if quality:
            final = cv2.putText(img=output, text='Slowed And Reverb', org=(120, 620), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(255,255, 255),thickness=6)
        else:
            final = cv2.putText(img=output, text='Slowed And Reverb', org=(80, 250), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255,255, 255),thickness=3)

        cv2.imwrite(dir_path + '/thumbnails/' +  f'thumb-{video_id}.jpg', output)
        cv2.waitKey(0)
        
        
        
    def uploader(video_id, video_title):
        thumbnail(video_id)
        youtube(video_id, f'{video_title} - Slowed And Reverb')
        
        
        
            
    def merger(audio_path, video_title, video_id, photo_path):
        print('merging audio with image ....')
        audio = dir_path + '/videos_cdn/'+ f'{video_id}' +'_drakify.wav'
        photo = dir_path + '/photos_cdn/'+ f'{video_id}-random.jpg'
        # Import the audio(Insert to location of your audio instead of audioClip.mp3)
        audio = AudioFileClip(audio)
        # Import the Image and set its duration same as the audio (Insert the location of your photo instead of photo.jpg)
        clip = ImageClip(photo).set_duration(audio.duration)
        # Set the audio of the clip
        clip = clip.set_audio(audio)
        # Export the clip
        clip.write_videofile(f"{video_id}.mp4", threads=8, fps=1, codec='h264_nvenc')
        
        
        shutil.move(dir_path + f'/{video_id}.mp4', dir_path + '/ready_to_upload/' + f'{video_id}.mp4')
        os.remove(dir_path + '/videos_cdn/'+ f'{video_id}' +'.wav')
        uploader(video_id, video_title)
    


    def random_image(audio_path, video_title, video_id):
        reponse = requests.get('https://source.unsplash.com/random/1920x1080?sig=3')
        image_path = dir_path + '/photos_cdn' +  f'/{video_id}-random.jpg'
        with open(image_path, 'wb') as f:
            f.write(reponse.content)
            f.close()

        my_image = Image.open('random.jpg')
        my_image = my_image.filter(ImageFilter.GaussianBlur(100))
        if len(video_title) > 30:
            title_font = ImageFont.truetype('fonts/edo.ttf', 70)
        else:
            title_font = ImageFont.truetype('fonts/edo.ttf', 90)
        title_text =  video_title + '\n       Slowed And Reverb' 
        image_editable = ImageDraw.Draw(my_image)
        image_editable.text((280,450), title_text, (255,255, 255), font=title_font)


        my_image.save(image_path)
        
        
        merger(audio_path, video_title, video_id, image_path)
        
        
    



    def proccessing(audio_path, video_title, video_id):
        print('Slowling ....')
        # Create a new video object
        aud.drakify(audio_path)

        # Push To get image
        random_image(audio_path, video_title, video_id)
        
    
    
    url = video_url
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': 'videos_cdn/%(id)s.%(ext)s',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print('Downloading ....')
        infromation = ydl.extract_info(url, download=False)
        video_id = infromation.get('id')
        title = infromation.get('title')
        ydl.download('https://youtu.be/' + video_id)
        proccessing(dir_path + f'/videos_cdn/{video_id}.wav', title, video_id)
        
        
    
        
    
        




video = str(input('Enter Video Url: '))
t1 = Thread(target=start, args=[video,])
t2 = Thread(target=start, args=['https://youtu.be/k8s7BNlo2-Y',])



t1.start()
#t2.start()



