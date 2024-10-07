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
    
    def edit_exercicio(self):
        self.edit_nome.value = self.check_exercicio.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_exercicio(self):
        self.check_exercicio.label = self.edit_nome.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()
    
    def delet_exercicio(self):
        self.delete_exercicio(self)

    def status_changed(self):
        self.completed = self.check_exercicio.value
        self.status_changed(self)

class GymBest(UserControl):
    def build(self):
        self.home_view = Container(
            Column(
                controls=[
                    Row(
                        controls=[
                            Text(value="Página Inicial", style="headlineMedium"),
                        ],
                        alignment=MainAxisAlignment.CENTER
                    ),
                    Row(
                        controls=[
                            ElevatedButton("Exercícios", on_click= lambda e: self.page.go("/exercicios")),
                        ],
                        alignment=MainAxisAlignment.CENTER
                    ),
                ]
            ),
        )

        self.exercicios_view = Container(
            Column(
                controls=[
                    Row(
                        controls=[
                            IconButton(
                                icon=icons.ARROW_BACK,
                                on_click=lambda e: self.page.go("/"),
                                icon_color = colors.WHITE,
                            ),
                            Text(value="Exercícios", style="headlineMedium"),
                        ],
                        alignment=MainAxisAlignment.CENTER
                    ),
                ]
            )
        )

        self.stack = Stack(
            controls=[
                self.home_view,
                self.exercicios_view,
            ],
            expand=True,
        )

        return self.stack
    
    def route_change(self, route):
        if route.route == "/":
            self.stack.controls[0].visible = True
            self.stack.controls[1].visible = False
        elif route.route == "/exercicios":
            self.stack.controls[0].visible = False
            self.stack.controls[1].visible = True
        self.update()

    def view_pop(self, view):
        self.page.go("/")

def main(page: Page):
    page.title = "Gym-Best"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"

    app = GymBest()
    page.add(app)

    page.on_route_change = app.route_change
    page.on_view_pop = app.view_pop
    page.go("/")

app(target=main)