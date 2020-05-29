import re
import os
import sys
import subprocess
from pytube import YouTube
from pytube import cli
from pytube import Caption
from moviepy.editor import *
import errno
import argparse
import cv2


#Функция удаление файла,если он существует. Нужно для видео и аудиофайлов, чтобы можно было записать.
#Текстовый файл просто перезапишется.
def silentremove(filename):
    try:
        os.remove(filename)
    except:
        ''

#Печать метоинформации о видео
def printvideoinfo(filename):
    video = cv2.VideoCapture(filename);
    fps = video.get(cv2.CAP_PROP_FPS);
    frames_count = video.get(cv2.CAP_PROP_FRAME_COUNT);
    length = frames_count*1.0/fps;
    print('FPS: %f'%(fps));
    print('Count frame in video: %d'%(frames_count));
    print('Video length: %d secs'%(length));



#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Download subtitels from Youtube in txt-format')
parser.add_argument('--u', dest="url",type=str,required=True,help='URL of Youtube video which will processing')
parser.add_argument('--p',dest="path",type=str,default="/default",help="Path where to store files")
parser.add_argument('--s',dest="start_sec",type=int,default=0,help="Seconds from start to cut video")
parser.add_argument('--e',dest="end_sec",type=int,default=0,help="Seconds to end to cut video")


args = parser.parse_args()
   

#адрес ютуб видео
url = args.url

#папка для выходных файлов
output_path = args.path

#начало обрезанного видео с ютуб
start_sec = args.start_sec

#конец обрезанного видео с ютуб
end_sec = args.end_sec

need_to_cut = True

#Если параметры нулевые, то обрезать видео не нужно - будет использоваться целиком
if start_sec==end_sec==0:
    need_to_cut = False

if start_sec<0 or end_sec<0 or start_sec>end_sec:
    sys.exit('Bad start_sec and end_sec parameters')

video_path_ytb = output_path+'/video_ytb.mp4'
video_path = output_path+'/video.mp4'
wav_path = output_path+'/audio.wav'
mp3_path = output_path+'/audio.mp3'
subtitles_path = output_path+'/subtitles.txt'

#Исходное и обрезанное видео - совпадают
if not need_to_cut:
   video_path = video_path_ytb

#проверяем, есть ли папка - создаем, если нет
output_path_exists = os.path.exists(output_path)
if not output_path_exists:
    os.makedirs(output_path)

source = YouTube(url)
caption = source.captions.get_by_language_code('ru')

if source==None:
    sys.exit('Video not found, check url')

if caption==None:
    print("No russian subtitles found")
else:
    caption_srt =(caption.generate_srt_captions())
    math = re.findall(r'(?<=\d\n).*\n(?=\n\d)',caption_srt)

    with open(subtitles_path, 'w') as f:
        for item in math:
            f.write("%s" % item)

#скачивание видео с ютуба в mp4, в лучшем разрешении. Progressive - аудио и видео дорожки - вместе
silentremove(video_path_ytb)
streams = source.streams.filter(progressive='True',file_extension='mp4',fps=30).get_highest_resolution()
streams.download(output_path=output_path,filename='video_ytb')

if need_to_cut:
    #обрезаем видео с ютуба: от-до
    silentremove(video_path)
    video = VideoFileClip(video_path_ytb).subclip(start_sec,end_sec)
    video.write_videofile(video_path)

#достаем аудиодорожку с обрезанного видео в wav
silentremove(wav_path)
command = "ffmpeg -i "+video_path+" -ab 192K -ac 2 -ar 44100 -vn -f wav "+wav_path
subprocess.call(command, shell=True)

#достаем аудиодоророжку с обрезанного видео в mp3
silentremove(mp3_path)
command = "ffmpeg -i "+video_path+" -ab 192K -ac 2 -ar 44100 -vn -f mp3 "+mp3_path

#Распечатаем информацию о результате работы 
print('---------------------')
print('Source video was successful download in: %s'%(video_path_ytb))
print('Source video title: %s'%(source.title))
printvideoinfo(video_path_ytb)
print('---------------------')

if caption!=None:
    print('Subtitles was successful download in %s'%(subtitles_path))
    print('---------------------')

if not need_to_cut:
    print('Video was not cut. Source video was used to extract mp3 and wav')
else:
    print('Video was cut from %d to %d sec in: %s'%(start_sec,end_sec,video_path))
    printvideoinfo(video_path)
    print('---------------------')

print('mp3 saved in: %s'%(mp3_path))
print('wav saved in: %s'%(wav_path))
