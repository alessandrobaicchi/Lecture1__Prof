import flet as ft


# questa riga importa la libreria Flet e le assegna il nome abbreviato ft

class View:
    # questa riga definisce la classe View, che rappresenta l'interfaccia grafica dell'applicazione

    def __init__(self, page):
        # questa riga è il costruttore della View e riceve la pagina Flet su cui disegnare
        self._page = page
        # questa riga salva la pagina in un attributo privato, così possiamo usarla in altri metodi

        self._controller = None
        # questa riga inizializza il riferimento al Controller a None; verrà impostato dopo con set_controller

        self._page.title = "TdP 2025 - Software Gestionale"
        # questa riga imposta il titolo della finestra dell'applicazione

        self._page.horizontal_alignment = "CENTER"
        # questa riga centra orizzontalmente i contenuti nella pagina

        self._page.theme_mode = ft.ThemeMode.LIGHT
        # questa riga imposta il tema grafico della pagina in modalità chiara (light)

        self.update_page()
        # questa riga aggiorna la pagina per applicare subito le modifiche al titolo, allineamento e tema


    def carica_interfaccia(self):

        # Prodotto
        self._txtInNomeP = ft.TextField(label="Nome prodotto", width=200)
        self._txtInPrezzo = ft.TextField(label="Prezzo", width=200)
        self._txtInQuantita = ft.TextField(label="Quantità", width=200)
        row1 = ft.Row(controls=[self._txtInNomeP,self._txtInPrezzo,self._txtInQuantita],
                      alignment=ft.MainAxisAlignment.CENTER)

        # Cliente
        self._txtInNomeC = ft.TextField(label="Nome cliente", width=200)
        self._txtInMail = ft.TextField(label="Email cliente", width=200)
        self._txtInCategoria = ft.TextField(label="Categoria cliente", width=200)
        row2 = ft.Row(controls=[self._txtInNomeC, self._txtInMail, self._txtInCategoria],
                      alignment=ft.MainAxisAlignment.CENTER)

        #Buttons
        self._btnAdd = ft.ElevatedButton(text="Aggiungi ordine",
                                         on_click=self._controller.add_ordine,width=200)
        self._btnGestisciOrdine = ft.ElevatedButton(text="Gestisci prossimo ordine",
                                                    on_click=self._controller.gestisci_ordine, width=200)
        self._btnGestisciAllOrdini = ft.ElevatedButton(text="Gestisci tutti gli ordini",
                                                       on_click=self._controller.gestisci_all_ordini, width=200)
        self._btnStampaInfo = ft.ElevatedButton(text="Stampa sommario",
                                                on_click=self._controller.stampa_sommario, width=200)
        row3 = ft.Row(controls=[self._btnAdd, self._btnGestisciOrdine, self._btnGestisciAllOrdini,
                                self._btnStampaInfo],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._lvOut = ft.ListView(expand=True)

        self._page.add(row1,row2,row3,self._lvOut)





    def set_controller(self, c):
        # questo metodo collega la View al suo Controller
        self._controller = c
        # questa riga salva il Controller in un attributo privato, così la View può chiamare i suoi metodi



    def update_page(self):
        # questo metodo aggiorna la pagina Flet dopo modifiche all'interfaccia grafica
        self._page.update()
        # questa riga dice a Flet di ridisegnare la pagina con lo stato corrente dei controlli