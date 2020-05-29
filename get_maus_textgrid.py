import argparse
import re
import urllib.request as urllib
import subprocess

#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Download subtitels from Youtube in txt-format')
parser.add_argument('--p',dest='output_path',type=str,help='output path to file',default='/default')
parser.add_argument('--a', dest="audio_path",type=str,required=True,help='path to wav file')
parser.add_argument('--t', dest="text_path",type=str,required=True,help='path to txt file')

args = parser.parse_args()

audio_path = args.audio_path
text_path = args.text_path

file_path = args.output_path+'/maus_out.TextGrid'

CurlUrl="curl -v -X POST -H 'content-type: multipart/form-data' -F SIGNAL=@%s -F LANGUAGE=rus-RU -F TEXT=@%s 'https://clarin.phonetik.uni-muenchen.de/BASWebServices/services/runMAUSBasic'"%(audio_path,text_path)
status, output = subprocess.getstatusoutput(CurlUrl)


link = re.findall(r'(?<=<downloadLink>).*(?=</downloadLink>)',output)[0]
response = urllib.urlopen(link)
html = response.read().decode('utf-8')

with open(file_path, 'w') as f:
    f.write(html)

print('TextGrid from TextAligner MausBasic was successful save in:%s'%s(file_path))
