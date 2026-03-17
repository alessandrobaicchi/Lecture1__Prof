import copy

from gestionale.core.prodotti import ProdottoRecord

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


