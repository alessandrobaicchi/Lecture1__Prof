"""
Scrivere un software gestionale che abbia le seguenti funzionalità:
1)  Supportare l'arrivo e la gestione degli ordini.
1b) Quando arriva un nuovo ordine lo aggiunga ad una coda, assicurando che sia eseguito solo dopo gli altri.
2)  Avere delle funzionalità per avere statistiche sugli ordini.
3)  Fornire statistiche sulla distribuzione di ordini per categoria di cliente.
"""

from collections import deque, Counter, defaultdict

from gestionale.core.clienti import ClienteRecord
from gestionale.core.prodotti import ProdottoRecord
from gestionale.vendite.ordini import Ordine, RigaOrdine


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
        # defaultdict(list) è un dizionario speciale che funziona così:
        #   --> se si accede ad una chiave che non esiste, inveve di dare errore crea
        #       automaticamente un valore di default, in questo caso una lista vuota!
        self._ordini_per_categoria = defaultdict(list)



    def add_ordine(self, ordine: Ordine):
        """Aggiunge un nuovo ordine agli elementi da gestire"""
        # Metodo semplice e corretto: aggiunge l’ordine in coda e informa l’utente.
        # L’uso di append() su deque mantiene la logica FIFO.
        self._ordini_da_processare.append(ordine)
        print(f"Ricevuto un nuovo ordine da parte di {ordine.cliente}.")
        print(f"Ordini ancora da evadere: {len(self._ordini_da_processare)}")


    def crea_ordine(self, nomeP, prezzoP, quantitaP, nomeC, emailC, categoriaC):
        return Ordine([RigaOrdine(ProdottoRecord(nomeP,prezzoP),quantitaP)],
                      ClienteRecord(nomeC,emailC,categoriaC))


    def processa_prossimo_ordine(self):
        """
            Processa il prossimo ordine nella coda FIFO (_ordini_da_processare).
            Questo metodo:
            - estrae il primo ordine dalla deque (FIFO)
            - stampa il riepilogo dell’ordine
            - aggiorna le statistiche dei prodotti venduti (Counter)
            - inserisce l’ordine nella categoria corretta (defaultdict(list))
            - archivia l’ordine tra quelli processati
            - restituisce True se un ordine è stato processato, False se la coda è vuota
            """
        print("\n" + "-" * 60)
        print("\n" + "=" * 60)
        # Se la coda è vuota, non c’è nulla da processare.
        # Restituisce False per segnalare che non è stato fatto alcun lavoro. Per avere una return consistente
        # con la return True, ritorno un ordine vuoto
        if not self._ordini_da_processare:
            print("Non ci sono ordini in coda.")
            return False, Ordine([],ClienteRecord("","",""))

        # Estrae il primo ordine dalla coda FIFO.
        # popleft() è O(1) e rispetta la logica di arrivo degli ordini.
        ordine = self._ordini_da_processare.popleft()

        # Stampa il riepilogo dell’ordine.
        # Il metodo riepilogo() appartiene alla classe Ordine e mostra:
        # - cliente
        # - righe ordine
        # - totale netto e totale lordo
        print(f"Sto processando l'ordine di {ordine.cliente}")
        print(ordine.riepilogo())

        # Aggiorna le statistiche dei prodotti venduti.
        # ordine.righe è una lista di RigaOrdine (classe RigaOrdine).
        # Ogni RigaOrdine contiene:
        #   - riga.prodotto (ProdottoRecord)
        #   - riga.quantita (int)
        # _statistiche_prodotti è un Counter che tiene traccia del totale venduto.
        for riga in ordine.righe:
            # Aggiornamento statistiche prodotti: Counter gestisce automaticamente
            # l’incremento e permette analisi successive (top N, ordinamenti, ecc.).
            # L’uso di riga.prodotto.name è corretto perché ProdottoRecord è hashable.
            self._statistiche_prodotti[riga.prodotto.name] += riga.quantita

        # Inserisce l’ordine nella categoria corretta.
        # ordine.cliente.categoria arriva dalla classe ClienteRecord.
        # _ordini_per_categoria è un defaultdict(list):
        #   - la chiave è la categoria (str)
        #   - il valore è una lista di Ordin
        self._ordini_per_categoria[ordine.cliente.categoria].append(ordine)

        # Archivia l’ordine tra quelli processati.
        # _ordini_processati è una lista semplice di Ordine.
        self._ordini_processati.append(ordine)

        print("Ordine processato correttamente!")

        # Restituisce True per indicare che l’ordine è stato processato correttamente. Inoltre,
        # restituisce anche l'ordine creato.
        return True, ordine



    def processa_tutti_ordini(self):
        """Processa tutti gli ordini presenti in coda"""
        # Metodo che delega completamente a processa_prossimo_ordine().
        # Design corretto: evita duplicazione di logica e mantiene il codice DRY.
        # Il while sulla deque è sicuro perché popleft() la svuota progressivamente.
        print("\n" + "=" * 60)
        print(f"Processando {len(self._ordini_da_processare)} ordini!")
        # Creo una lista che conterrà tutti gli ordini processati e sarà il return di questo metodo,
        # ad esempio userò il return in controller.py
        ordini = []
        while self._ordini_da_processare:
            _,ordine = self.processa_prossimo_ordine()
            # processa_prossimo_ordine() ha due parametri come return. Qui il secondo non mi serve, però
            # DEVO dargli un nome fittizio: lo chiamo _ (è una convenzione questo nome fittizio).
            ordini.append(ordine)
        print("Tutti gli ordini sono stati processati!")
        return ordini



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
        """
        Restituisce il fatturato totale generato da ogni categoria cliente.
        La struttura dati usata è _ordini_per_categoria, un defaultdict(list)
        popolato durante processa_prossimo_ordine().
        Ogni chiave è una categoria (stringa), ogni valore è una lista di Ordine.
        """

        valori = []  # Lista finale di tuple (categoria, fatturato)

        # Itero su tutte le categorie presenti nel dizionario.
        # Le chiavi provengono da ordine.cliente.categoria (classe ClienteRecord).
        for cat in self._ordini_per_categoria.keys():
            # Recupero la lista degli ordini associati a quella categoria.
            # Ogni elemento della lista è un oggetto della classe Ordine.
            ordini = self._ordini_per_categoria[cat]

            # Calcolo il fatturato totale della categoria.
            # La list comprehension crea una lista di totali lordi, uno per ogni ordine.
            # o.totale_lordo(0.22) richiama il metodo della classe Ordine,
            # che a sua volta somma le righe ordine (RigaOrdine) e applica l'IVA.
            totale_Fatturato = sum([o.totale_lordo(0.22) for o in ordini])

            # Aggiungo una tupla (categoria, fatturato) alla lista dei risultati.
            valori.append((cat, totale_Fatturato))

        # Restituisco la lista completa con il fatturato per categoria.
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
        for prod, quantita in self.get_statistiche_prodotti():
            print(f"{prod}: {quantita}")

        print("Fatturato per categoria:")
        for cat, fatturato in self.get_distribuzione_categorie():
            print(f"{cat} : {fatturato}")


    def get_riepilogo(self):
        """Restituisce info di massima"""
        # Metodo che restituisce le info di massima. Mi serve per controller.py. Non posso usare in
        # controller.py stampa_riepilogo() perché non ha return. Qui creo invece una stringa sommario
        #  che conterrà tutto il riepilogo e sarà il return di questo metodo.
        sommario = ""
        sommario += ("\n" + "=" * 60)
        sommario += f"\n Ordini correttamente gestiti: {len(self._ordini_processati)}"
        sommario += f"\n Ordini in coda: {len(self._ordini_da_processare)}"

        sommario += "\n Prodotti più venduti:"
        for prod, quantita in self.get_statistiche_prodotti():
            sommario += f"\n {prod}: {quantita}"

        sommario += "\n Fatturato per categoria:"
        for cat, fatturato in self.get_distribuzione_categorie():
            sommario += f"\n {cat} : {fatturato}"
        sommario += ("\n" + "=" * 60)

        return sommario


