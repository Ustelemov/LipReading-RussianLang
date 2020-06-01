import pandas as pd
import matplotlib.pyplot as plt

import argparse
import os
import numpy as np


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
text_stat_path = output_path+'/phonemes_duration_stat.txt'
#График суммарной длительности в кадрах по фонемам
sum_duration_graph = output_path+'/sum_duration.png'
#График суммарной длительности в процентах от общего числа кадров по фонемам
sum_duration_percent_graph = output_path+'/sum_duration_percent_graph.png'
#График максимальной длительности в кадрах по фонемам
max_duration_graph = output_path+'/max_duration_graph.png'
#График минимальной длительности в кадрах по фонемам
min_duration_graph = output_path+'/min_duration_graph.png'
#График средней длительности (+std) в кадрах по фонемам
mean_duration_graph = output_path+'/mean_duration_graph.png'

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
#цвет для std-границ
errors_col = 'yellow'

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


desc_df = result_df.agg(['sum','min','max','mean','std','count']).fillna(0)

#Посчитаем длительность в процентах от всех кадров и создадим результирующих DF
sum_df = desc_df.loc['sum',:]
sum_percent = [round(i*100.0/count_frames,1) for i in sum_df]
dur_by_phoneme_df = pd.DataFrame({'sum':sum_df,'sum_percent':sum_percent,'min':desc_df.loc['min',:],
                           'max':desc_df.loc['max',:],'mean':desc_df.loc['mean',:],
                           'std':desc_df.loc['std',:], 'count':desc_df.loc['count',:]})

#Создадим список всех длительностей фонем по кадрам (для построения общей статистики)
all_dur_list = []
for k in info_dict.values():
  all_dur_list.extend(k)

#Преобразуем в numpy-массив для работы со статистическими функциями
all_dur_list = np.asarray(all_dur_list)

#Запишем информацию в файле
with open(text_stat_path,'w') as f:
  f.writelines('В данном файле указана статистика о длительности фонем в кадрах (в разрезе каждой фонемы и общая)\n')
  f.writelines('Всего кадров (и, соответственно, фонем): %d\n'%(count_frames))
  f.writelines('---Статистика в разрезе каждой фонемы---\n')
  f.writelines('Столбец sum - сумма длительности в кадрах\n')
  f.writelines('Столбец sum_percent - сумма длительности в процентах от общего количества кадров\n')
  f.writelines('Столбец min - минимальная длительность в кадрах\n')
  f.writelines('Столбец max - максимальная длительность в кадрах\n')
  f.writelines('Стообец mean - средняя длительность в кадрах\n')
  f.writelines('Столбец std - среднее квадратичное отклонение длительности в кадрах\n')
  f.writelines('Столбец count - число встреч фонемы (не учитывается длительность)\n')
  f.writelines(dur_by_phoneme_df.to_string())
  f.writelines('\n')
  f.writelines('---Общая статистика---\n')
  f.writelines('Минимальная длительность в кадрах по всем фонемам: %d\n'%(int(all_dur_list.min())))
  f.writelines('Максимальная длительность в кадрах по всем фонемам: %d\n'%(int(all_dur_list.max())))
  f.writelines('Средняя длительность в кадрах по всем фонемам: %f\n'%(round(all_dur_list.mean(),2)))
  f.writelines('Среднее квадратичное отклонение длительности в кадрах по всем фонемам: %f\n'%(round(all_dur_list.std(),2)))

print('Text file with statistic was create in: %s'%(text_stat_path))

#Добавим индекс (ключ - фонему). Будем сортировать по нужном столбцу и соответственно использовать
#отсортированные индексы
dur_by_phoneme_df = dur_by_phoneme_df.reset_index()

#Нарисуем график суммарной длительности в кадрах по каждой фонеме
tmp_df = dur_by_phoneme_df.sort_values('sum')
fig = plt.figure(figsize=figsize,dpi=dpi)

ax = tmp_df['sum'].plot (kind='bar',color=bars_col,capsize=5, alpha = 0.5,width=.5)

ax2 = ax.twinx()
ax2.plot(ax.get_xticks(),tmp_df['count'],c='navy', linewidth=0.5)

for i, val in enumerate(tmp_df['sum']):
    ax.text(i, val, int(val), horizontalalignment='center', verticalalignment='bottom', 
            fontdict={'fontweight':500, 'size':8})
    
for i, val in enumerate(tmp_df['count']):
    ax2.text(i, val, int(val), horizontalalignment='center', verticalalignment='bottom', color='blue',
            fontdict={'fontweight':500, 'size':7})    

ax.set_xticklabels(tmp_df['index'],
                   horizontalalignment= 'right',fontsize=10,rotation=60)



ax.set_title("Распределение суммарной длительности в кадрах по фонемам", fontsize=18)
ax.set_ylabel("Суммарное количество кадров",fontsize=16)
ax.set_xlabel("Фонемы",fontsize=16)
ax2.set_ylabel('Число встреч фонемы',fontsize=16)


fig.savefig(sum_duration_graph)
plt.close(fig)

print('Graphic of sum of duratation in frames by phonemes was create in: %s'%(sum_duration_graph))

#Нарисуем график суммарной длительности в процентах от общего числа кадров по каждой фонеме
tmp_df = dur_by_phoneme_df.sort_values('sum_percent')
fig = plt.figure(figsize=figsize,dpi=dpi)

