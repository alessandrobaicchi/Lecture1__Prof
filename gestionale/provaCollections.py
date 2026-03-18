import copy
from collections import Counter, deque

from gestionale.core.clienti import ClienteRecord
from gestionale.core.prodotti import ProdottoRecord
from gestionale.vendite.ordini import Ordine, RigaOrdine

# OGGETTI (istanze) di tipo ProdottoRecord
p1 = ProdottoRecord("Laptop", 1200.0)
p2 = ProdottoRecord("Mouse", 20.0)
p3 = ProdottoRecord("Auricolari", 250.0)

####################################### LISTE ###############################################

# CREO UNA LISTA con gli oggetti creati prima + uno creato "sul momento". L'unica differenza è che
# quest'ultimo non ha un nome tipo gli altri tre e così posso accedere a lui solo come elemento della lista
# (ciò per la lista carrello è irrilevante).
carrello = [p1, p2, p3, ProdottoRecord("Tablet", 700.0)]

print("Prodotti nel carrello:")
# enumerate() è un metodo che prende come argomento una lista e mi restituisce una lista di tuple,
# dove il primo elemento è l'indice e il secondo elemento è l'elemento stesso.
for i, p in enumerate(carrello):
    print(f"{i}) {p.name} - {p.prezzo_unitario}")

#AGGIUNGERE elementi ad una lista
carrello.append(ProdottoRecord("Monitor", 150.0))

# ORDINARE una lista
# carrello.sort() --> ordina in place, quindi modifica direttamente la lista senza crearne una nuova.

# key = lambda x: x.prezzo_unitario --> questa è la funzione che dice in base a cosa ordinare.
# 👉 x è ogni elemento della lista
# 👉 x.prezzo_unitario è il valore usato per confrontare gli elementi.
# 👉 In pratica: ordina gli oggetti del carrello in base al loro prezzo unitario
# (qui in ordine decrescente perché reverse = TRUE)
carrello.sort(key = lambda x: x.prezzo_unitario, reverse=True)

# print("Prodotti nel carrello:")
# for i, p in enumerate(carrello):
#     print(f"{i}) {p.name} - {p.prezzo_unitario}")

# FUNZIONE AGGREGATA sulla lista
tot = sum(p.prezzo_unitario for p in carrello)
# E' una GENERATOR EXPRESSION. L'elemento p scorre tutti gli oggetti in carrello, estraendone il prezzo_unitario.
# Quindi, a ogni estrazione sum() accumula i valori uno alla volta. Alla fine tot contiene la sommma di tutti
# i prezzi unitari. La GENERATOR EXPRESSION NON CREA UNA LISTA TEMPORANEA, cosa che invece farebbe
# la list comprehension (meno efficente) la cui sintassi è simile: tot = sum([p.prezzo_unitario for p in carrello]).
print(f"Totale del carrello: {tot}")

# AGGIUNGERE elementi alla lista
carrello.append(ProdottoRecord("Propdo", 100.0))    # append() aggiunge un elemento in coda alla lista
carrello.extend([ProdottoRecord("aaa", 100.0), ProdottoRecord("bbb", 100.0)])   # extend() aggiunge una lista
carrello.insert(2, ProdottoRecord("ccc", 100.0))    # insert() aggiunge un elemento in una posizione specifica

# RIMUOVERE elementi dalla lista
carrello.pop() # pop() rimuove l'ultimo elemento
carrello.pop(2) # pop(indice) rimuove l'elemento in posizione 2
carrello.remove(p1) # remove() elimina la prima occorrenza di p1
# carrello.clear() # clear() svuota la lista

# ORDINARE (Sorting) gli elementi di una lista
# carrello.sort() #ordina seguendo ordinamento naturale (non funziona se gli oggetti contenuti non definisco un metodo __lt__)
# carrello.sort(reverse=True) #ordina al contrario
# carrello.sort(key = function) # ad esempio usando la lambda function
# carrello_ordinato = sorted(carrello) # a differenza di sort(), sorted() non modifica la lista originale ma ne crea una nuova

