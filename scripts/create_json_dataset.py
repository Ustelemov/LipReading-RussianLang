from work_with_frames_funcs import get_lips_points
import sys
import cv2
import argparse
import os
import json
import time

#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Create JSON-dataset phoneneme+lip point')
parser.add_argument('--i', dest="input_video",type=str,required=True,help='Path to source video')
parser.add_argument('--o',dest="output_file",type=str,required=True,help="Path to output fie")
parser.add_argument('--k',dest='phoneme_file_name',type=str,required=True,help='Path to phoneme by frame file')
parser.add_argument('--d',dest="depress_video",type=bool,default=False,help="Need to depress resolution or not. True - need")



args = parser.parse_args()


videofile_path = args.input_video
phoneme_file_name = args.phoneme_file_name
output_file = args.output_file
depress_video = args.depress_video

depress_width = 854
depress_height = 640


output_path = output_file.replace(output_file.split('/')[-1],'') #Уберем название файла из пути

#проверяем, есть ли папка - в которую хотим класть выходной файл - создаем, если нет
output_path_exists = os.path.exists(output_path)
if not output_path_exists:
    os.makedirs(output_path)

#Считаем информацию с файла фонем по кадрам
phonemeFrames = []
with open(phoneme_file_name,'r') as f:
  phonemeFrames = f.read().splitlines()


cap = cv2.VideoCapture(videofile_path)
frames_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

if (cap.isOpened()== False): 
  sys.exit('Error while openning video file, maybe file doesnt exist')


if(len(phonemeFrames)!=frames_count):
  sys.exit('Lenght of phoneme-by-frame file not equal to frames count in video')

#Запустим таймер
start = time.time()

print('Processing is running') 

result = []
none_count = 0

count = 0
while(True):
#считывает кадры последовательно, если ret - true - кадр считался верно, если false - будем прекращать считывание
  ret, frame = cap.read()
  if count%100==0 and count>0:
    print('Proccesed %d of %d frames'%(count,frames_count))
    print('Time from start in sec: %d'%(int(time.time()-start)))
    print('Time per frame: %f'%(round((time.time()-start)/count,2)))
  if ret == True:
    
    if depress_video:
      res_frame = cv2.resize(frame,(depress_width,depress_height))
    else:
      res_frame = frame

    lips_points = get_lips_points(res_frame)
    #Считаем что губы всегда максимум одни
    #lips_points = lips_points[0] if len(lips_points)>0 else None
    if len(lips_points)>0:
      lips_points = lips_points[0]
    else:
      lips_points = None
      none_count = none_count+1      

    
    phoneme = phonemeFrames[count]
    
    result.append({'phoneme':phoneme,'frame_num':count,'lips_points':lips_points})


    count = count+1
  else:
    break
cap.release()
json.dump(result, open(output_file,'w'))
print('Proccesed frames: %d. With none_lips: %d'%(count,none_count))
print('Processing is ended')
