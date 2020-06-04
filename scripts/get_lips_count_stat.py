import json
import statistics
import numpy as np
import math
import pandas as pd

import matplotlib.pyplot as plt
import argparse
import os

#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Create statistic info about frame with lips count by phonemes')
parser.add_argument('--i',dest="json_path",type=str,required=True,help="Path to JSON file")
parser.add_argument('--o',dest="outputh_path",type=str,default="/default",help="Path where to store files")

args = parser.parse_args()

#Путь к JSON-датасету
json_path = args.json_path

#Путь к выходной папке
output_path = args.outputh_path

#Выходной текстовый файл
text_stat_path = output_path+'/phonemes_wlips_count_stat.txt'
#График количества кадров с губами по фонемам
wlips_count_graph = output_path+'/wlips_count_graph.png'

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

#Загрузим JSON файл
json = json.load(open(json_path))

#Создадим словарь: <фонема, список массивов точек губ>
dict = {}

for f in json:
  #В JSON-None означается, что для кадра (фонемы) не было найден губ
  if f['lips_points']!=None:
    phoneme = f['phoneme']
    lip_points = f['lips_points']['bottom_lip']+f['lips_points']['top_lip']
    if phoneme not in dict.keys():
      dict[phoneme] = []
    dict[phoneme].append(lip_points)

df = pd.DataFrame.from_dict(dict,orient='index')
count_df = pd.DataFrame({'count':df.transpose().agg('count')}, index = dict.keys()).sort_values('count')

#Запишем информацию в файле
with open(text_stat_path,'w') as f:
  f.writelines('В данном файле указана статистка о количестве массивов точек губ по фонемам\n')
  f.writelines('Столбец count - количестве массивов точек губ по фонемам (количество кадров, где удалось распознать губы\n')
  f.writelines(count_df.to_string())
  f.writelines('\n')
print('Text file with statistic was create in: %s'%(text_stat_path))

#Добавим столбец index в DataFrame
count_df = count_df.reset_index()

#Нарисуем график количества массивов точек губ по фонемам
fig,ax = plt.subplots(figsize=figsize, dpi=dpi)
ax.bar(count_df['index'], count_df['count'], color=bars_col, width=.5)
for i, val in enumerate(count_df['count']):
    plt.text(i, val, int(val), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight':500, 'size':8})

ax.set_xticklabels(count_df['index'], rotation=60, horizontalalignment= 'right')
ax.set_title("Распределение количества массивов точек губ по фонемам", fontsize=18)
ax.set_ylabel("Количество массивов точек",fontsize=16)
ax.set_xlabel("Фонемы",fontsize=16)

fig.savefig(wlips_count_graph)
plt.close(fig)

print('Graphic of count of lips points by phoneme was create in: %s'%(wlips_count_graph))
