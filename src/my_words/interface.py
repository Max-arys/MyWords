import flet as ft

a = [
  "that",
  "have",
  "vikendi",
  "then",
  "surprise",
  "can"
]
b = []


def main(page: ft.Page):
    color_of_selected = ft.colors.AMBER_500
    color_of_not_selected = ft.colors.AMBER_100
    page.title = "GridView Example"
    r = ft.Row(wrap=True, scroll="always", expand=True)
    page.add(r)

    def container_click(e: ft.ContainerTapEvent):
        word = e.control.content.value
        if e.control.bgcolor == color_of_not_selected:
            e.control.bgcolor = color_of_selected
            a.remove(word)
            b.append(word)
        else:
            e.control.bgcolor = color_of_not_selected
            b.remove(word)
            a.append(word)
        print(a, b)
        page.update()

    for i in a:
        r.controls.append(
            ft.Container(
                ft.Text(i),
                width=100,
                height=50,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.AMBER_100,
                border=ft.border.all(1, ft.colors.AMBER_400),
                border_radius=ft.border_radius.all(5),
                on_click=container_click,
            )
        )
    page.update()


if __name__ == '__main__':
    ft.app(target=main)
