"""
Scrivere un software gestionale che abbia le seguenti funzionalità:
1)  Supportare l'arrivo e la gestione degli ordini.
1b) Quando arriva un nuovo ordine lo aggiunga ad una coda, assicurando che sia eseguito solo dopo gli altri.
2)  Avere delle funzionalità per avere statistiche sugli ordini.
3)  Fornire statistiche sulla distribuzione di ordini per categoria di cliente.
"""

from collections import deque, Counter, defaultdict
from gestionale.vendite.ordini import Ordine

class GestoreOrdini:

    def __init__(self):
        # deque è la struttura ideale per una coda FIFO: append() + popleft()
        # garantiscono O(1) e modellano perfettamente l’arrivo degli ordini.
        self._ordini_da_processare = deque()

        # Lista semplice per gli ordini già gestiti: non serve mantenere ordine
        # o accesso rapido, quindi list è la scelta corretta.
        self._ordini_processati = []

        # Counter è perfetto per contare prodotti venduti: supporta most_common()
        # che useremo per ottenere i top N prodotti.
        self._statistiche_prodotti = Counter()

        # defaultdict(list) permette di raggruppare ordini per categoria cliente
        # senza dover controllare se la chiave esiste.
        self._ordini_per_categoria = defaultdict(list)



    def add_ordine(self, ordine: Ordine):
        """Aggiunge un nuovo ordine agli elementi da gestire"""
        # Metodo semplice e corretto: aggiunge l’ordine in coda e informa l’utente.
        # L’uso di append() su deque mantiene la logica FIFO.
        self._ordini_da_processare.append(ordine)
        print(f"Ricevuto un nuovo ordine da parte di {ordine.cliente}.")
        print(f"Ordini ancora da evadere: {len(self._ordini_da_processare)}")


    def processa_prossimo_ordine(self):
        """Questo metodo legge il prossimo ordine in coda e lo gestisce"""
        # Metodo centrale del gestionale: implementa la logica FIFO,
        # aggiorna tutte le statistiche e archivia l’ordine processato.

        # Assicuriamoci che ci sia un ordine da processare
        # Controllo corretto: se la coda è vuota, si evita un errore e si
        # restituisce False per segnalare che non è stato processato nulla.
        if not self._ordini_da_processare:
            print("Non ci sono ordini in coda.")
            return False

        # Se esiste un ordine da processare, gestiamo il primo in coda
        ordine = self._ordini_da_processare.popleft()
        # popleft() è la scelta perfetta: rispetta la logica FIFO e ha costo O(1).
        print(f"Sto processando l'ordine di {ordine.cliente}")
        print(ordine.riepilogo())
        # Ottima scelta: riepilogo() restituisce una stringa già formattata,
        # quindi il metodo non si occupa della formattazione ma solo della logica.


        # Aggiornare statistiche dei prodotti venduti
        for riga in ordine.righe:
            # Aggiornamento statistiche prodotti: Counter gestisce automaticamente
            # l’incremento e permette analisi successive (top N, ordinamenti, ecc.).
            # L’uso di riga.prodotto.name è corretto perché ProdottoRecord è hashable.
            self._statistiche_prodotti[riga.prodotto.name] += riga.quantita

        # Raggruppamento per categoria: defaultdict(list) evita controlli superflui.
        # Questo permette di calcolare statistiche aggregate per categoria cliente.
        self._ordini_per_categoria[ordine.cliente.categoria].append(ordine)

        # Archiviamo l'ordine
        self._ordini_processati.append(ordine)

        print("Ordine processato correttamente!")

        return True
        # Restituzione booleana corretta: permette a chi chiama di sapere
        # se un ordine è stato effettivamente processato.



    def processa_tutti_ordini(self):
        """Processa tutti gli ordini presenti in coda"""
        # Metodo che delega completamente a processa_prossimo_ordine().
        # Design corretto: evita duplicazione di logica e mantiene il codice DRY.
        # Il while sulla deque è sicuro perché popleft() la svuota progressivamente.

        print(f"Processando {len(self._ordini_da_processare)} ordini!")
        while self._ordini_da_processare:
            self.processa_prossimo_ordine()
        print("Tutti gli ordini sono stati processati!")



    def get_statistiche_prodotti(self, top_n: int = 5):
        """Questo metodo restituisce informazioni sui prodotti più venduti"""
        # Metodo che incapsula l’accesso al Counter.
        # Restituire una lista di tuple è una scelta ottima: evita di esporre
        # direttamente la struttura interna e permette flessibilità di stampa.
        # Parametro top_n ben progettato: rende il metodo riutilizzabile.
        valori = []
        for prodotto, quantita in self._statistiche_prodotti.most_common(top_n):
            valori.append((prodotto, quantita))
        return valori



    def get_distribuzione_categorie(self):
        """Questo metodo restituisce info su totale fatturato per ogni categoria presente"""
        # Metodo che calcola il fatturato totale per categoria cliente.
        # L’uso di totale_lordo(0.22) è coerente con la logica del gestionale.
        # La lista di tuple (categoria, fatturato) è un formato semplice e chiaro.
        # Suggerimento: totale_Fatturato dovrebbe essere snake_case (totale_fatturato).
        valori = []
        for cat in self._ordini_per_categoria.keys():
            ordini = self._ordini_per_categoria[cat]
            totale_Fatturato = sum([o.totale_lordo(0.22) for o in ordini])
            valori.append((cat, totale_Fatturato))
        return valori




    def stampa_riepilogo(self):
        """Stampa info di massima"""
        # Metodo di sola stampa: aggrega e presenta le informazioni.
        # È corretto che non faccia calcoli ma si limiti a usare i metodi get_*.
        # Questo rispetta il principio di incapsulamento e separazione delle responsabilità.
        # Output leggibile.
        print("\n" + "=" * 60)
        print("Stato attuale del business:")
        print(f"Ordini correttamente gestiti: {len(self._ordini_processati)}")
        print(f"Ordini in coda: {len(self._ordini_da_processare)}")

        print("Prodotti più venduti:")
        for prod, quantità in self.get_statistiche_prodotti():
            print(f"{prod}: {quantità}")

        print("Fatturato per categoria:")
        for cat, fatturato in self.get_distribuzione_categorie():
            print(f"{cat} : {fatturato}")