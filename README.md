## Структура проекта
- [README.md](README.md) - Описание репозитория
- [requirements.txt](requirements.txt) - Список зависимостей
- [Документация](docs/)
  - [FORMALIZATION.MD](docs/FORMALIZATION.md) - формальное описание работы: проблематика, цели, задачи, развитие и пр.
  - [DESCRIPTION.MD](docs/DESCRIPTION.md) - комментарии, описание, полезные ссылки
  - [maus_phonemes_info.txt](docs/maus_phonemes_info.txt) - информация по фонемам с сервиса MAUS
  - [maus_service_help.txt](docs/maus_service_help.txt) - документация по запросам к сервисам MAUS
- [Скрипты](scripts/)
  - [get_info_from_youtube.py](scripts/get_info_from_youtube.py) - получения с Youtube-видео: русских суббтитров в txt формате (без знаков препинания, парсинг из srt),исходного видео в mp4, обрезанного видео (передаются секунды до и после) в mp4, дорожки обрезанного видео в wav
  - [get_maus_textgrid.py](scripts/get_maus_textgrid.py) - получение разметки аудиодорожки в формате textGrid при помощи MAUS-TextAlignment
  - [create_words_phonemes_dict.py](scripts/create_words_phonemes_dict.py) - создание из словаря слов - словаря слово->фонемная транскрипция
  - [get_phonewords_frames.py](scripts/get_phonewords_frames.py) - получение файлов: русских слов по кадрам (из транскрипции), фонем по кадрам (самих фонем и ключей из словаря - нужно для классификатор в дальнейшем), фонемных транскрипций по кадрам
  - [get_phonemes_duration_stat.py](scripts/python get_phonemes_duration_stat.py) - получение статистики по длительности фонем в кадрах (в разрезе каждой фонемы и в целом): min,max,mean,std,sum,sum_percent
  - [get_phonemes_appearence_stat.py](scripts/get_phonemes_appearence_stat.py) - получение статистике по количеству встреч фонем: сколько раз использовалась фонема, независимо от длины в кадрах
- [Cловари](dicts/)
  - [words_phonemes_1_5kk.txt](dicts/words_phonemes_1_5kk.txt) - словарь {слово; фонемная транскрипция}. Содержит 1531154 слов. Удалены слова с пробелами и несловарными символами (кроме -), слова с - слиты в одно слово (- заменено на пустоту)
  - [phonemes_with_examples.txt](dicts/phonemes_with_examples.txt) - словарь фонем с примерами слов
  - [phonemes_keys.txt](dicts/phonemes_keys.txt) - словарь фонем с ключами
## Использование
### Установка (клонирование)
```
git clone https://github.com/Ustelemov/LiReading-RussianLang
```
### Установка зависимостей
Для установки всех требуемых зависимостей воспользуйтесь командой:
```
pip install -r requirements.txt
```
### Получение информации с Youtube-видео
```
python get_info_from_youtube.py --u 'https://www.youtube.com/watch?v=vyhzVJBln6k' --p '/content/pedagog' --s 0 --e 68
```
- --u - ссылка на видео {Обязательный аргумент}
- --p - путь к папке, в которую будет помещен файлы.txt. Дефолтно: /default
- --s - секунда старта для обрезки видео. Дефолтно: 0. Если оставить нулем или указать 0 явно (то есть, если s==e==0), то файл будет использован целиком
- --e - секунда окончания для обрезки видео. Дефолтно: 0. Если оставить нулем или указать 0 явно (то есть, если s==e==0), то файл будет использован целиком


Файлы:
- video_ytb.mp4 - исходный файл, скачанный с ютуба
- video.mp4 - обрезанный файл из video_ytb.mp4, используется для извлечение аудиодорожки (если файл не обрязается - то данный файл не создается, для извлечения аудиодорожки используется исходный файл)
- audio.wav - аудиодорожка, созданная по video.mp4
- subtitles.txt - русские суббтитры (если есть, если нет - в консоли появится соответствующее сообщение), полученные с Youtube

