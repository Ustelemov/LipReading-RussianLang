import pandas as pd
import matplotlib.pyplot as plt

import argparse
import os

#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Create statistic info about phonemes appearence')
parser.add_argument('--p',dest="path",type=str,default="/default",help="Path where to store files")
parser.add_argument('--d',dest='phonemekeys_dict',type=str,required=True, help="Path to phonemes-keys dictionary-file")
parser.add_argument('--f',dest='phonemes_frames',type=str,required=True, help="Path to phonemes by frames file")
parser.add_argument('--e',dest='exclude_p',type=bool,default=False, help="Exclude <p:> phoneme or not")


args = parser.parse_args()


#Исключать ли <p:>
exclude_p = args.exclude_p

#Лист фонем, которые не включаются в статистику
exception_list = ['<p:>'] #в основном будет исключаться <p:>, но при необходимости можно будет расширить

#Если не надо исключать - сделаем список исключения пустым
if exclude_p==False:
  exception_list=[]

#путь к словарю фонем
phonemes_dict_path = args.phonemekeys_dict

#Путь к файлу фонем по кадрам
phonemes_frames_path = args.phonemes_frames

#Путь к выходной папке
output_path = args.path

#Выходной текстовый файл
text_stat_path = output_path+'/phonemes_appears_info.txt'
#График количества встреч фонем
appearence_graph = output_path+'/phonemes_appears_count.png'
#График процента количества встреч фонем
appearence_percent_graph = output_path+'/phonemes_appears_percent.png'

#проверяем, есть ли папка - создаем, если нет
output_path_exists = os.path.exists(output_path)
if not output_path_exists:
    os.makedirs(output_path)

#dpi для графиков (множитель)
dpi = 100
#width heights, с dpi 100, для размера 1280х720 - (12.7,7.2)
figsize = (12.8,7.2)

#цвет столбиков на диаграммах
bars_col = 'red'

info_dict = {}

#Считаем словарь фонем
with open(phonemes_dict_path,'r') as f:
  phonemes = f.readlines()

#Строка выглядит следующим образом:фонема ключ
#Создадим словарь <фонема, массив>
for el in phonemes:
  phoneme = el.split(' ')[0]
  #Если фонема в листе исключений, не будем добавлять её
  if phoneme in exception_list:
    continue
  info_dict[phoneme] = []

#Считаем фонемы по кадрам
with open(phonemes_frames_path,'r') as f:
  phoneme_frames_lines = f.readlines()

#Уберем \n-ы
phoneme_frames = [i.split('\n')[0] for i in phoneme_frames_lines]

#число кадров\строк в файле
count_frames = len(phoneme_frames)

tmp_count = 1

#Заполним словарь: ключ - фонема, значение - список встреч фонемы (одна встреча - один элемент, каждый элемент - длительность в кадрах)
for i in range(count_frames):
  this_ph = phoneme_frames[i]
  #Если фонема в листе исключений - пропустим её
  if this_ph in exception_list:
    continue
  #Если последняя
  if i == count_frames -1:
    next_ph = None
  else:
    next_ph = phoneme_frames[i+1]
  
  #Если дальше такая же, то просто прибавим
  if this_ph==next_ph:
    tmp_count = tmp_count+1
  #Если следующая не такая, то запишем в словарь
  else:
    info_dict[this_ph].append(tmp_count)
    tmp_count = 1 #Обновим для новой фонемы

#Создадим DataFrame из словаря 
df = pd.DataFrame.from_dict(info_dict, orient='index')
result_df = df.transpose()

phonemes = info_dict.keys()

count_df = result_df.describe().loc['count',:]

#Сделаем список с процентом появлений
counts_percent_list = [round(i*100.0/count_df.sum(),1) for i in count_df]

#Создадим общий DataFrame, который выведем в файл
count_df = pd.DataFrame({'count': count_df,'count_percent':counts_percent_list},index=phonemes)


#Запишем информацию в файле
with open(text_stat_path,'w') as f:
  f.writelines('В данном файле указана статистка о встрече фонем\n')
  f.writelines('Столбец count - количество встреч фонемы\n')
  f.writelines('Столбец count_percent - процент от всех встреч\n')
  f.writelines(count_df.to_string())
  f.writelines('\n')
  f.writelines('Значение sum - общее количество всех встреч\n')
  f.writelines(count_df['count'].transpose().agg(['sum','min','max','mean','std']).to_string())
print('Text file with statistic was create in: %s'%(text_stat_path))

count_df = count_df.reset_index().sort_values('count')

#Нарисуем график количества появлений по фонемам
fig,ax = plt.subplots(figsize=figsize, dpi=dpi)
ax.bar(count_df['index'], count_df['count'], color=bars_col, width=.5)
for i, val in enumerate(count_df['count']):
    plt.text(i, val, int(val), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight':500, 'size':8})

ax.set_xticklabels(count_df['index'], rotation=60, horizontalalignment= 'right')
ax.set_title("Распределение количества появлений по фонемам", fontsize=18)
ax.set_ylabel("Количество появлений",fontsize=16)
ax.set_xlabel("Фонемы",fontsize=16)

fig.savefig(appearence_graph)
plt.close(fig)

print('Graphic of appearence count by frame was create in: %s'%(appearence_graph))

#Нарисуем график процента появлений от общего числа появлений по фонемам
fig,ax = plt.subplots(figsize=figsize, dpi=dpi)
ax.bar(count_df['index'], count_df['count_percent'], color=bars_col, width=.5)
for i, val in enumerate(count_df['count_percent']):
    plt.text(i, val, val, horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight':500, 'size':8})

ax.set_xticklabels(count_df['index'], rotation=60, horizontalalignment= 'right')
ax.set_title("Распределение количества появлений в процентах по фонемам (из %d кадров)"%(count_frames), fontsize=18)
ax.set_ylabel("Процент появления",fontsize=16)
ax.set_xlabel("Фонемы",fontsize=16)

fig.savefig(appearence_percent_graph)
plt.close(fig)

print('Graphic of appearence percent count by frame was create in: %s'%(appearence_graph))
