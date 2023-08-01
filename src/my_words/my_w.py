import json
import re

import flet as ft
from youtube_transcript_api import YouTubeTranscriptApi


class Words:
    """Class has methods write_data() and check_from_sub(video_id: str)"""

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
    def check_from_sub(self, video_id: str):
        for v in YouTubeTranscriptApi.get_transcript(video_id):
            self.new_words.update(
                re.findall(r'[A-Za-z\']+', v['text'].lower())
            )
        self.new_words = self.new_words - self.my_words


class Subtitles(ft.ElevatedButton):

    def __init__(self, words, page, users_data, row_words):
        self.row_words = row_words
        self.page = page
        self.words = words
        self.users_data = users_data
        self.youtube_id = ft.TextField(label="Enter video ID")
        self.dlg_subtitles = ft.AlertDialog(
            title=ft.Text("Enter the video ID"),
            content=ft.Column([self.youtube_id], tight=True),
            actions=[ft.ElevatedButton(text="Get", on_click=self.subtitles)],
            actions_alignment="end",
        )
        super().__init__()
        self.text = "Get subtitles"
        self.on_click = self.get_subtitles
        self.disabled = False if self.users_data.user else True

    def get_subtitles(self, e):
        self.page.dialog = self.dlg_subtitles
        self.dlg_subtitles.open = True
        self.page.update()

    def subtitles(self, e):
        self.page.dialog.open = False
        self.words.check_from_sub(self.youtube_id.value)
        self.row_words.container_words()
        self.youtube_id.value = ""
        self.page.update()


if __name__ == '__main__':
    ...