### Получение разметки аудиодорожки в формате textGrid при помощи MAUS-TextAlignment
```
python get_maus_textgrid.py --a '/content/pedagog/audio.wav' --t '/content/pedagog/subtitles.txt' --o '/content/pedagog/maus_out.TextGrid'
```
- --a - путь к wav файлу {Обязательный аргумент}
- --t - путь к txt файлу текстовой аннотации (транскрипции для wav файла) {Обязательный аргумент}
- --o - путь к TextGrid файлу, который будут создан. Дефолтно: /default/maus_out.TextGrid

## Cоздание из словаря слов - словаря слово->фонемная транскрипция
```
python create_words_phonemes_dict.py --i '/content/words_1_5kk.txt' --o '/content/words_phonemes_1_5kk.txt'
```
- --i - путь к входному файлу словоря {Обязательный аргумент}
- --o - путь для выходного файла словаря слов->фонемной транскрипции. Дефолтно: /default/out_words.txt

## Создание русских слов по кадрам (из транскрипции), фонем по кадрам (самих фонем и ключей из словаря - нужно для классификатор в дальнейшем), фонемных транскрипций по кадрам
```
python get_phonewords_frames.py --p '/content/pedagog' --t '/content/out.TextGrid'  --d '/content/LiReading-RussianLang/dicts/phonemes_keys.txt 
```
- --p - путь к выходной папке, в которую буду помещены файлы. Дефолтно: /default
- --t - путь к TextGrid файлу {Обязательный аргумент}
- --f - кол-во FPS в видео. Дефолтно 25.0
- --d - путь к словарю фонем с ключами {Обязательный аргумент}
Файлы:
- phonemekeys_frames.txt - ключи фонем по кадрам
- phonemes_frames.txt - фонемы по кадрам
- phonemeswords_frames.txt - фонемные транскрипции по кадрам
- words_frames.txt - слова по кадрам

## Cкрипт для получения статистики о встречи фонем
```
python get_phonemes_appearence_stat.py --p '/content/stat1' --d '/content/phonemes_keys.txt' --f '/content/phonemes_frames.txt'
```
- --p - путь к выходной папке, в которую буду помещены файлы. Дефолтно: /default
- --d - путь к словарю фонем с ключами {Обязательный аргумент}
- --f - путь к файлу фонем по кадрам {Обязательный аргумент}
- --e - требуется ли исключить фонемы (стандартно <:p>) из рассмотрения. Дефолтно: False

Информация:
- 1. Сколько раз фонема появлялась - график phonemes_appears_count.png с количество встреч каждой фонемы + расписанное в phonemes_appears_info.txt по каждой фонеме количество
- 2. Процент появлений от общего числа появлений - график phonemes_appears_percent с процентом встреч от общего количества встреч по каждой фонеме + расписанная в phonemes_appears_info.txt информация по каждой фонеме
- 3. Минимальное количество появлений - min в phonemes_appears_info.txt
- 4. Максимальное количество появлений - max в phonemes_appears_info.txt
- 5. Среднее количество появлений - mean в phonemes_appears_info.txt
 -6. Среднее квадратичное отклонение количества появлений - std в phonemes_appears_info.txt
 
## Скрипт для получения статистики по длительности фонем в кадрах
```
python get_phonemes_duration_stat.py --p '/content/stat1' --d '/content/phonemes_keys.txt' --f '/content/phonemes_frames.txt'
```
- --p - путь к выходной папке, в которую буду помещены файлы. Дефолтно: /default
- --d - путь к словарю фонем с ключами {Обязательный аргумент}
- --f - путь к файлу фонем по кадрам {Обязательный аргумент}
- --e - требуется ли исключить фонемы (стандартно <:p>) из рассмотрения. Дефолтно: False
 
