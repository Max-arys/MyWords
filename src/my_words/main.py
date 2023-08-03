import atexit

import flet as ft
from my_w import Subtitles, Words, Words_chose
from users import BottomChange, BottomCreate, NameBadge, Users


def main(page: ft.Page):
    page.title = "My Words"
    users_data = Users()
    words = Words(users_data.user)
    name = users_data.user if users_data.user else "???"
    text_name = NameBadge(name)
    row_words = Words_chose(words, page)
    row_words.container_words()
    g_s = Subtitles(words, page, users_data, row_words)

    r = ft.Row(wrap=True, scroll="always")
    r.controls.append(text_name)
    r.controls.append(
        BottomCreate(page, users_data, g_s, text_name, words))
    r.controls.append(
        BottomChange(page, users_data, text_name, row_words, words))
    r.controls.append(g_s)
    page.add(r)
    page.add(row_words)

    atexit.register(words.write_data)
    atexit.register(users_data.save_data)


if __name__ == '__main__':
    ft.app(target=main)
