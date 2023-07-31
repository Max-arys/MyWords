import atexit

import flet as ft


class GreeterControl(ft.UserControl):
    def build(self):
        return ft.Text("Hello!")
    
    def pppr(self):
        print('Exit')


def main(page):
    a = GreeterControl()
    page.add(a)
    atexit.register(a.pppr)


ft.app(target=main)