#COPIE ed altro su una lista
carrello.reverse() # inverte l'ordine
carrello_copia = carrello.copy()          # Shallow copy:
                                          # - crea una nuova lista
                                          # - gli elementi NON vengono copiati
                                          # - nella nuova lista ci sono riferimenti
                                          #   agli STESSI oggetti della lista originale (condivisi in memoria)
                                          # 👉 nuova lista, stessi oggetti → nessuna duplicazione in memoria degli elementi.

carrello_copia2 = copy.deepcopy(carrello) # Deep copy:
                                          # - crea una nuova lista
                                          # - crea anche nuove copie degli oggetti contenuti
                                          # - nella nuova lista ci sono riferimenti
                                          #   a NUOVI oggetti (nuova memoria allocata), indipendenti dagli originali
                                          # 👉 nuova lista, nuovi oggetti → duplicazione completa in memoria.


####################################### TUPLE ###############################################

# TUPLE
sede_principale = (45, 8) # ad esempio, latitudine e longitudine della sede di Torino
sede_milano = (45, 9) # ad esempio, latitudine e longitudine della sede di Milano
# Perché lo faccio con una tupla e non con una lista? Perché  la latitudine e la longitudine non cambiano.

# ACCESSO ai valori di una tupla
print(f"Sede principale lat: {sede_principale[0]}, long: {sede_principale[1]}")

# Una tupla che contiene le varie aliquote iva (che sono tuple): tupla che contiene tuple!
AliquoteIVA = (
    ("Standard", 0.22),
    ("Ridotta", 0.10),
    ("Alimentari", 0.04),
    ("Esente", 0.0)
)

# Ciclo for su una tupla di tuple
for descr, valore in AliquoteIVA:
    print(f"{descr}: {valore*100}%")

def calcola_statistiche_carrello(carrello):
    """Restituisce prezzo totale, prezzo medio, massimo e minimo"""
    prezzi = [p.prezzo_unitario for p in carrello]
    # prezzi = [p.prezzo_unitario for p in carrello] è una list comprehension:
    # - crea una lista vera e propria in memoria
    # - è utile se devo riutilizzare la lista più volte (come in questo caso)
    return (sum(prezzi), sum(prezzi)/len(prezzi), max(prezzi), min(prezzi))
    # Il return restituisce una TUPLA di 4 valori:
    # (totale, media, massimo, minimo)
    # Restituire una tupla è perfettamente valido in Python.


tot, media, max, min = calcola_statistiche_carrello(carrello)
# Mi aspetto già come return una tupla di 4 elementi e così faccio l'unpacking degli elementi della tupla del return.
# Tuple unpacking:
# - la funzione restituisce una tupla di 4 elementi
# - Python assegna automaticamente ogni elemento della tupla
#   alla variabile corrispondente (tot, media, max, min)
# - il numero di variabili DEVE corrispondere al numero di elementi della tupla
print(tot, media, max, min)

# L'alternativa è: tupla = calcola_statistiche_carrello(carrello)
# e poi faccio tupla[0], tupla[1], ...

# Ulteriore alternativa è usare *
# tot, *altri_campi = calcola_statistiche_carrello(carrello)
# La funzione restituisce una tupla di 4 elementi, e poi:
# Unpacking con star:
# - 'tot' prende il primo elemento della tupla
# - '*altri_campi' raccoglie TUTTI gli altri elementi
#   e li mette in una LISTA (non in una tupla)
# L’operatore * nell’unpacking ha una regola precisa:
# “Raccogli tutti gli elementi rimanenti e mettili in una lista.”
# Non in una tupla, non in un set, non in un’altra struttura: sempre una lista.
# print(tot, *altri_campi)
# '*altri_campi' espande la lista nei singoli valori
# quindi stampa tutti i valori restituiti dalla funzione.
# La stampa finale saranno i 4 valori restituiti dalla funzione.






####################################### SET ###############################################

#SET
# Un set ha due proprietà fondamentali:
# - non contiene duplicati
# - non mantiene l’ordine

categorie = {"Gold", "Silver", "Bronze", "Gold"}
# Creo un SET:
# - struttura non ordinata
# - NON ammette duplicati --> il secondo "Gold" viene automaticamente eliminato
print(categorie)
# Stampa il set (ordine arbitrario, perché i set non mantengono l'ordine)
print(len(categorie))
# Stampa la quantità di elementi unici del set → 3