Информация
- 1. Относительно каждой фонемы информация по длительности в кадрах:
  - 1.1. Минимальная длительность в кадрах по каждой фонеме - min в phonemes_duration_stat.txt, график - min_duration_graph.png
  - 1.2. Максимальная длительность в кадрах по каждой фонеме - max в phonemes_duration_stat.txt, график - max_duration_graph.png
  - 1.3. Средняя длительность в кадрах по каждой фонеме - mean в phonemes_duration_stat.txt, график - mean_duration_graph.png
  - 1.4. Отклонение длительности в кадрах по каждой фонеме - std в phonemes_duration_stat.txt, график - std_duration_graph.png
  - 1.5. Сумма длительности в кадрах по каждой фонеме - sum в phonemes_duration_stat.txt, график - sum_duration_graph.png
  - 1.6. Процент длительности фонемы в кадрах относительно всех кадров - sum_percent в phonemes_duration_stat.txt, график - sum_duration_percent_graph.png
- 2. Общая статистика по всем фонемам:
  - 2.1. Минимальная длительность в кадрах - min в phonemes_duration_stat.txt (блок общей статистики)
  - 2.2. Максимальная длительность в кадрах - max в phonemes_duration_stat.txt (блок общей статистики)
  - 2.3. Средняя длительность в кадрах - mean в phonemes_duration_stat.txt (блок общей статистики)
  - 2.4. Отклонение длительности в кадрах - std в phonemes_duration_stat.txt (блок общей статистики
 
## Todo-лист
- [X] 1. ~~Создать файл с зависимостями - requirements.txt~~
- [X] 2. ~~Создать скрипт для получения с Youtube-видео: русских суббтитров в txt формате (без знаков препинания, парсинг из srt),исходного видео в mp4, обрезанного видео (передаются секунды до и после) в mp4, дорожки обрезанного видео в wav~~
- [X] 3. ~~Создать скрипт для получения разметки аудиодорожки в формате textGrid при помощи MAUS-TextAlignment~~
- [X] 4. ~~Создать скрипт для получения из словаря слов - словаря слово->фонемная транскрипция~~
- [X] 5. ~~Добавить словари: слова->транскрипции по фонемам, словарь фонем (с ключом и значением, для работы классификатора), словарь фонем с примерами использования~~
- [X] 6. ~~Создать скрипт для получения файлов: русских слов по кадрам (из транскрипции), фонем по кадрам (самих фонем и ключей из словаря - нужно для классификатор в дальнейшем), фонемных транскрипций по кадрам~~
- [X] 7. ~~Создать скрипт для получения статистики о встречи фонем:~~
   - 7.1. ~~Сколько раз фонема появлялась~~
   - 7.2. ~~Процент появлений от общего числа появлений~~
   - 7.3. ~~Минимальное количество появлений~~
   - 7.4. ~~Максимальное количество появлений~~
   - 7.5. ~~Среднее количество появлений~~
   - 7.6. ~~Среднее квадратичное отклонение количества появлений~~
- [X] 8. ~~Создать скрипт для получения статистики по длительности фонем в кадрах:~~
   - 8.1. ~~Относительно каждой фонемы информация по длительности в кадрах:~~
     - 8.1.1. ~~Минимальная длительность в кадрах по каждой фонеме~~
     - 8.1.2. ~~Максимальная длительность в кадрах по каждой фонеме~~
     - 8.1.3. ~~Средняя длительность в кадрах по каждой фонеме~~
     - 8.1.4. ~~Отклонение длительности в кадрах по каждой фонеме~~
     - 8.1.5. ~~Сумма длительности в кадрах по каждой фонеме~~
     - 8.1.6. ~~Процент длительности фонемы в кадрах относительно всех кадров~~
   - 8.2. ~~Общая статистика по всем фонемам:~~
     - 8.2.1. ~~Минимальная длительность в кадрах~~
     - 8.2.2. ~~Максимальная длительность в кадрах~~
     - 8.2.3. ~~Средняя длительность в кадрах~~
     - 8.2.4. ~~Отклонение длительности в кадрах~~
- [ ] 9. Придумать решение проблемы c фонемами а и о. Пример проблемы:
  - аббатскому;a b b a t s k a m u
  - аббатскою;a b b a t s k o j u
