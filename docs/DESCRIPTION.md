## Получение словаря G2P (Graphema-To-Phonema) 
- Словарь русских слов (1531461 слов) взят с репозитория: https://github.com/danakt/russian-words
- Для работы с G2P-MAUS (преобразователь слов в фонемную транскрипцию) требуется удалить знаки '.' и '-', а после - очистить от образовавшихся дублей
- В скрипте [create_words_phonemes_dict.py](./scripts/create_words_phonemes_dict.py) используется [G2P-MAUS-Service](https://clarin.phonetik.uni-muenchen.de/BASWebServices/interface/Grapheme2Phoneme) c Output Symbol inventory - maus-sampa, т.к. TextAligner-MAUS выдает результат также в данной нотации

