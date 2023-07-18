import json
import re

from youtube_transcript_api import YouTubeTranscriptApi


def check_words(video_id):

    def get_my_words():
        with open(r'MyWords\src\my_words\data\my_worlds.json', 'r') as m_w:
            return json.load(m_w)

    def write_data(my_words, nev_words):
        # Запись новых слов в nev_words
        with open(r'MyWords\src\my_words\data\nev_words.json', 'w') as n_w:
            json.dump(list(nev_words), n_w, indent=2)
        # Запись новых слов в my_worlds
        with open(r'MyWords\src\my_words\data\my_worlds.json', 'w') as m_w:
            json.dump(my_words, m_w, indent=2)

    # Ручной выбор знакомых слов
    def select_words(my_words, nev_words):
        for v in list(nev_words):
            if input(f'{v}: ') == '+':
                my_words.append(v)
                nev_words.remove(v)

    # Отсеивает знакомые слова в сабах
    def check_from_sub():
        my_words = get_my_words()
        nev_words = []
        for v in YouTubeTranscriptApi.get_transcript(video_id):
            nev_words.extend(re.findall(r'[A-Za-z\']+', v['text'].lower()))
        nev_words = set(nev_words) - set(my_words)
        select_words(my_words, nev_words)
        write_data(my_words, nev_words)

    # Отсеивавет знакомые слова в файле nev_words
    def check_from_file():
        my_words = get_my_words()
        with open(r'MyWords\src\my_words\data\nev_words.json', 'r') as n_w:
            nev_words = json.load(n_w)
        nev_words = set(nev_words) - set(my_words)
        select_words(my_words, nev_words)
        write_data(my_words, nev_words)

    try:
        if video_id:
            check_from_sub()
        else:
            check_from_file()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    video_id = 'Dn33_uncuzk'
    check_words(video_id)
