import os
import argparse
import glob



#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Stretch txt files in folder to txt')
parser.add_argument('--i',dest="input_path",type=str,required=True,help="Path to files")
parser.add_argument('--o',dest="out_filepath",type=str,required=True,help="Path to output txt file")


args = parser.parse_args()

input_path = args.input_path
out_filepath = args.out_filepath


with open(out_filepath,'w') as w: #Откроем файл для записи 
  files_array = sorted(glob.glob(input_path+'/*.txt'),key=os.path.abspath) #Найдем все txt файлы в папке и отсортируем по пути (если цифра больше, то файл будет позже)
  for indx,file_path in enumerate(files_array):  
    with open(file_path,'r') as r:
      print(r)
      #Запишем в файл прочитанные сторки (readlines) файла
      if indx!=len(files_array)-1:
        w.writelines(r.readlines()+'\n')
      else:
        w.writelines(r.readlines())
        