def test_modulo():
       # Crea un'istanza della classe GestoreOrdini.
       sistema = GestoreOrdini()

       # Creo degli ordini per poter testare GestoreOrdini
       ordini = [
           Ordine([RigaOrdine(ProdottoRecord("Laptop", 1200.0), 1),
                   RigaOrdine(ProdottoRecord("Mouse", 10.0), 3)],
                  ClienteRecord("Mario Rossi", "mario@mail.it", "Gold")),

           Ordine([RigaOrdine(ProdottoRecord("Laptop", 1200.0), 1),
                   RigaOrdine(ProdottoRecord("Mouse", 10.0), 2),
                   RigaOrdine(ProdottoRecord("Tablet", 500.0), 1),
                   RigaOrdine(ProdottoRecord("Cuffie", 250.0), 3)],
                  ClienteRecord("Fulvio Bianchi", "bianchi@gmail.com", "Gold")),

           Ordine([RigaOrdine(ProdottoRecord("Laptop", 1200.0), 2),
                   RigaOrdine(ProdottoRecord("Mouse", 10.0), 2)],
                   ClienteRecord("Giuseppe Averta", "giuseppe.averta@polito.it", "Silver")),

           Ordine([RigaOrdine(ProdottoRecord("Tablet", 900.0), 1),
                   RigaOrdine(ProdottoRecord("Cuffie", 250.0), 3)],
                   ClienteRecord("Carlo Masone", "carlo@mail.it", "Gold")),

           Ordine([RigaOrdine(ProdottoRecord("Laptop", 1200.0), 1),
                   RigaOrdine(ProdottoRecord("Mouse", 10.0), 2)],
                   ClienteRecord("Francesca Pistilli", "francesca@gmail.com", "Bronze"))
       ]

       for o in ordini:
           sistema.add_ordine(o)

       sistema.processa_tutti_ordini()

       sistema.stampa_riepilogo()





if __name__ == "__main__":
    test_modulo()
    # Il triangolino verde indica che test_modulo() viene eseguito quando faccio il play
    # di gestoreOrdini