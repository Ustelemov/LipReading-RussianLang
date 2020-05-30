## В работе использованы
- [Функция silentremove](https://stackoverflow.com/questions/10840533/most-pythonic-way-to-delete-a-file-which-may-not-exist) - удаление файла, если он существует
- [Moviepy](https://github.com/Zulko/moviepy) - нарезка видео
- [ffmpeg](https://github.com/kkroening/ffmpeg-python) - для извлечения аудио
- [pytube](https://github.com/nficano/pytube/tree/8c598376bb2432a5ff25ef2cd0ed1080236d5d62) - работа с ютуб видео (скачивание видео, скачивание суббтитров, получение мета-информации)

## Документация по запросам к сервисам MAUS
Может быть получена по запросу
```
curl -X GET http://clarin.phonetik.uni-muenchen.de/BASWebServices/services/help
```
Результат запроса приведен в [файле](maus_service_help.txt)

## Получение словаря G2P (Graphema-To-Phonema) 
- Словарь русских слов (1531461 слов) взят с репозитория: https://github.com/danakt/russian-words
- Для работы с G2P-MAUS (преобразователь слов в фонемную транскрипцию) требуется удалить знаки '.' и '-', а после - очистить от образовавшихся дублей
- В скрипте [create_words_phonemes_dict.py](./scripts/create_words_phonemes_dict.py) используется [G2P-MAUS-Service](https://clarin.phonetik.uni-muenchen.de/BASWebServices/interface/Grapheme2Phoneme) c Output Symbol inventory - maus-sampa, т.к. TextAligner-MAUS выдает результат также в данной нотации

## Как скачать папку в форме zip-архив с Google Colab
Информация с [stackoverflow](https://stackoverflow.com/questions/50453428/how-do-i-download-multiple-files-or-an-entire-folder-from-google-colab)
```
!zip -r /content/pedagog.zip /content/pedagog
from google.colab import files
files.download("/content/pedagog.zip")
```
