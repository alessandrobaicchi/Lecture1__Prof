import flet as ft
from gestionale.gestoreOrdini import GestoreOrdini

class Controller:
    # Classe che gestisce la logica applicativa dell'interfaccia grafica.
    # Riceve la View e crea il Model (GestoreOrdini).

    def __init__(self, v):
        # Salvo la View per poter leggere i campi e aggiornare l'interfaccia
        self._view = v

        # Creo il modello: contiene la logica di gestione degli ordini
        self._model = GestoreOrdini()

    def add_ordine(self, e):
        # Metodo chiamato quando l'utente clicca "Aggiungi ordine".
        # Legge i campi della View, valida i dati, crea un ordine e lo aggiunge al modello.


        # --- PRODOTTO ---

        nomePstr = self._view._txtInNomeP.value
        # Validazione nome prodotto
        if nomePstr == "":
            self._view._lvOut.controls.append(ft.Text("Attenzione, il campo Nome prodotto non può essere vuoto!",
                                                      color="red"))
            self._view.update_page()        # Devo sempre aggiornare la pagina!
            return

        # Validazione prezzo
        try:
            prezzo = float(self._view._txtInPrezzo.value)
        except ValueError:
            self._view._lvOut.controls.append(
                ft.Text("Attenzione! Il prezzo deve essere un numero!", color="red")
            )
            self._view.update_page()
            return

        # Validazione quantità
        try:
            quantita = int(self._view._txtInQuantita.value)
        except ValueError:
            self._view._lvOut.controls.append(
                ft.Text("Attenzione! La quantità deve essere un numero!", color="red")
            )
            self._view.update_page()
            return


        # --- CLIENTE ---
        nomeC = self._view._txtInNomeC.value
        # Validazione nome cliente
        if nomeC == "":
            self._view._lvOut.controls.append(ft.Text("Attenzione, il campo Nome cliente non può essere vuoto!",
                                                      color="red"))
            self._view.update_page()  # Devo sempre aggiornare la pagina!
            return

        email = self._view._txtInMail.value
        # Validazione email cliente
        if email == "":
            self._view._lvOut.controls.append(ft.Text("Attenzione, il campo Email cliente non può essere vuoto!",
                                                      color="red"))
            self._view.update_page()  # Devo sempre aggiornare la pagina!
            return

        categoria = self._view._txtInCategoria.value
        # Validazione categoria cliente
        if categoria == "":
            self._view._lvOut.controls.append(ft.Text("Attenzione, il campo Categoria cliente non può essere vuoto!",
                                                      color="red"))
            self._view.update_page()  # Devo sempre aggiornare la pagina!
            return

        # Creo l'ordine tramite il modello
        ordine = self._model.crea_ordine(nomePstr, prezzo, quantita, nomeC, email, categoria)

        # Aggiungo l'ordine alla coda FIFO
        self._model.add_ordine(ordine)

        # Pulizia dei campi della View
        self._view._txtInNomeP.value = ""
        self._view._txtInPrezzo.value = ""
        self._view._txtInQuantita.value = ""
        self._view._txtInNomeC.value = ""
        self._view._txtInMail.value = ""
        self._view._txtInCategoria.value = ""

        # Messaggi di conferma
        self._view._lvOut.controls.append(ft.Text("Ordine correttamente inserito", color="green"))
        self._view._lvOut.controls.append(ft.Text("Dettagli dell'ordine:"))
        self._view._lvOut.controls.append(ft.Text(ordine.riepilogo()))
        self._view._lvOut.controls.append(ft.Text("\n"))

        # Aggiorno la pagina
        self._view.update_page()


    def gestisci_ordine(self, e):
        # Processa il prossimo ordine nella coda FIFO
        self._view._lvOut.controls.clear() # Ripulisco l'interfaccia grafica
        # Chiamo il metodo corrispondente, e poi grazie al suo return dico quale ordine ha gestito
        res, ordine = self._model.processa_prossimo_ordine()
        if res:
            self._view._lvOut.controls.append(ft.Text("Ordine processato correttamente", color="green"))
            # Stampo l'ordine processato
            self._view._lvOut.controls.append(ft.Text(ordine.riepilogo()))
            self._view.update_page()
        else:
            self._view._lvOut.controls.append(ft.Text("Non ci sono ordini in coda!", color="blue"))
            self._view.update_page()


    def gestisci_all_ordini(self, e):
        self._view._lvOut.controls.clear()
        ordini = self._model.processa_tutti_ordini()
        # La lista ordini può essere anche vuota, quindi, faccio un controllo con un if.
        if not ordini:
            self._view._lvOut.controls.append(ft.Text("Non ci sono ordini in coda!", color="blue"))
            self._view.update_page()
        else:
            self._view._lvOut.controls.append(ft.Text("\n"))
            self._view._lvOut.controls.append(ft.Text(f"Ho processato correttamente {len(ordini)} ordini!",
                                                      color="green"))
            # Stampo il riepilogo di ordine
            for o in ordini:
                self._view._lvOut.controls.append(ft.Text("\n"))
                self._view._lvOut.controls.append(ft.Text(o.riepilogo()))
            self._view.update_page()


    def stampa_sommario(self, e):
        self._view._lvOut.controls.clear()
        self._view._lvOut.controls.append(ft.Text("Di seguito il sommario dello stato del business",
                                                  color="orange"))
        self._view._lvOut.controls.append(ft.Text(self._model.get_riepilogo()))
        self._view.update_page()