import flet as ft
# questa riga importa la libreria Flet e le assegna il nome abbreviato ft

from gestionale.view import View
# questa riga importa la classe View dal modulo view del package gestionale

from gestionale.controller import Controller
# questa riga importa la classe Controller dal modulo controller del package gestionale

def main(page: ft.Page):
    # questa riga definisce la funzione main, punto di ingresso dell'app Flet
    # il parametro page è l'oggetto pagina su cui disegneremo l'interfaccia grafica

    v = View(page)
    # questa riga crea un oggetto View e gli passa la pagina Flet su cui deve disegnare

    c = Controller(v)
    # questa riga crea un oggetto Controller e gli passa la View, così il Controller può interagire con la View

    v.set_controller(c)
    # questa riga dice alla View qual è il suo Controller, collegando i due oggetti

    v.carica_interfaccia()
    # questa riga chiama il metodo della View che costruisce e carica tutta l'interfaccia grafica

ft.app(target = main)
# questa riga avvia l'applicazione Flet usando la funzione main come funzione principale