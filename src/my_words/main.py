import atexit

import flet as ft
from interface import Words_chose
from my_w import Subtitles, Words
from users import Users


def main(page: ft.Page):
    page.title = "My Words"
    users_data = Users()
    user_name = ft.TextField(label="Enter your name")

    if name := users_data.user:
        words = Words(users_data.user)
    else:
        name = "No name"
        words = None

    text_name = ft.Container(
        content=ft.Text(name, italic=True),
        bgcolor=ft.colors.ORANGE,
        padding=5,
        border_radius=ft.border_radius.all(5),
    )

    def create(e):
        nonlocal words
        if not user_name.value:
            user_name.error_text = "Name cannot be blank!"
            user_name.update()
        elif user_name.value in users_data.users:
            user_name.error_text = "Choose a different name!"
            user_name.update()
        else:
            page.dialog.open = False
            name = user_name.value
            users_data.user = name
            users_data.users.append(name)
            user_name.value = ""
            text_name.content.value = name
            g_s.disabled = False
            words = Words(users_data.user)
            page.update()

    dlg_create = ft.AlertDialog(
        title=ft.Text("Welcome!"),
        content=ft.Column([user_name], tight=True),
        actions=[ft.ElevatedButton(text="Create", on_click=create)],
        actions_alignment="end",
    )

    dlg_change = ft.AlertDialog(
        title=ft.Text("Select a profile"),
        actions_alignment="end",
    )

    def create_user(e):
        page.dialog = dlg_create
        dlg_create.open = True
        page.update()

    def change(e):
        nonlocal words
        nonlocal row_words
        name = dlg_change.actions[0].value
        if name:
            users_data.user = name
            text_name.content.value = name
            dlg_change.open = False
            words.write_data()
            words = Words(users_data.user)
            row_words.words = words
            row_words.container_words()
            page.update()

    def change_user(e):
        page.dialog = dlg_change
        dlg_change.actions = [ft.Dropdown(
                width=100,
                options=[ft.dropdown.Option(v) for v in users_data.users]
                ),
            ft.ElevatedButton(text="Change", on_click=change)
        ]
        dlg_change.open = True
        page.update()

    row_words = Words_chose(words, page)
    row_words.container_words()
    g_s = Subtitles(words, page, users_data, row_words)

    r = ft.Row(wrap=True, scroll="always",)
    r.controls.append(text_name)
    r.controls.append(
        ft.ElevatedButton("Create a profile", on_click=create_user))
    r.controls.append(
        ft.ElevatedButton("Change a profile", on_click=change_user))
    r.controls.append(g_s)
    page.add(r)
    page.add(row_words)

    atexit.register(users_data.save_data)
    atexit.register(words.write_data)


if __name__ == '__main__':
    ft.app(target=main)
