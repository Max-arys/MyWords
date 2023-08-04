import json
from pathlib import Path

import flet as ft
from words import RowsWords, Subtitles, Words

dir_path = Path.cwd()
file_path = Path(dir_path, 'data', 'users.json')
file_path = r'data\users.json'


class Users:
    def __init__(self):
        self.d_users = self.get_users()
        self.users = self.d_users["users"]
        self.user = self.d_users["user"]

    def get_users(self):
        try:
            with open(file_path, 'r') as u:
                return json.load(u)
        except FileNotFoundError:
            return {"user": "", "users": []}

    def save_users(self):
        with open(file_path, 'w') as u:
            self.d_users["users"] = self.users
            self.d_users["user"] = self.user
            json.dump(self.d_users, u)


class NameBadge(ft.Container):

    def __init__(self, name: str):
        self.name = name
        super().__init__()
        self.content = ft.Text(name, italic=True)
        self.bgcolor = ft.colors.ORANGE
        self.padding = 5
        self.border_radius = ft.border_radius.all(5)


class BottomCreate(ft.ElevatedButton):

    def __init__(self, page: ft.Page, users_data: Users, g_s: Subtitles,
                 text_name: NameBadge, words: Words):
        self.words = words
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
            if self.words.user:
                self.words.save_words()
            self.words.user = self.users_data.user
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
            self.words.save_words()
            self.words.user = self.users_data.user
            self.words.get_words()
            self.rows_words.words = self.words
            self.rows_words.add_container_words()
            self.page.update()
