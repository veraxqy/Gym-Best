from flet import *

class Exercicios(UserControl):
    def __init__(self, nome, carga, repeticao, status_exercicio, delete_exercicio, show_checkbox):
        super().__init__()
        self.completed = False
        self.nome = nome
        self.carga = carga
        self.repeticao = repeticao
        self.status_exercicio = status_exercicio
        self.delete_exercicio = delete_exercicio
        self.show_checkbox = show_checkbox

def main(page: Page):
    page.title = "Gym-Best"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"

    page.add()

app(target=main)