# Posso fare l'UNIONE  due set
categorie2 = {"Platinum", "Elite", "Gold"}
categorie_all = categorie.union(categorie2)
#categorie_all = categorie | categorie2 # E' equivalente a sopra: unisce due set
print(categorie_all)

# Posso fare l'INTERSEZIONE tra due set --> prendo solo gli elementi comuni
categorie_comuni = categorie & categorie2
# Operatore '&' = INTERSEZIONE tra set.
# Restituisce un nuovo set contenente SOLO gli elementi presenti in entrambi i set.
print(categorie_comuni)
# Stampa gli elementi comuni → {'Gold'}


# Posso fare la DIFFERENZA tra set --> prendo solo gli elementi presenti in uno dei due set
categorie_esclusive = categorie - categorie2
# Operatore '-' = DIFFERENZA tra set.
# Restituisce un nuovo set con gli elementi presenti in 'categorie', ma NON presenti in 'categorie2'.
# In questo caso → {"Silver", "Bronze"}
print(categorie_esclusive)

# Posso fare la DIFFERENZA SIMMETRICA tra set
categorie_esclusive_symm = categorie ^ categorie2 # differenza simmetrica
# Operatore '^' = DIFFERENZA SIMMETRICA tra set.
# Restituisce un nuovo set con:
# - tutti gli elementi presenti in UNO dei due set, ma NON presenti in ENTRAMBI.
# In questo caso → {"Silver", "Bronze", "Platinum", "Elite"}
print(categorie_esclusive_symm)


# Posso creare un set di OGGETTI creati da me, ad esempio ProdottoRecord. E su questi posso
# usare quanto fatto sopra: |, &, ...
prodotti_ordine_A = {ProdottoRecord("Laptop", 1200),
                     ProdottoRecord("Mouse", 20),
                     ProdottoRecord("Tablet", 700)}

prodotti_ordine_B = {ProdottoRecord("Laptop2", 1200),
                     ProdottoRecord("Mouse2", 20),
                     ProdottoRecord("Tablet", 700)}
# Nota. Ho dovuto scrivere una funzione di hash() per ProdottoRecord perché il set vuole oggetti hashable.

#METODI UTILI per i set
s = set()
s1 = set()

#Aggiungere
s.add(ProdottoRecord("aaa", 20.0))
# add() inserisce UN singolo elemento nel set.
# - Se l'oggetto non è presente → viene aggiunto.
# - Se è già presente → nessuna modifica (i set non ammettono duplicati).
# Nota: gli oggetti devono essere hashable (es. dataclass frozen=True).

s.update([ProdottoRecord("aaa", 20.0), ProdottoRecord("bbb", 20.0)]) #aggiungo più elementi
# update() inserisce TUTTI gli elementi di un iterabile passato (lista, set, tupla…, in questo caso è una lista).
# È equivalente a chiamare add() in un ciclo.
# Gli eventuali duplicati vengono ignorati automaticamente dal set.
# - "aaa" non viene aggiunto se è già presente nel set
# - "bbb" viene aggiunto perché è un nuovo elemento
# Dopo questa riga: s contiene 2 elementi.



#Togliere
#s.remove(nome_elemento) # Rimuove un elemento. Raise KeyError se non esiste.
#s.discard(nome_elemento) # Rimuove un elemento, senza "arrabbiarsi" se questo non esiste.
#s.pop() # Rimuove e restituisce un elemento.
#s.clear() # Svuota il set.

#Operazioni insiemistiche (già viste sopra)
#s.union(s1) # s | s1, ovvero genera un set che unisce i due set di partenza
#s.intersection(s1) # s & s1, ovvero solo elementi comuni
#s.difference(s1) # s-s1, ovvero elementi di s che non sono contenuti in s1
#s.symmetric_difference(s1) #s ^s1, ovvero elementi di s non contenuti in s1 ed elementi di s1 non contenuti in s

# s1.issubset(s) # se gli elementi di s1 sono contenuti in s
# s1.issuperset(s) # se gli elementi di s sono contenuti in s1
# s1.isdisjoint(s) # se gli elementi di s e quelli di s1 sono diversi







