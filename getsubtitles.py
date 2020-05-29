import re
import os
from pytube import YouTube
from pytube import cli
from pytube import Caption

import argparse

#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Download subtitels from Youtube in txt-format')
parser.add_argument('--u', dest="url",type=str,required=True,help='URL of Youtube video which will processing')
parser.add_argument('--p',dest="path",type=str,default="/default",help="Path where to store file")

args = parser.parse_args()

url = args.url
output_path=args.path

#проверяем, есть ли папка - создаем, если нет
output_path_exists = os.path.exists(output_path)
if not output_path_exists:
    os.makedirs(output_path)


#скачивание субтитры с ютуб в srt формате, удаляем лишнее - оставляем только текст, сохраняем в файл
source = YouTube(url)
caption = source.captions.get_by_language_code('ru')
if caption==None:
  print("No russian subtitles found")
#Если русские суббтитры были найдены
else:
  caption_srt =(caption.generate_srt_captions())
  math = re.findall(r'(?<=\d\n).*\n(?=\n\d)',caption_srt)

  with open(output_path+'/subtitles.txt', 'w') as f:
    for item in math:
        f.write("%s" % item)
  print('Video title: %s'%(source.title))
  print('Video length: %s secs'%(source.length))
  print("Subtitles saved with success to %s"%(output_path+'/subtitles.txt'))
