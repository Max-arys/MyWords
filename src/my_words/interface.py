import flet as ft


class Words_chose(ft.Row):
    color_of_selected = ft.colors.AMBER_500
    color_of_not_selected = ft.colors.AMBER_100

    def __init__(self, words, page):
        self.words = words
        self.page = page
        super().__init__()
        self.wrap = True
        self.scroll = "always"
        self.expand = True
        self.click = self.container_click

    def container_click(self, e: ft.ContainerTapEvent):
        word = e.control.content.value

        if e.control.bgcolor == self.color_of_not_selected:
            e.control.bgcolor = self.color_of_selected
            self.words.new_words.remove(word)
            self.words.my_words.add(word)
        else:
            e.control.bgcolor = self.color_of_not_selected
            self.words.my_words.remove(word)
            self.words.new_words.add(word)
        self.page.update()

    def container_words(self):
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


if __name__ == '__main__':
    ...
