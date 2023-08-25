import atexit
import logging.config

import flet as ft
from setings import LOGGING_CONFIG
from users import BottomChange, BottomCreate, NameBadge, Users
from words import RowsWords, Subtitles, Words

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('my_words')


def main(page: ft.Page):
    logger.info('session start')
    page.title = "My Words"
    users_data = Users()
    words = Words(users_data.user)
    name = users_data.user if users_data.user else "???"
    text_name = NameBadge(name)
    rows_words = RowsWords(words, page)
    rows_words.add_container_words()
    g_s = Subtitles(words, page, users_data, rows_words)

    r = ft.Row(wrap=True, scroll="always")
    r.controls.append(text_name)
    r.controls.append(
        BottomCreate(page, users_data, g_s, text_name, rows_words, words))
    r.controls.append(
        BottomChange(page, users_data, text_name, rows_words, words))
    r.controls.append(g_s)
    page.add(r)
    page.add(rows_words)

    logger.info('session end')
    atexit.register(words.save_words)
    atexit.register(users_data.save_users)


if __name__ == '__main__':
    ft.app(target=main)
