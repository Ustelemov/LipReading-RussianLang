from work_with_frames_funcs import get_lips_points
import sys
import cv2
import argparse
import os
import json


#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Create JSON-dataset phoneneme+lip point')
parser.add_argument('--i', dest="input_video",type=str,required=True,help='Path to source video')
parser.add_argument('--o',dest="output_file",type=str,required=True,help="Path to output fie")
parser.add_argument('--k',dest='phoneme_file_name',type=str,required=True,help='Path to phoneme by frame file')



args = parser.parse_args()


videofile_path = args.input_video
phoneme_file_name = args.phoneme_file_name
output_file = args.output_file

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

print('Processing is running') 

result = []

count = 0
while(True):
#считывает кадры последовательно, если ret - true - кадр считался верно, если false - будем прекращать считывание
  ret, frame = cap.read()
  if count%100==0:
    print('Proccesing %d of %d frames'%(count,frames_count))
  if ret == True:
    lips_points = get_lips_points(frame)
    #Считаем что губы всегда максимум одни
    lips_points = lips_points[0] if len(lips_points)>0 else None
    phoneme = phonemeFrames[count]
    
    result.append({'phoneme':phoneme,'frame_num':count,'lips_points':lips_points})


    count = count+1
  else:
    break
cap.release()
json.dump(result, open("text.json",'w'))
print('Processing is ended')
