Данный проект разрабатывался в качестве НИР на 1-курсе

## Структура проекта
- [README.md](README.md) - Описание репозитория
- [requirements.txt](requirements.txt) - Список зависимостей
- [Документация]
- [Скрипты](scripts/)
  - get_info_from_youtube.py - получения с Youtube-видео: русских суббтитров в txt формате (без знаков препинания, парсинг из srt),исходного видео в mp4, обрезанного видео (передаются секунды до и после) в mp4, дорожки обрезанного видео в wav и mp3
## Использование
### 
### Установка зависимостей
Для установки всех требуемых зависимостей воспользуйтесь командой:
```
pip install -r requirements.txt
```
### Получение информации с Youtube-видео
```
python get_info_from_youtube.py --u 'https://www.youtube.com/watch?v=vyhzVJBln6k' --p '/content/pedagog' --s 0 --e 68
```
- --u - ссылка на видео
- --p - путь к папке, в которую будет помещен файл subtitles.txt. Дефолтно: /default
- --s - секунда старта для обрезки видео
- --e - секунда окончания для обрезки видео

### Получение textGrid от MAUS TextAlignment
```
python get_maus_textgrid.py --a '/content/pedagog/audio.wav' --t '/content/pedagog/subtitles.txt' --p '/content/pedagog'
```
- --a - путь к wav файлу
- --t - путь к txt файлу текстовой аннотации (транскрипции для wav файла)
- --p - путь к папке, в которую будет положен выходной maus_out.TextGrid file

## Todo-лист
- [X] 1. ~~Создать файл с зависимостями - requirements.txt~~
- [X] 2. ~~Создать скрипт для получения с Youtube-видео: русских суббтитров в txt формате (без знаков препинания, парсинг из srt),исходного видео в mp4, обрезанного видео (передаются секунды до и после) в mp4, дорожки обрезанного видео в wav и mp3~~
- [X] 3. ~~Создать скрипт для получения textGrid с MAUS TextAligner~~
- [ ] 4. Создать скрипт для получения из словаря слов словаря слово->фонемная транскрипция
- [ ] 5. Добавить словари: слова->транскрипции по фонемам, словарь фонем (с ключом и значением, для работы классификатора), словарь фонем с примерами использования
