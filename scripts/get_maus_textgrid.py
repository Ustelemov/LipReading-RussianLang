import argparse
import re
import urllib.request as urllib
import subprocess
import os

#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Download subtitels from Youtube in txt-format')
parser.add_argument('--o',dest='output_file',type=str,help='output path to TextGrid file',default='/default/maus_out.TextGrid')
parser.add_argument('--a', dest="audio_path",type=str,required=True,help='path to wav file')
parser.add_argument('--t', dest="text_path",type=str,required=True,help='path to txt file')

args = parser.parse_args()

audio_path = args.audio_path
text_path = args.text_path

output_file = args.output_file

output_path = output_file.replace(output_file.split('/')[-1],'') #Уберем название файла из пути

#проверяем, есть ли папка - в которую хотим класть выходной файл - создаем, если нет
output_path_exists = os.path.exists(output_path)
if not output_path_exists:
    os.makedirs(output_path)

CurlUrl="curl -v -X POST -H 'content-type: multipart/form-data' -F SIGNAL=@%s -F LANGUAGE=rus-RU -F TEXT=@%s 'https://clarin.phonetik.uni-muenchen.de/BASWebServices/services/runMAUSBasic'"%(audio_path,text_path)
status, output = subprocess.getstatusoutput(CurlUrl)


link = re.findall(r'(?<=<downloadLink>).*(?=</downloadLink>)',output)[0]

if len(link) == 0:
    print('System error (maybe length of subtitles is exceed)')
else:
    response = urllib.urlopen(link)
    html = response.read().decode('utf-8')

    with open(output_file, 'w') as f:
        f.write(html)

    print('TextGrid from TextAligner MausBasic was successful save in:%s'%(output_file))