ax = tmp_df['sum_percent'].plot (kind='bar',color=bars_col,capsize=5, alpha = 0.5,width=.5)

ax2 = ax.twinx()
ax2.plot(ax.get_xticks(),tmp_df['count'],c='navy', linewidth=0.5)

for i, val in enumerate(tmp_df['sum_percent']):
    ax.text(i, val, round(val,1), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight':500, 'size':10})

for i, val in enumerate(tmp_df['count']):
    ax2.text(i, val, int(val), horizontalalignment='center', verticalalignment='bottom', color='blue',
            fontdict={'fontweight':500, 'size':7}) 

ax.set_xticklabels(tmp_df['index'],
                   horizontalalignment= 'right',fontsize=10,rotation=60)

ax.set_title("Распределение суммарной длительности в процентах", fontsize=18)
ax.set_ylabel("Процент кадров",fontsize=16)
ax.set_xlabel("Фонемы",fontsize=16)
ax2.set_ylabel('Число встреч фонемы',fontsize=16)


fig.savefig(sum_duration_percent_graph)
plt.close(fig)

print('Graphic of percentes duration of all frames by phonemes: %s'%(sum_duration_percent_graph))

#Нарисуем график максимальной длительности в кадрах по каждой фонеме
tmp_df = dur_by_phoneme_df.sort_values('max')
fig = plt.figure(figsize=figsize,dpi=dpi)

ax = tmp_df['max'].plot (kind='bar',color=bars_col,capsize=5, alpha = 0.5,width=.5)

ax2 = ax.twinx()
ax2.plot(ax.get_xticks(),tmp_df['count'],c='navy', linewidth=0.5)

for i, val in enumerate(tmp_df['max']):
    ax.text(i, val, int(val), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight':500, 'size':10})

for i, val in enumerate(tmp_df['count']):
    ax2.text(i, val, int(val), horizontalalignment='center', verticalalignment='bottom', color='blue',
            fontdict={'fontweight':500, 'size':7}) 

ax.set_xticklabels(tmp_df['index'],
                   horizontalalignment= 'right',fontsize=10,rotation=60)

ax.set_title("Распределение максимальной длительности фонем в кадрах", fontsize=18)
ax.set_ylabel("Максимальная длительность в кадрах",fontsize=16)
ax.set_xlabel("Фонемы",fontsize=16)
ax2.set_ylabel('Число встреч фонемы',fontsize=16)


fig.savefig(max_duration_graph)
plt.close(fig)

print('Graphic of max duration in frames by phonemes: %s'%(max_duration_graph))

#Нарисуем график минимальной длительности в кадрах по каждой фонеме

tmp_df = dur_by_phoneme_df.sort_values('min')
fig = plt.figure(figsize=figsize,dpi=dpi)

ax = tmp_df['min'].plot (kind='bar',color=bars_col,capsize=5, alpha = 0.5,width=.5)

ax2 = ax.twinx()
ax2.plot(ax.get_xticks(),tmp_df['count'],c='navy', linewidth=0.5)

for i, val in enumerate(tmp_df['min']):
    ax.text(i, val, int(val), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight':500, 'size':10})

ax.set_xticklabels(tmp_df['index'],
                   horizontalalignment= 'right',fontsize=10,rotation=60)

for i, val in enumerate(tmp_df['count']):
    ax2.text(i, val, int(val), horizontalalignment='center', verticalalignment='bottom', color='blue',
            fontdict={'fontweight':500, 'size':7}) 

ax.set_title("Распределение минимальной длительности фонем в кадрах", fontsize=18)
ax.set_ylabel("Минимальная длительность в кадрах",fontsize=16)
ax.set_xlabel("Фонемы",fontsize=16)
ax2.set_ylabel('Число встреч фонемы',fontsize=16)

fig.savefig(min_duration_graph)
plt.close(fig)

print('Graphic of min duration in frames by phonemes: %s'%(min_duration_graph))

#Нарисуем график средней длительности в кадрах (плюс отклонение) по каждой фонеме
tmp_df = dur_by_phoneme_df.sort_values('mean')
fig = plt.figure(figsize=figsize,dpi=dpi)

ax = tmp_df['mean'].plot (kind='bar', yerr= tmp_df['std'],color=bars_col,
       ecolor=errors_col, capsize=5, alpha = 0.5,width=.5)

ax2 = ax.twinx()
ax2.plot(ax.get_xticks(),tmp_df['count'],c='navy', linewidth=0.5)

for i, val in enumerate(tmp_df['mean']):
    ax.text(i, val, round(val,1), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight':500, 'size':10})

for i, val in enumerate(tmp_df['count']):
    ax2.text(i, val, int(val), horizontalalignment='center', verticalalignment='bottom', color='blue',
            fontdict={'fontweight':500, 'size':7}) 

ax.set_xticklabels(tmp_df['index'],
                   horizontalalignment= 'right',fontsize=10,rotation=60)

ax.set_title("Распределение средней длительности фонем в кадрах по каждой фонеме", fontsize=18)
ax.set_ylabel("Средняя длительность в кадрах",fontsize=16)
ax.set_xlabel("Фонемы",fontsize=16)
ax2.set_ylabel('Число встреч фонемы',fontsize=16)

fig.savefig(mean_duration_graph)
plt.close(fig)

print('Graphic of mean (+\- std) duration in frames by phonemes: %s'%(mean_duration_graph))
