from work_with_frames_funcs import get_lips_points
from work_with_frames_funcs import draw_lips_points
import sys
import cv2
import argparse
import os
import time
import numpy as np

#Функция удаление файла,если он существует. Нужно для видео и аудиофайлов, чтобы можно было записать.
def silentremove(filename):
    try:
        os.remove(filename)
    except:
        ''


#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Create lip video from face video file')
parser.add_argument('--i', dest="input_video",type=str,required=True,help='Path to video to take lips from')
parser.add_argument('--o',dest="outfile_name",type=str,required=True,help="Output file path")
parser.add_argument('--c',dest="count_border",type=int,default=-1,help="How much frames to process. -1 means all")
parser.add_argument('--d',dest="depress_video",type=bool,default=False,help="Need to depress resolution or not. True - need")


args = parser.parse_args()


videofile_path = args.input_video
outfile_name = args.outfile_name
count_border = args.count_border
depress_video = args.depress_video

depress_width = 854
depress_height = 480

output_path = outfile_name.replace(outfile_name.split('/')[-1],'') #Уберем название файла из пути

#проверяем, есть ли папка - в которую хотим класть выходной файл - создаем, если нет
output_path_exists = os.path.exists(output_path)
if not output_path_exists:
    os.makedirs(output_path)

#Удалим выходной файл, если он уже существует
silentremove(outfile_name)


cap = cv2.VideoCapture(videofile_path)
frames_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
width  = int(cap.get(3))
height = int(cap.get(4)) 

if depress_video:
  width = depress_width
  height = depress_height

if (cap.isOpened()== False): 
 sys.exit('Error while openning video file, maybe file doesnt exist')

print('Processing is running') 

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
writer = cv2.VideoWriter(outfile_name, fourcc, fps, (width,height))
count = 0

#Запустим таймер
start = time.time()

while(True):
#считывает кадры последовательно, если ret - true - кадр считался верно, если false - будем прекращать считывание
  ret, frame = cap.read()
  if count%100==0 and count>0:
    print('Proccesed %d of %d frames'%(count,frames_count))
    print('Time from start in sec: %d'%(int(time.time()-start)))
    print('Time per frame: %f'%(round((time.time()-start)/count,2)))
  if count==200:
    break
  if ret == True:
    count = count+1

    if depress_video:
      res_frame = cv2.resize(frame,(width,height))
    else:
      res_frame = frame

    #Если губы есть, то нарисуем точки, если нет - просто запишем кадр
    draw_lips_points(res_frame)
    writer.write(res_frame)
  else:
    break
    
  #Проверяем границу по кадрам, если нужно - выходим
  if count_border>0 and count>=count_border:
    break
    
cap.release()
writer.release()

print('Processing is ended') 
