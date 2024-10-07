from flet import *
import sqlite3

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
    
    def build(self):
        self.check_exercicio = Checkbox(
            value = False, label = self.nome, on_change = self.status_changed, visible=self.show_checkbox
        )

        self.edit_nome = TextField(expand=1)
        self.edit_carga = TextField(expand=1)
        self.edit_repeticao = TextField(expand=1)
        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.check_exercicio if self.show_checkbox else Text(value=self.nome),
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Editar Exercício",
                            on_click=self.edit_exercicio,
                            icon_color=colors.WHITE,
                        ),
                        IconButton(
                            icon=icons.DELETE_OUTLINED,
                            tooltip="Deletar Exercício",
                            on_click=self.delet_exercicio,
                            icon_color=colors.WHITE,
                        )
                    ]
                )
            ]
        )
        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_nome,
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.WHITE,
                    tooltip="Atualizar Exercício",
                    on_click=self.save_exercicio,
                )
            ]
        )
        return super().build()
    
class GymBest(UserControl):
    def build(self):
        self.home_view = Column(
            controls=[
                Row([Text(value="Página Inicial", style="headlineMedium")], alignment="center"),
            ]
        )
        return self.home_view

def main(page: Page):
    page.title = "Gym-Best"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"

    app = GymBest()
    page.add(app)

app(target=main)