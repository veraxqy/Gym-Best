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

class CreateExercicio(UserControl):
    def build(self):
        self.exercicio_nome = TextField(hint_text="Nome do Exercício")
        self.exercicio_carga = TextField(hint_text="Carga do Exercício")
        self.exercicio_repeticao = TextField(hint_text="Repetições do Exercício")

        self.exercicio_button = ElevatedButton(
            text="Adicionar Exercício", icon=icons.ADD, on_click=self.add_exercicio
        )

        self.total_exercicios = Text(value="0 Exercício(s) Adicionado(s)")
        self.exercicios_container = Column()

        self.exercicio_pagina = Container(
            Column(
                controls=[
                    Row(
                        controls=[
                            self.total_exercicios,
                        ],
                        alignment=MainAxisAlignment.CENTER
                    ),
                    Row(
                        controls=[
                            Column(
                                controls=[
                                    self.exercicio_nome,
                                    self.exercicio_carga,
                                    self.exercicio_repeticao,
                                    self.exercicio_button,
                                ],
                                spacing=10,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER
                    ),
                ]
            ),
        )
        
        Column(
            width=400,
            controls=[
                
                
                Column(
                    spacing=20,
                    controls=[
                        self.exercicios_container,
                    ]
                )
            ]
        )

        return self.exercicio_pagina

    def add_exercicio(self, e):
        nome = self.exercicio_nome.value
        carga = self.exercicio_carga.value
        repeticao = self.exercicio_repeticao.value

        if nome and carga and repeticao:
            exercicio = Exercicios(
                nome, carga, repeticao, self.status_exercicio,
                self.delete_exercico, show_checkbox=False
            )
            self.exercicios_container.controls.append(exercicio)
            self.exercicio_nome.value = ""
            self.exercicio_carga.value = ""
            self.exercicio_repeticao.value = ""
            self.exercicio_nome.focus()
            self.update_total_exercicios()

    def status_exercicio(self):
        self.update()

    def delete_exercicio(self, exercicio):
        self.exercicios_container.controls.remove(exercicio)
        self.update_total_exercicios()

    def update_total_exercicios(self):
        total = len(self.exercicios_container.controls)
        self.total_exercicios.value = f"{total} Exercício(s) Cadastro(s)"
        self.update()

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
                        ]
                    ),
                    Row(
                        controls=[
                            Text(value="Exercícios", style="headlineMedium"),
                        ],
                        alignment=MainAxisAlignment.CENTER
                    ),
                    CreateExercicio()
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