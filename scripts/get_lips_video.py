from work_with_frames_funcs import get_aligned_lips
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
parser = argparse.ArgumentParser(usage='Download subtitels from Youtube in txt-format')
parser.add_argument('--i', dest="input_video",type=str,required=True,help='Path to video to take lips from')
parser.add_argument('--f',dest="outfile_name",type=str,required=True,help="Output file path")
parser.add_argument('--w',dest='width',type=int,default=320,help='Width of output video')
parser.add_argument('--h',dest='height',type=int,default=240,help='Height of output video')


args = parser.parse_args()


videofile_path = args.input_video
outfile_name = args.outfile_name
width = args.width
height = args.height

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

if (cap.isOpened()== False): 
 sys.exit('Error while openning video file, maybe file doesnt exist')

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
    count = count+1
    frames = get_aligned_lips(frame,desiredLipWidth=width,desiredLipHeight=height)
    #Берем только первый кадр (считаем, что там одни губы пока всегда)
    #Если нет губ - пропускаем кадр
    if len(frames)>0: 
      writer.write(frames[0])
  else:
    break
cap.release()
writer.release()

print('Processing is ended') 
