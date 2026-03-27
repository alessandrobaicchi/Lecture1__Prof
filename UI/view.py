import flet as ft

class View:
    # Classe che rappresenta l'interfaccia grafica dell'applicazione.

    def __init__(self, page):
        # Salvo la pagina Flet
        self._page = page

        # Controller verrà impostato successivamente
        self._controller = None

        # Impostazioni grafiche iniziali
        self._page.title = "TdP 2025 - Software Gestionale"
        self._page.horizontal_alignment = "CENTER"
        self._page.theme_mode = ft.ThemeMode.LIGHT

        # Aggiorno la pagina
        self.update_page()

    def carica_interfaccia(self):
        # Metodo che costruisce tutti gli oggetti grafici dell'interfaccia.

        # --- PRODOTTO ---
        self._txtInNomeP = ft.TextField(label="Nome prodotto", width=200)
        self._txtInPrezzo = ft.TextField(label="Prezzo", width=200)
        self._txtInQuantita = ft.TextField(label="Quantità", width=200)

        row1 = ft.Row(
            controls=[self._txtInNomeP, self._txtInPrezzo, self._txtInQuantita],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # --- CLIENTE ---
        self._txtInNomeC = ft.TextField(label="Nome cliente", width=200)
        self._txtInMail = ft.TextField(label="Email cliente", width=200)
        self._txtInCategoria = ft.TextField(label="Categoria cliente", width=200)

        row2 = ft.Row(
            controls=[self._txtInNomeC, self._txtInMail, self._txtInCategoria],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # --- PULSANTI ---
        self._btnAdd = ft.ElevatedButton(
            text="Aggiungi ordine",
            on_click=self._controller.add_ordine,
            width=200
        )

        self._btnGestisciOrdine = ft.ElevatedButton(
            text="Gestisci prossimo ordine",
            on_click=self._controller.gestisci_ordine,
            width=200
        )

        self._btnGestisciAllOrdini = ft.ElevatedButton(
            text="Gestisci tutti gli ordini",
            on_click=self._controller.gestisci_all_ordini,
            width=200
        )

        self._btnStampaInfo = ft.ElevatedButton(
            text="Stampa sommario",
            on_click=self._controller.stampa_sommario,
            width=200
        )

        row3 = ft.Row(
            controls=[self._btnAdd, self._btnGestisciOrdine, self._btnGestisciAllOrdini, self._btnStampaInfo],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # --- LIST VIEW DI OUTPUT ---
        self._lvOut = ft.ListView(expand=True)

        # Aggiungo tutto alla pagina
        self._page.add(row1, row2, row3, self._lvOut)

    def set_controller(self, c):
        # Collega la View al Controller
        self._controller = c

    def update_page(self):
        # Aggiorna la pagina Flet
        self._page.update()