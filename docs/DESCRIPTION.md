## В работе использованы
- [Функция silentremove](https://stackoverflow.com/questions/10840533/most-pythonic-way-to-delete-a-file-which-may-not-exist) - удаление файла, если он существует
- [Moviepy](https://github.com/Zulko/moviepy) - нарезка видео
- [ffmpeg](https://github.com/kkroening/ffmpeg-python) - для извлечения аудио
- [pytube](https://github.com/nficano/pytube/tree/8c598376bb2432a5ff25ef2cd0ed1080236d5d62) - работа с ютуб видео (скачивание видео, скачивание суббтитров, получение мета-информации)
- [praatIO](https://github.com/timmahrt/praatIO) - парсер TextGrid
  - [Документация с примерами](https://nbviewer.jupyter.org/github/timmahrt/praatIO/blob/master/tutorials/tutorial1_intro_to_praatio.ipynb#installing_praatio) 
- [face-recognition](https://github.com/ageitgey/face_recognition) - Библиотека для распознавания лица + выделения ключевых точек
  - [Пример как работать с cv2 и библиотекой](https://github.com/ageitgey/face_recognition/blob/master/examples/blur_faces_on_webcam.py)
  - [Пример как работать с точками лица](https://github.com/ageitgey/face_recognition/blob/master/examples/digital_makeup.py)
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
## Полезные ссылки
- [Форматирование MD страниц](https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax)
- [Инофрмация про FPS](https://balyberdin.com/hey/all/about-fps/)
- [Хороший сайт про Git](https://rogerdudler.github.io/git-guide/)
- [Инфа про Git 1](https://progr.interplanety.org/en/how-to-start-working-with-git-and-github/)
- [Инфа про Git 2](https://opensource.com/article/18/1/step-step-guide-git)
- [Инфа про Git 3](https://proglib.io/p/git-github-gitflow)
- [Инфа про Git 4](https://htmlacademy.ru/blog/boost/tools/git-console)
- [Запись файлов](https://pyneng.readthedocs.io/ru/latest/book/07_files/3_write.html)
- [Примеры графиков matplotlib](https://habr.com/ru/post/468295/)
- [Инфа про figsize в matplotlib](https://stackoverflow.com/questions/47633546/relationship-between-dpi-and-figure-size)
- [Шпаргалка по Pandas](https://habr.com/ru/company/ruvds/blog/494720/)
- [Документация по Pandas](https://pandas.pydata.org/docs/#)
- [Инфа по Pandas](https://python.ivan-shamaev.ru/pandas-series-and-dataframe-objects-build-index/)
- [cURL to Python](https://curl.trillworks.com)
