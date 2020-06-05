import os
import argparse
import glob
import json


#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Stretch json files in folder to json')
parser.add_argument('--i',dest="input_path",type=str,required=True,help="Path to files")
parser.add_argument('--o',dest="out_filepath",type=str,required=True,help="Path to output json file")


args = parser.parse_args()

input_path = args.input_path
out_filepath = args.out_filepath


result = []

for f in sorted(glob.glob(input_path+'/*.json'),key=os.path.abspath): #Найдем все json файлы в папке и отсортируем по пути
  from_json = json.load(open(f))
  for i in from_json:
    result.append({'phoneme':i['phoneme'],'lips_points':i['lips_points']})

json.dump(result, open(out_filepath,'w'))
print('JSONs was stretched to: %s'%(out_filepath))