####################################### DIZIONARI ###############################################
catalogo = {
    # E' un Dizionario: chiave = codice prodotto (stringa, che è hashable)
    #                   valore = istanza di ProdottoRecord
    "LAP001": ProdottoRecord("Laptop", 1200.0),
    "LAP002": ProdottoRecord("Laptop Pro", 2300.0),
    "MAU001": ProdottoRecord("Mouse", 20.0),
    "AUR001": ProdottoRecord("Auricolari", 250.0),
}
# Accesso O(1): recupero diretto del prodotto tramite la chiave
cod = "LAP002"

prod = catalogo[cod]
# Grazie al metodo __str__, la stampa è leggibile
print(f"Il prodotto con codice {cod} è {prod}")


# Se accedo a una chiave inesistente con [], ottengo un KeyError.
# catalogo["NonEsiste"]
# get() evita il KeyError e restituisce None se la chiave non esiste.
prod1 = catalogo.get("NonEsiste")
if prod1 is None:
    print("Prodotto non trovato")

# Possiamo specificare un valore di default da restituire se la chiave non esiste.
prod2 = catalogo.get("NonEsiste2", ProdottoRecord("Sconosciuto", 0.0))
print(prod2)


# --- Ciclare su un dizionario ---

# Recupero delle chiavi e dei valori (view objects).
keys = list(catalogo.keys())     # Converto in lista per stamparli facilmente.
values = list(catalogo.values())

for k in keys:
    print(k)                     # Stampa tutte le chiavi del dizionario.

for v in values:
    print(v)                     # Stampa tutti i valori del dizionario.

# Iterazione diretta su chiave e valore tramite items().
for k, v in catalogo.items():
    print(f"Il codice {k} è associato a: {v}")



# --- Rimuovere oggetti da un dizionario ---
# pop() rimuove la chiave e restituisce il valore associato.
rimosso = catalogo.pop("LAP002")
print(rimosso)



# --- Dict comprehension ---
# Creo un nuovo dizionario che mappa codice → prezzo.
prezzi = {codice: prod.prezzo_unitario for codice, prod in catalogo.items()}


# Altri metodi da sapere
# d[key] = v # Scrivere sul dizionario
# v = d[key] # Leggere da un dizionario, restituisce "keyerror" se non esiste quella chiave
# v = d.get(key, default) # Leggere da un dizionario senza rischiare "keyerror", se non esiste restituisce il default
# d.pop(key) # Restituisce un valore e lo cancella dal dizionario
# d.clear() # Elimina tutto
# d.keys() # Restituisce tutte le chiavi definite nel dizionario
# d.values() # Restituisce tutti i valori definiti nel dizionario
# d.items() # Restituisce tutte le coppie chiave + valore definite nel dizionario
# k in d # Condizione che verifica se key è presente nel dizionario


"""Esercizio live -- Per ciascuno di questi casi, decidere quale struttura dati usare:"""

# 1) Memorizzare un elenco di ordini da processare in ordine di arrivo
# Una LISTA mantiene l'ordine di inserimento ed è perfetta per una coda semplice.
ordini_da_processare = []

o1 = Ordine([], ClienteRecord("Mario Rossi", "mario@polito.it", "Gold"))
o2 = Ordine([], ClienteRecord("Mario Bianchi", "bianchi@polito.it", "Silver"))
o3 = Ordine([], ClienteRecord("Fulvio Rossi", "fulvio@polito.it", "Bronze"))
o4 = Ordine([], ClienteRecord("Carlo Masone", "carlo@polito.it", "Gold"))

# Salvo anche il tempo di arrivo per poter ordinare successivamente.
ordini_da_processare.append((o1, 0))
ordini_da_processare.append((o2, 10))
ordini_da_processare.append((o3, 3))
ordini_da_processare.append((o4, 45))


# 2) Memorizzare i codici fiscali dei clienti (univoco)
# Un SET garantisce l'unicità degli elementi.
codici_fiscali = {
    "gjdlkgkdjg52",
    "ojoirehghpreiuh25",
    "euyiifgugfuioi78",
    "euyiifgugfuioi78"  # duplicato, verrà ignorato
}
print(codici_fiscali)


# 3) Creare un database di prodotti cercabili tramite codice univoco
# Un DIZIONARIO permette ricerche O(1) tramite chiave.
listino_prodotti = {
    "LAP0001": ProdottoRecord("Laptop", 1200.0),
    "KEY001": ProdottoRecord("Keybord", 20.0),
}


