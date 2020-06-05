import os
import argparse

#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Stretch two txt files to one')
parser.add_argument('--f',dest="first_filepath",type=str,required=True,help="Path to first file")
parser.add_argument('--s',dest="second_filepath",type=str,required=True,help="Path to second file")
parser.add_argument('--o',dest="out_filepath",type=str,required=True,help="Path to outputfile")


args = parser.parse_args()

first_filepath = args.first_filepath
second_filepath = args.second_filepath
out_filepath = args.out_filepath

first_lines = []
second_lines = []

#Получаемые данные из первого файла
with open(first_filepath,'r') as f:
  first_lines = f.readlines()

#Получаемые данные из второго файла
with open(second_filepath,'r') as f:
  second_lines = f.readlines()

#Записываем данные в выходной файл
with open(out_filepath,'w') as f:
  f.writelines(first_lines) #Запишем данные первого файла
  f.writelines(second_lines) #Запишем данные второго файла

print('Files was stretched in: %s'%(out_filepath))
