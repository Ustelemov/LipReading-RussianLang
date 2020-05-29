import argparse
import re
import urllib.request as urllib
import subprocess
import numpy as np
import os

#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Download subtitels from Youtube in txt-format')
parser.add_argument('--i', dest="in_path",type=str,required=True,help='Path to words dictionary')
parser.add_argument('--o', dest="out_path",type=str,default='/default/out_words.txt',help='Path to output dictionary')


args = parser.parse_args()


#адрес ютуб видео
in_path = args.in_path
out_path = args.out_path

#Как много слов можно передать, в MAUS-G2P - ограничение 100к, поставим 99к - наверняка
words_capacity=99*1000

with open(in_path) as f:
    words = f.readlines()

#Найдем и заменим - и . на пустоту
for i in range(len(words)):
  source = words[i]
  wo_dot = re.sub(r'[.]+','',source)
  wo_dash = re.sub(r'[-]+','',wo_dot)
  words[i]=wo_dash


words_len = len(words)
print('Words in file before distinct: %d'%(words_len))

#Удалим повторы
words_set = list(set(words))
words_set.sort()

words_len = len(words_set)
print('Words in file after distinct: %d'%(words_len))


parts = words_len//words_capacity
over = words_len-words_capacity*parts


result = []

for i in range(parts+1):
  if i==parts and over>0:
    start = i*words_capacity
    end = i*words_capacity+over
  else:
    start = i*words_capacity
    end = (i+1)*words_capacity

  #Будем писать в файл для работы с curl
  with open('tmp.txt', 'w') as f:
      f.writelines(words_set[start:end])

  CurlUrl="curl -v -X POST -H 'content-type: multipart/form-data' -F com=no -F tgrate=16000 -F stress=no -F lng=rus-RU -F lowercase=yes -F syl=no -F outsym=maus-sampa -F nrm=no -F i=@'tmp.txt' -F tgitem=ort -F align=no -F featset=standard -F iform=txt -F embed=no -F oform=txt 'https://clarin.phonetik.uni-muenchen.de/BASWebServices/services/runG2P'"
  status, output = subprocess.getstatusoutput(CurlUrl)

  link = re.findall(r'(?<=<downloadLink>).*(?=</downloadLink>)',output)[0]

  response = urllib.urlopen(link)
  html = response.read().decode('utf-8')

  splited_html = html.split('\t')

  #Создадим массив со сторчками вида: {словo;фонемная транскрипция}
  tmp_result = [('%s;%s\n'%(words_set[start+i].split('\n')[0],splited_html[i])) for i in range(len(splited_html))]

  result.extend(tmp_result)

#Уберем у последнего элемента лишние \n
result[-1] = result[-1].split('\n')[0]

#Удалим временный файл
os.remove('tmp.txt')

#Запишем результирующий словарь в файл
with open(out_path, 'w') as f:
    f.writelines(result)
print('Dictionary with %d words was succesful created'%(len(result)))
