import flet as ft
import random

# Palabras posibles
PALABRAS = ["CASA", "PERRO", "GATO", "FLOR", "FLET", "PYTHON", "INSECTO"]

# Variables globales
puntaje = 0
palabra_actual = ""
letras_presionadas = ""

def lluvia_de_letras(page: ft.Page):
    global puntaje, palabra_actual, letras_presionadas

    page.clean()
    page.title = "Lluvia de Letras ☔"
    page.bgcolor = "#0A192F"

    palabra_actual = random.choice(PALABRAS)
    letras_presionadas = ""

    # Audio
    audio_tecla = ft.Audio(src="/collect.mp3", autoplay=False)
    audio_punto = ft.Audio(src="/coin.mp3", autoplay=False)
    audio_error = ft.Audio(src="/error.mp3", autoplay=False)
    page.add(audio_tecla, audio_punto, audio_error)

    score_text = ft.Text(f"Puntaje: {puntaje} ⭐", size=32, color=ft.colors.YELLOW, weight=ft.FontWeight.BOLD)
    palabra_texto = ft.Text(f"Forma esta palabra: {palabra_actual}", size=36, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN)
    letras_texto = ft.Text("", size=36, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_ACCENT)

    botones = []
    letras_desordenadas = list(palabra_actual)
    random.shuffle(letras_desordenadas)

    def presionar_letra(e):
        global puntaje, letras_presionadas
        letra = e.control.text
        audio_tecla.play()

        if len(letras_presionadas) < len(palabra_actual) and letra == palabra_actual[len(letras_presionadas)]:
            letras_presionadas += letra
            letras_texto.value = letras_presionadas

            if letras_presionadas == palabra_actual:
                puntaje += 1
                score_text.value = f"Puntaje: {puntaje} ⭐"
                audio_punto.play()
                page.update()
                lluvia_de_letras(page)
        else:
            puntaje -= 1
            score_text.value = f"Puntaje: {puntaje} ⭐"
            audio_error.play()
        page.update()

    for letra in letras_desordenadas:
        boton = ft.ElevatedButton(text=letra, on_click=presionar_letra, bgcolor=ft.colors.BLUE_GREY_700, color=ft.colors.WHITE, height=70, width=70)
        botones.append(boton)

    def volver_menu(e):
        main(page)

    page.add(
        ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column([
                        palabra_texto,
                        score_text,
                        letras_texto,
                        ft.Row(controls=botones, alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        ft.ElevatedButton("⬅ Volver al Menú", on_click=volver_menu, bgcolor=ft.colors.RED_ACCENT, color=ft.colors.WHITE, height=60, width=200)
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
                    padding=50,
                    border_radius=20,
                    bgcolor="#112D4E",
                    shadow=ft.BoxShadow(blur_radius=12, spread_radius=4),
                    width=1200
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

def main(page: ft.Page):
    page.clean()
    page.title = "Flet Mentor"
    page.bgcolor = "#0A192F"

    def abrir_lluvia(e):
        lluvia_de_letras(page)

    gradient_container = ft.Container(
        content=ft.Column([
            ft.Text("Flet Mentor", size=42, weight=ft.FontWeight.BOLD, color=ft.colors.YELLOW, text_align=ft.TextAlign.CENTER),
            ft.Image(src="/Mentor.jpg", width=200, height=150, fit=ft.ImageFit.CONTAIN),
            ft.Text("Selecciona un juego", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN),
            ft.ElevatedButton("🔡 Lluvia de Letras", on_click=abrir_lluvia, bgcolor=ft.colors.BLUE_ACCENT, color=ft.colors.WHITE, height=60, width=250)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
        padding=163,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=20, spread_radius=6),
        alignment=ft.alignment.center,
        gradient=ft.LinearGradient(colors=["#112D4E", "#3F72AF"], begin=ft.alignment.top_center, end=ft.alignment.bottom_center)
    )

    page.add(
        ft.Column(
            controls=[gradient_container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
