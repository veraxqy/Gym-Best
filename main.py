from flet import *

def main(page: Page):
    page.title = "Gym-Best"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"

    page.add()

app(target=main)