## Структура проекта
- [README.md](README.md) - Описание репозитория
- [requirements.txt](requirements.txt) - Список зависимостей
- [Документация](docs/)
  - [FORMALIZATION.MD](docs/FORMALIZATION.md) - формальное описание работы: проблематика, цели, задачи, развитие и пр.
  - [DESCRIPTION.MD](docs/DESCRIPTION.md) - комментарии, описание, полезные ссылки
  - [maus_phonemes_info.txt](docs/maus_phonemes_info.txt) - информация по фонемам с сервиса MAUS
- [Скрипты](scripts/)
  - [maus_phonemes_info.txt](docs/maus_phonemes_info.txt) - информация по фонемам с сервиса MAUS
  - [get_info_from_youtube.py](scripts/get_info_from_youtube.py) - получения с Youtube-видео: русских суббтитров в txt формате (без знаков препинания, парсинг из srt),исходного видео в mp4, обрезанного видео (передаются секунды до и после) в mp4, дорожки обрезанного видео в wav и mp3
  - [get_maus_textgrid.py](scripts/get_maus_textgrid.py) - получение разметки аудиодорожки в формате textGrid при помощи MAUS-TextAlignment
  - [create_words_phonemes_dict.py](scripts/create_words_phonemes_dict.py) - создание из словаря слов - словаря слово->фонемная транскрипция
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
- --u - ссылка на видео
- --p - путь к папке, в которую будет помещен файл subtitles.txt. Дефолтно: /default
- --s - секунда старта для обрезки видео
- --e - секунда окончания для обрезки видео

### Получение разметки аудиодорожки в формате textGrid при помощи MAUS-TextAlignment
```
python get_maus_textgrid.py --a '/content/pedagog/audio.wav' --t '/content/pedagog/subtitles.txt' --o '/content/pedagog/maus_out.TextGrid'
```
- --a - путь к wav файлу
- --t - путь к txt файлу текстовой аннотации (транскрипции для wav файла)
- --o - путь к TextGrid файлу, который будут создан

## Cоздание из словаря слов - словаря слово->фонемная транскрипция
```
python create_words_phonemes_dict.py --i '/content/words_1_5kk.txt' --o '/content/words_phonemes_1_5kk.txt'
```
- --i - путь к входному файлу словоря
- --o - путь для выходного файла словаря слов->фонемной транскрипции

## Todo-лист
- [X] 1. ~~Создать файл с зависимостями - requirements.txt~~
- [X] 2. ~~Создать скрипт для получения с Youtube-видео: русских суббтитров в txt формате (без знаков препинания, парсинг из srt),исходного видео в mp4, обрезанного видео (передаются секунды до и после) в mp4, дорожки обрезанного видео в wav и mp3~~
- [X] 3. ~~Создать скрипт для получения разметки аудиодорожки в формате textGrid при помощи MAUS-TextAlignment~~
- [ ] 4. Создать скрипт для получения из словаря слов - словаря слово->фонемная транскрипция
- [ ] 5. Добавить словари: слова->транскрипции по фонемам, словарь фонем (с ключом и значением, для работы классификатора), словарь фонем с примерами использования
- [ ] 6. Придумать решение проблемы c фонемами а и о. Пример проблемы:
  - аббатскому;a b b a t s k a m u
  - аббатскою;a b b a t s k o j u
