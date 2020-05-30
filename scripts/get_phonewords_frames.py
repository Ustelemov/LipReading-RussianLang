from praatio import tgio
import os
import fileinput

import argparse

#Конфигурация параметров при вызове с консоли
parser = argparse.ArgumentParser(usage='Create phonemes by frames, phonemes trancription by frames, words by frames files')
parser.add_argument('--f', dest="fps",type=float,default=25.0,help='Frames-per-second in video')
parser.add_argument('--p',dest="path",type=str,default="/default",help="Path where to store files")
parser.add_argument('--t',dest="tg_path",type=str,required=True,help="Path to TextGrid input file")
parser.add_argument('--d',dest='phonemekeys_dict',type=str,default='./dicts/phonemes_keys.txt')


args = parser.parse_args()

tg_path = args.tg_path

#Паузы TextAligner представляет в виде: text = ""
#При парсинге эти промежутки будут пропущены, для этого заменим в файле "" на "<:silence>"
with fileinput.FileInput(tg_path, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace("text = \"\"", "text = \"<silence:>\""), end='')

fps = args.fps

phonemekeys_dict = '/content/phonemes_keys.txt'

output_path = '/content/pedagog'

tg = tgio.openTextgrid(tg_path)
russian_words = tg.tierDict['ORT-MAU'].entryList
phonemes_words = tg.tierDict['KAN-MAU'].entryList
phonemes = tg.tierDict['MAU'].entryList

phonemes_frames_out = output_path+'/phonemes_frames.txt'
phonemekeys_frames_out = output_path+'/phonemekeys_frames.txt'
phonemeswords_frames_out = output_path+'/phonemeswords_frames.txt'
words_frames_out = output_path+'/words_frames.txt'

#convert_to_keys определяет будут ли фонемы преобразованы в ключи
def make_phonemes_frames_file(output_file,input_dict,fps,phonemes_keys_file,convert_to_keys=True):
  key_to_phonemes = {}
  with open(phonemes_keys_file,'r') as f:
    lines = f.readlines()
    for line in lines:
      list = line.split(' ')
      #Если требуется перевести в ключи фонем, то ключом в словарем будет фонема, а значением число
      if convert_to_keys:
        key_to_phonemes[list[0]] = list[1].split('\n')[0]
      else: #В пративном случаем (если оставляем фонемы в файле), то ключ и значения оставим одинаковыми
        key_to_phonemes[list[0]] = list[0]

  
  with open(output_file, 'w') as f:
    for el in input_dict:
      start_frame = (int)(el.start*fps) #Стратовый фрейм фонемы
      end_frame = (int)(el.end*fps) #Конечный фрейм фонемы
      lab = el.label
      for i in range(start_frame,end_frame):
        if(i!=0): #Чтобы лишний \n не ставить в конце
           f.write('\n')
        f.write(key_to_phonemes[lab])

def make_words_frames_file (output_file,input_dict,fps):
  with open(output_file, 'w') as f:
    for el in input_dict:
      start_frame = (int)(el.start*fps) #Стартовый фрейм слова
      end_frame = (int)(el.end*fps) #Конечный фрейм слова
      lab = el.label
      
      for i in range(start_frame,end_frame):
        if(i!=0): #Чтобы лишний \n не ставить в конце
           f.write('\n')
        f.write(lab)

#проверяем, есть ли папка - создаем, если нет
output_path_exists = os.path.exists(output_path)
if not output_path_exists:
    os.makedirs(output_path)




#Список фонем по фреймам
make_phonemes_frames_file(phonemes_frames_out,phonemes,fps,phonemekeys_dict,convert_to_keys=False)
#Список ключей фонем по фреймам
make_phonemes_frames_file(phonemekeys_frames_out,phonemes,fps,phonemekeys_dict,convert_to_keys=True)

#Список фонемных транскрипций по фреймам
make_words_frames_file(phonemeswords_frames_out,phonemes_words,fps)
#Список слов по фреймам
make_words_frames_file(words_frames_out,russian_words,fps)

print('Files successful create in %s'%(output_path))
print(phonemes_words)
