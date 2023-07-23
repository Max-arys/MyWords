import json
import re

from youtube_transcript_api import YouTubeTranscriptApi


class Words:

    def __init__(self, user):
        self.user = user
        try:
            with open(
                    rf'MyWords\src\my_words\data\{self.user}_my_worlds.json',
                    'r'
                    ) as m_w:
                self.my_words = set(json.load(m_w))
            with open(
                    rf'MyWords\src\my_words\data\{self.user}_new_words.json',
                    'r'
                    ) as n_w:
                self.new_words = set(json.load(n_w))
        except FileNotFoundError:
            self.my_words = set()
            self.new_words = set()

    def write_data(self):
        # Запись новых слов в nev_words
        with open(
                rf'MyWords\src\my_words\data\{self.user}_new_words.json', 'w'
                ) as n_w:
            json.dump(list(self.new_words), n_w, indent=2)
        # Запись новых слов в my_worlds
        with open(
                rf'MyWords\src\my_words\data\{self.user}_my_worlds.json', 'w'
                ) as m_w:
            json.dump(list(self.my_words), m_w, indent=2)

    # Отсеивает знакомые слова в сабах
    def check_from_sub(self, video_id):
        for v in YouTubeTranscriptApi.get_transcript(video_id):
            self.new_words.update(
                re.findall(r'[A-Za-z\']+', v['text'].lower())
                )
        self.new_words = self.new_words - self.my_words


if __name__ == '__main__':
    video_id = 'Dn33_uncuzk'
    words = Words('Max')
    words.check_from_sub(video_id)
    print(words.new_words)
    print('----------------------')
    print(words.my_words)
    words.write_data()
