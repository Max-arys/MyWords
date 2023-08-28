import json
import logging.config
from typing import List

import flet as ft
from setings import LOGGING_CONFIG, USERS_FILE
from words import RowsWords, Subtitles, Words

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Users:
    def __init__(self):
        self.user: str = None
        self.users: List[str] = None
        self.get_users()

    def get_users(self):
        try:
            with open(USERS_FILE, 'r') as u:
                d_users = json.load(u)
                self.user = d_users["user"]
                self.users = d_users["users"]
        except FileNotFoundError:
            self.user = ""
            self.users = []

    def save_users(self):
        with open(USERS_FILE, 'w') as u:
            d_users = {}
            d_users["user"] = self.user
            d_users["users"] = self.users
            json.dump(d_users, u)


class NameBadge(ft.Container):
    """A class for displaying the user's badge."""

    def __init__(self, name: str):
        self.name = name
        super().__init__()
        self.content = ft.Text(name, italic=True)
        self.bgcolor = ft.colors.ORANGE
        self.padding = 5
        self.border_radius = ft.border_radius.all(5)


class BottomCreateUser(ft.ElevatedButton):

    def __init__(self, page: ft.Page, users_data: Users, g_s: Subtitles,
                 text_name: NameBadge, rows_words: RowsWords, words: Words):
        self.words = words
        self.rows_words = rows_words
        self.text_name = text_name
        self.g_s = g_s
        self.users_data = users_data
        self.page = page
        self.user_name = ft.TextField(label="Enter your name")
        self.dlg_create = ft.AlertDialog(
            title=ft.Text("Welcome!"),
            content=ft.Column([self.user_name], tight=True),
            actions=[ft.ElevatedButton(
                text="Create", on_click=self.create_user)],
            actions_alignment="end",
        )
        super().__init__()
        self.text = "Create a profile"
        self.on_click = self.click_create_user

    def click_create_user(self, e):
        self.page.dialog = self.dlg_create
        self.dlg_create.open = True
        self.page.update()

    def create_user(self, e):
        if not self.user_name.value:
            self.user_name.error_text = "Name cannot be blank!"
            self.user_name.update()
        elif self.user_name.value in self.users_data.users:
            self.user_name.error_text = "Choose a different name!"
            self.user_name.update()
        else:
            self.page.dialog.open = False
            name = self.user_name.value
            self.users_data.user = name
            self.users_data.users.append(name)
            self.user_name.value = ""
            self.text_name.content.value = name
            self.g_s.disabled = False
            self.rows_words.refresh_row_words(name)
            self.page.update()


class BottomChange(ft.ElevatedButton):

    def __init__(self, page: ft.Page, users_data: Users, text_name: NameBadge,
                 rows_words: RowsWords, words: Words):
        self.words = words
        self.rows_words = rows_words
        self.text_name = text_name
        self.users_data = users_data
        self.page = page
        self.dlg_change = ft.AlertDialog(
            title=ft.Text("Select a profile"),
            actions_alignment="end",
        )
        super().__init__()
        self.text = "Change a profile"
        self.on_click = self.click_change_user

    def click_change_user(self, e):
        self.page.dialog = self.dlg_change
        self.dlg_change.actions = [ft.Dropdown(
                width=100,
                options=[ft.dropdown.Option(v) for v in self.users_data.users]
                ),
            ft.ElevatedButton(text="Change", on_click=self.change_user)
        ]
        self.dlg_change.open = True
        self.page.update()

    def change_user(self, e):
        name = self.dlg_change.actions[0].value
        if name:
            self.users_data.user = name
            self.text_name.content.value = name
            self.dlg_change.open = False
            self.rows_words.refresh_row_words(name)
            self.page.update()
