from work_with_frames_funcs import DlibFaceAligner
import sys
import cv2
import argparse
import os
import time

#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Create lip-image dataset with phonemekey in filename')
parser.add_argument('--i', dest="input_video",type=str,required=True,help='Path to source video')
parser.add_argument('--p',dest="output_path",type=str,required=True,help="Output path to folder")
parser.add_argument('--k',dest='phonemekeys_file_name',type=str,required=True,help='Path to phonemkeys by frame file')
parser.add_argument('--w',dest="lip_width",type=int,default=320,help="Width of output lip picture")
parser.add_argument('--h',dest="lip_height",type=int,default=240,help="Height of output lip picture")
parser.add_argument('--c',dest="count_border",type=int,default=-1,help="How much frames to process. -1 means all")
parser.add_argument('--dw',dest="depressed_width",type=int,default=240,help="Width of input image")
parser.add_argument('--dh',dest="depressed_height",type=int,default=180,help="Height of input image")

args = parser.parse_args()

videofile_path = args.input_video
phonemekey_file_name = args.phonemekeys_file_name
output_path = args.output_path
lip_width = args.lip_width
lip_height = args.lip_height
count_border = args.count_border

depressed_width = args.depressed_width
depressed_height = args.depressed_height


aligner = DlibFaceAligner('/content/LiReading-RussianLang/models/shape_predictor_68_face_landmarks.dat',
                          '/content/LiReading-RussianLang/models/frozen_inference_graph.pb',
                          SSD_input_w = depressed_width,
                          SSD_input_h = depressed_height)


#проверяем, есть ли папка - в которую хотим класть выходной файл - создаем, если нет
output_path_exists = os.path.exists(output_path)
if not output_path_exists:
    os.makedirs(output_path)

#Считаем информацию с файла текста по кадрам
phonemekeyFrames = []
with open(phonemekey_file_name,'r') as f:
  phonemekeyFrames = f.read().splitlines()


cap = cv2.VideoCapture(videofile_path)
frames_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

if (cap.isOpened()== False): 
  sys.exit('Error while openning video file, maybe file doesnt exist')


if(len(phonemekeyFrames)!=frames_count):
  sys.exit('Lenght of phonemekeys-by-frame file not equal to frames count in video')

#Запустим таймер
start = time.time()

print('Processing is running') 

count = 0
while(True):
#считывает кадры последовательно, если ret - true - кадр считался верно, если false - будем прекращать считывание
  ret, frame = cap.read()
  if count%100==0 and count>0:
    print('Proccesed %d of %d frames'%(count,frames_count))
    print('Time from start in sec: %d'%(int(time.time()-start)))
    print('Time per frame: %f'%(round((time.time()-start)/count,2)))
  if ret == True:
    
    lips = aligner.get_aligned_lips(frame,desiredLipWidth=lip_width,desiredLipHeight=lip_height)
    #Считаем что губы всегда максимум одни
    if len(lips)>0:
      #В названии файла зашьем номер фонем до _. После _ добавим номер кадра, чтобы избежать 
      #проблемы с повторением имени
      file_name = output_path+'/%s_%s.jpg'%(phonemekeyFrames[count],count)
      cv2.imwrite(file_name,lips)
    count = count+1
  else:
    break
  #Проверяем границу по кадрам, если нужно - выходим
  if count_border>0 and count>=count_border:
    break
cap.release()
print('Processing is ended') 
