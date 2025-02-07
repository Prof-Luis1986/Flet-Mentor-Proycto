import flet as ft
import random

def main(page: ft.Page):
    page.title = "Juego de Matemáticas 🧮"
    page.window_width = 400
    page.window_height = 500
    page.bgcolor = "#D6EAF8"  # Fondo azul claro
    page.window_resizable = False  # Fijar el tamaño de la ventana

    # Puntuación global
    score_value = 0
    score = ft.Text(f"Puntuación: {score_value}", size=18, color=ft.colors.BLUE)

    # Elementos de la pantalla de operaciones
    num1 = ft.Text(random.randint(10, 200), size=24, weight=ft.FontWeight.BOLD)
    num2 = ft.Text(random.randint(10, 200), size=24, weight=ft.FontWeight.BOLD)
    resultado_input = ft.TextField(hint_text="Ejemplo: 42", width=200, text_align=ft.TextAlign.CENTER)
    operacion_actual = ft.Text("+", size=30, weight=ft.FontWeight.BOLD)

    # Audio para efectos de sonido
    audio_correcto = ft.Audio(src="/collect.mp3", autoplay=False)
    audio_siguiente = ft.Audio(src="/coin.mp3", autoplay=False)
    audio_error = ft.Audio(src="/error.mp3", autoplay=False)

    page.add(audio_correcto, audio_siguiente, audio_error)

    # Función para generar nuevos números
    def nueva_pregunta():
        num1.value = random.randint(10, 200)
        num2.value = random.randint(10, 200)

        if operacion_actual.value == "÷":
            while num2.value == 0:  # Evitar división por cero
                num2.value = random.randint(10, 200)

        resultado_input.value = ""
        audio_siguiente.play()
        page.update()

    # Función para cambiar operación
    def cambiar_operacion(op):
        operacion_actual.value = op
        nueva_pregunta()
        page.update()

    # Función para verificar respuesta
    def verificar_respuesta(e):
        nonlocal score_value

        if resultado_input.value.replace(".", "").isdigit():
            respuesta_usuario = float(resultado_input.value)
            n1, n2 = int(num1.value), int(num2.value)

            # Determinar la respuesta correcta según la operación
            if operacion_actual.value == "+":
                respuesta_correcta = n1 + n2
            elif operacion_actual.value == "-":
                respuesta_correcta = n1 - n2
            elif operacion_actual.value == "×":
                respuesta_correcta = n1 * n2
            elif operacion_actual.value == "÷":
                respuesta_correcta = round(n1 / n2, 2)  # Resultado con 2 decimales

            # Actualizar la puntuación
            if respuesta_usuario == respuesta_correcta:
                score_value += 1
                audio_correcto.play()
            else:
                score_value = max(0, score_value - 1)  # Evita puntuaciones negativas
                audio_error.play()

            score.value = f"Puntuación: {score_value}"
        else:
            score.value = "⚠️ Ingresa un número válido"

        page.update()

    # Botones de operaciones
    btn_suma = ft.ElevatedButton("➕", on_click=lambda e: cambiar_operacion("+"), bgcolor="#2ECC71")
    btn_resta = ft.ElevatedButton("➖", on_click=lambda e: cambiar_operacion("-"), bgcolor="#F39C12")
    btn_multi = ft.ElevatedButton("✖", on_click=lambda e: cambiar_operacion("×"), bgcolor="#E74C3C")
    btn_div = ft.ElevatedButton("➗", on_click=lambda e: cambiar_operacion("÷"), bgcolor="#3498DB")

    # Botones de acciones
    btn_verificar = ft.ElevatedButton("✅ Verificar", on_click=verificar_respuesta, bgcolor="#8E44AD")
    btn_siguiente = ft.ElevatedButton("➡️ Siguiente", on_click=lambda e: nueva_pregunta(), bgcolor="#16A085")

    # Layout principal
    page.add(
        ft.Column(
            [
                ft.Text("Juego de Matemáticas 🏆", size=26, weight=ft.FontWeight.BOLD, color="black"),
                
                # Botones de operaciones
                ft.Row([btn_suma, btn_resta, btn_multi, btn_div], alignment=ft.MainAxisAlignment.CENTER),

                # Contenedor de la pregunta
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Operación:", size=22, weight=ft.FontWeight.BOLD, color="black"),
                            operacion_actual,
                            ft.Row([num1, ft.Text(" "), operacion_actual, ft.Text(" "), num2], alignment=ft.MainAxisAlignment.CENTER),
                            resultado_input,
                            btn_verificar,
                            score,
                            btn_siguiente,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                    bgcolor="white",
                    border_radius=15,
                    shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.colors.GREY),
                    alignment=ft.alignment.center
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
