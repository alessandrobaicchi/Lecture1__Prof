import flet as ft

from gestionale.gestoreOrdini import GestoreOrdini


class Controller:
    # questa riga definisce la classe Controller, che gestisce la logica tra View e Model

    def __init__(self, v):
        # questa riga è il costruttore del Controller e riceve un oggetto View come parametro
        self._view = v
        # questa riga salva la View in un attributo privato, così il Controller può usarla in altri metodi
        self._model = GestoreOrdini()


    def add_ordine(self, e):
        # Prodotto
        nomePstr = self._view._txtInNomeP.value
        try:
            prezzo = float(self._view._txtInPrezzo.value)
        except ValueError:
            self._view._lvOut.controls.append(ft.Text("Attenzione! Il prezzo deve essere un numero!",
                                                      color="red"))
            self._view.update_page()
            return

        try:
            quantita = int(self._view._txtInQuantita.value)
        except ValueError:
            self._view._lvOut.controls.append(ft.Text("Attenzione! La quantità deve essere un numero!",
                                                      color="red"))
            self._view.update_page()
            return

        # Cliente
        nomeC = self._view._txtInNomeC.value
        email = self._view._txtInMail.value
        categoria = self._view._txtInCategoria.value

        ordine = self._model.crea_ordine(nomePstr,prezzo,quantita,nomeC,email,categoria)
        self._model.add_ordine(ordine)

        self._view._txtInNomeP.value = ""
        self._view._txtInPrezzo.value = ""
        self._view._txtInQuantita.value = ""
        self._view._txtInNomeC.value = ""
        self._view._txtInMail.value = ""
        self._view._txtInCategoria.value = ""

        self._view._lvOut.controls.append(ft.Text("Ordine correttamente inserito", color="green"))
        self._view._lvOut.controls.append(ft.Text("Dettagli dell'ordine:"))
        self._view._lvOut.controls.append(ft.Text(ordine.riepilogo()))

        self._view.update_page()


    def gestisci_ordine(self, e):
        pass


    def gestisci_all_ordini(self, e):
        pass


    def stampa_sommario(self, e):
        pass