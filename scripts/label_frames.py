from work_with_frames_funcs import label_on_frame
import sys
import cv2
import argparse
import os

#Функция удаление файла,если он существует. Нужно для видео и аудиофайлов, чтобы можно было записать.
def silentremove(filename):
    try:
        os.remove(filename)
    except:
        ''


#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Write text on video from text-by-frame file')
parser.add_argument('--i', dest="input_video",type=str,required=True,help='Path to source video')
parser.add_argument('--o',dest="outfile_name",type=str,required=True,help="Output file path")
parser.add_argument('--t',dest='textfile_name',type=str,required=True,help='Path to text-by-frame file')
parser.add_argument('--f',dest='font_path',type=str,required=True,help='Path to DejaVuSans font to write on russian')

font_size = 24 #Размер щрифта
color = (255,255,255,0) #цвет шрифта
point = (10,10) #Точка на кадре в которой писать текст

args = parser.parse_args()


videofile_path = args.input_video
outfile_name = args.outfile_name
textfile_name = args.textfile_name
font_path = args.font_path

output_path = outfile_name.replace(outfile_name.split('/')[-1],'') #Уберем название файла из пути

#проверяем, есть ли папка - в которую хотим класть выходной файл - создаем, если нет
output_path_exists = os.path.exists(output_path)
if not output_path_exists:
    os.makedirs(output_path)

#Удалим выходной файл, если он уже существует
silentremove(outfile_name)

#Считаем информацию с файла текста по кадрам
textFrames = []
with open(textfile_name,'r') as f:
  textFrames = f.read().splitlines()


cap = cv2.VideoCapture(videofile_path)
frames_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
width  = int(cap.get(3))
height = int(cap.get(4)) 


if (cap.isOpened()== False): 
  sys.exit('Error while openning video file, maybe file doesnt exist')


if(len(textFrames)!=frames_count):
  sys.exit('Lenght of text-frame file not equal to frames count in video')

print('Processing is running') 

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
writer = cv2.VideoWriter(outfile_name, fourcc, fps, (width,height))
  
count = 0
while(True):
#считывает кадры последовательно, если ret - true - кадр считался верно, если false - будем прекращать считывание
  ret, frame = cap.read()
  if count%100==0:
    print('Proccesing %d of %d frames'%(count,frames_count))
  if ret == True:
    label = textFrames[count]
    frame_texted = label_on_frame(frame,label,point=point,fontsize=font_size,font_path=font_path,color=color)
    writer.write(frame_texted)
    count = count+1
  else:
    break
cap.release()
writer.release()
print('Processing is ended') 