# 4) Memorizzare le coordinate GPS della nuova sede di Roma
# Una TUPLA è immutabile e perfetta per dati fissi.
magazzino_roma = (45, 6)


# 5) Tenere traccia delle categorie dei clienti che hanno fatto un ordine
# Un SET evita duplicati e permette aggiunte O(1).
categorie_periodo = set()
categorie_periodo.add("Gold")
categorie_periodo.add("Bronze")





###################################### COUNTER ##########################################

print("=================================================================================")

# Lista di clienti che hanno effettuato ordini
lista_clienti = [
    ClienteRecord("Mario Rossi", "mario@polito.it", "Gold"),
    ClienteRecord("Mario Bianchi", "bianchi@polito.it", "Silver"),
    ClienteRecord("Fulvio Rossi", "fulvio@polito.it", "Bronze"),
    ClienteRecord("Carlo Masone", "carlo@polito.it", "Gold"),
    ClienteRecord("Mario Bianchi", "mario@polito.it", "Gold"),
    ClienteRecord("Giuseppe Averta", "bianchi@polito.it", "Silver"),
    ClienteRecord("Francesca Pistilli", "fulvio@polito.it", "Bronze"),
    ClienteRecord("Carlo Masone", "carlo@polito.it", "Gold"),
    ClienteRecord("Fulvio Corno", "carlo@polito.it", "Silver")
]

# Estraggo tutte le categorie tramite list comprehension
categorie = [c.categoria for c in lista_clienti]

# Creo un Counter per contare le occorrenze delle categorie
categorie_counter = Counter(categorie)

print("Distribuzione categorie clienti")
print(categorie_counter)

# Mostro le due categorie più frequenti
print("Le due categorie più frequenti sono:")
print(categorie_counter.most_common(2))

# Totale degli elementi contati
print("Totale elementi:")
print(categorie_counter.total())

# Counter per vendite mensili
vendite_gennaio = Counter({"Laptop": 13, "Tablet": 15})
vendite_febbraio = Counter({"Laptop": 3, "Stampanti": 1})

# Aggregazione tramite somma
vendite_bimestre = vendite_gennaio + vendite_febbraio

print(f"Vendite Gennaio: {vendite_gennaio}")
print(f"Vendite Febbraio: {vendite_febbraio}")
print(f"Vendite Bimestre: {vendite_bimestre}")

# Differenza tra Counter
print(f"Differenza vendite: {vendite_gennaio - vendite_febbraio}")

# Modifica dei valori on the fly
vendite_gennaio["Laptop"] += 4
print(f"Vendite Gennaio aggiornate: {vendite_gennaio}")

# Metodi da ricordare:
# c.most_common(n)  -> restituisce gli n elementi più frequenti
# c.total()         -> somma dei conteggi




###################################### DEQUE ##########################################

print("=================================================================================")
print("Deque")

coda_ordini = deque()
# Creo una coda FIFO di ordini usando deque (O(1) per append e popleft)

for i in range(1, 10):
    # Simulo l'arrivo di un nuovo ordine
    cliente = ClienteRecord(f"Cliente {i}", f"cliente{i}@polito.it", "Gold")
    # Creo un cliente con nome e mail parametrica, categoria fissa
    prodotto = ProdottoRecord(f"Prodotto{i}", 100.0 * i)
    # Creo un prodotto con nome parametrico e prezzo crescente
    ordine = Ordine([RigaOrdine(prodotto, 1)], cliente)
    # Creo un ordine composto da una singola riga ordine
    coda_ordini.append(ordine)
    # Accodo l'ordine alla coda FIFO (append → aggiunge a destra)

print(f"Ordini in coda: {len(coda_ordini)}")
# Stampo quanti ordini sono stati accodati

while coda_ordini:
    # Il ciclo continua finché la coda non è vuota
    ordine_corrente = coda_ordini.popleft()
    # popleft → rimuove l'ordine più vecchio (FIFO)
    print(f"Sto gestendo l'ordine del cliente: {ordine_corrente.cliente}")
    # Stampo il cliente dell'ordine corrente (usa __str__)

print("Ho processato tutti gli ordini!")
# Conferma finale quando la coda è vuota