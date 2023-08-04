import json
import re
from pathlib import Path
from typing import Set

import flet as ft
from youtube_transcript_api import YouTubeTranscriptApi


class Words:
    """Class has methods save_words() and check_from_sub(video_id: str)"""

    def __init__(self, user: str):
        self.user = user
        self.my_words: Set[str] = set()
        self.new_words: Set[str] = set()
        self.get_words()

    def get_path_my_w(self):
        return Path(Path.cwd(), 'data', f'{self.user}_my_worlds.json')

    def get_patch_nev_w(self):
        return Path(Path.cwd(), 'data', f'{self.user}_new_words.json')

    def get_words(self):
        try:
            with open(self.get_path_my_w(), 'r') as m_w:
                self.my_words = set(json.load(m_w))
            with open(self.get_patch_nev_w(), 'r') as n_w:
                self.new_words = set(json.load(n_w))
        except FileNotFoundError as err:
            print(err)

    def save_words(self):
        if self.user:
            # Запись новых слов в my_worlds
            with open(self.get_path_my_w(), 'w') as m_w:
                json.dump(list(self.my_words), m_w, indent=2)

            # Запись новых слов в nev_words
            with open(self.get_patch_nev_w(), 'w') as n_w:
                json.dump(list(self.new_words), n_w, indent=2)

    # Отсеивает знакомые слова в сабах check_from_sub
    def get_words_subs(self, video_id: str):
        for v in YouTubeTranscriptApi.get_transcript(video_id):
            self.new_words.update(
                re.findall(r'[A-Za-z\']+', v['text'].lower())
            )
        self.new_words = self.new_words - self.my_words


class RowsWords(ft.Row):
    COLOR_OF_SELECTED = ft.colors.AMBER_500
    COLOR_OF_NOT_SELECTED = ft.colors.AMBER_100

    def __init__(self, words: Words, page: ft.Page):
        self.words = words
        self.page = page
        super().__init__()
        self.wrap = True
        self.scroll = "always"
        self.expand = True
        self.click = self.container_click

    def container_click(self, e):
        word = e.control.content.value

        if e.control.bgcolor == self.COLOR_OF_NOT_SELECTED:
            e.control.bgcolor = self.COLOR_OF_SELECTED
            self.words.new_words.remove(word)
            self.words.my_words.add(word)
        else:
            e.control.bgcolor = self.COLOR_OF_NOT_SELECTED
            self.words.my_words.remove(word)
            self.words.new_words.add(word)
        self.page.update()

    def add_container_words(self):
        items = []
        for i in self.words.new_words:
            items.append(
                ft.Container(
                    ft.Text(i),
                    width=100,
                    height=50,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.AMBER_100,
                    border=ft.border.all(1, ft.colors.AMBER_400),
                    border_radius=ft.border_radius.all(5),
                    on_click=self.click,
                )
            )
        self.controls = items


class Subtitles(ft.ElevatedButton):

    def __init__(self, words: Words, page: ft.Page, users_data,
                 rows_words: RowsWords):
        self.rows_words = rows_words
        self.page = page
        self.words = words
        self.users_data = users_data
        self.youtube_id = ft.TextField(label="Enter video ID")
        self.dlg_subtitles = ft.AlertDialog(
            title=ft.Text("Enter the video ID"),
            content=ft.Column([self.youtube_id], tight=True),
            actions=[ft.ElevatedButton(
                text="Get", on_click=self.get_subtitles)],
            actions_alignment="end",
        )
        super().__init__()
        self.text = "Get subtitles"
        self.on_click = self.click_sub
        self.disabled = False if self.users_data.user else True

    def click_sub(self, e):
        self.page.dialog = self.dlg_subtitles
        self.dlg_subtitles.open = True
        self.page.update()

    def get_subtitles(self, e):
        self.page.dialog.open = False
        self.words.get_words_subs(self.youtube_id.value)
        self.rows_words.add_container_words()
        self.youtube_id.value = ""
        self.page.update()
