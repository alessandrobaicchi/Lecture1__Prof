import mysql.connector

from dao.dbConnect import DBConnect
from gestionale.core.cliente import ClienteRecord
from gestionale.core.prodotto import ProdottoRecord


class DAO:

    # ************************************* PROTOTIPI DI METODI CHE LEGGONO DAL DB*********************************
    @staticmethod
    def getAllProdotti():
        # Creo la connessione al DB
        # cnx = mysql.connector.connect(
        #     user = "root",
        #     password = "root",
        #     host="127.0.0.1",
        #     database="sw_gestionale"
        # )
        cnx = DBConnect.getConnection()

        # Prendo un cursore (cursor) che serve per scorrere i risultati delle mie query
        cursor = cnx.cursor(dictionary=True)
        # Esegue una query SQL che scrivo all'interno di una stringa
        cursor.execute("SELECT * FROM prodotti")
        row = cursor.fetchall()    # E' una lista di dizionari
        # fetchall() restituisce tutte le righe. In questo caso sarà una lista di tuple,
        # perché non ho specificato il tipo di output che mi aspetto (in cursor=cnx.cursor()).

        res = [] # Lista vuota
        for p in row:
            # Creo un ProdottoRecord e lo aggiungo alla lista res: sto creando dei DTO.
            res.append(ProdottoRecord(p["nome"],p["prezzo"]))
            # "nome" e "prezzo" sono i nomi delle colonne del database.

        # Lo faccio per tutte le righe e alla fine faccio la chiusura. Faccio la return di res.
        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def getAllClienti():
        # Creo la connessione al DB
        # cnx = mysql.connector.connect(
        #     user = "root",
        #     password = "root",
        #     host="127.0.0.1",
        #     database="sw_gestionale"
        # )
        cnx = DBConnect.getConnection()

        # Prendo un cursore (cursor) che serve per scorrere i risultati delle mie query
        cursor = cnx.cursor(dictionary=True)
        # Esegue una query SQL che scrivo all'interno di una stringa
        cursor.execute("SELECT * FROM clienti")
        row = cursor.fetchall()    # E' una lista di dizionari
        # fetchall() restituisce tutte le righe. In questo caso sarà una lista di tuple,
        # perché non ho specificato il tipo di output che mi aspetto (in cursor=cnx.cursor()).

        res = [] # Lista vuota
        for p in row:
            # Creo un ClienteRecord e lo aggiungo alla lista res: sto creando dei DTO.
            res.append(ClienteRecord(p["nome"],p["mail"],p["categoria"]))
            # "nome", "mail" e "categoria" sono i nomi delle colonne del database.

        # Lo faccio per tutte le righe e alla fine faccio la chiusura. Faccio la return di res.
        cursor.close()
        cnx.close()
        return res


    # ************************************* PROTOTIPI DI METODI CHE SCRIVONO SUL DB*********************************
    @staticmethod
    def addProdotto(prodotto):
        # Creo la connessione al DB
        # cnx = mysql.connector.connect(
        #     user = "root",
        #     password = "root",
        #     host="127.0.0.1",
        #     database="sw_gestionale"
        # )
        cnx = DBConnect.getConnection()

        # Prendo un cursore (cursor) che serve per scorrere i risultati delle mie query
        cursor = cnx.cursor()
        # Esegue una query SQL che scrivo all'interno di una stringa
        query = """INSERT INTO prodotti (nome,prezzo) VALUES (%s,%s)"""
        # Per migliorare la leggibilità del codice scrivo la query in una stringa a parte (qui query) che poi metto
        # nell'execute.
        cursor.execute(query, (prodotto.name,prodotto.prezzo_unitario))
        # I due parametri devono stare in una tupla, perché l'execute si aspetta una query e una tupla di
        # parametri.

        # Sto facendo un execute di una query che modifica il database, quindi, mi serve da fare il commit.
        cnx.commit()    # Questa istruzione va a modificare il database.
        cursor.close()
        cnx.close()
        return

    @staticmethod
    def addCliente(cliente):
        # Creo la connessione al DB
        # cnx = mysql.connector.connect(
        #     user = "root",
        #     password = "root",
        #     host="127.0.0.1",
        #     database="sw_gestionale"
        # )
        cnx = DBConnect.getConnection()

        # Prendo un cursore (cursor) che serve per scorrere i risultati delle mie query
        cursor = cnx.cursor()
        # Esegue una query SQL che scrivo all'interno di una stringa
        query = """INSERT INTO clienti (nome,mail,categoria) VALUES (%s,%s,%s)"""
        # Per migliorare la leggibilità del codice scrivo la query in una stringa a parte (qui query) che poi metto
        # nell'execute.
        cursor.execute(query, (cliente.nome,cliente.mail,cliente.categoria))
        # I tre parametri devono stare in una tupla, perché l'execute si aspetta una query e una tupla di
        # parametri.

        # Sto facendo un execute di una query che modifica il database, quindi, mi serve da fare il commit.
        cnx.commit()    # Questa istruzione va a modificare il database.
        cursor.close()
        cnx.close()
        return

    # ************************************* ALTRI METODI*********************************

    # Questo metodo controlla se esiste già nel database un cliente con la stessa mail.
    # Restituisce True se il cliente è presente, False altrimenti.
    @staticmethod
    def hasCliente(cliente):

        # 1) Creo la connessione al database.
        #    Il DAO è l’unico punto dell’applicazione autorizzato a farlo.
        # cnx = mysql.connector.connect(
        #     user="root",
        #     password="root",
        #     host="127.0.0.1",
        #     database="sw_gestionale"
        # )
        cnx = DBConnect.getConnection()

        # 2) Creo un cursore in modalità dictionary=True.
        #    Questo significa che ogni riga letta sarà un dizionario
        #    con chiavi uguali ai nomi delle colonne.
        cursor = cnx.cursor(dictionary=True)

        # 3) Preparo la query SQL.
        #    Cerco un cliente con la stessa mail del cliente passato come parametro.
        #    Usiamo il placeholder %s per evitare SQL injection.
        query = "SELECT * FROM clienti WHERE mail = %s"

        # 4) Eseguo la query passando una tupla con il valore della mail.
        #    Il prof lo ha spiegato: cerchiamo per chiave primaria (mail),
        #    perché due clienti con la stessa mail NON possono esistere.
        cursor.execute(query, (cliente.mail,))

        # 5) fetchall() legge tutte le righe restituite dalla query.
        #    In questo caso la lista sarà:
        #       - vuota  → il cliente NON esiste
        #       - con 1 elemento → il cliente ESISTE
        row = cursor.fetchall()

        # 6) Chiudo il cursore e la connessione (buona pratica sempre).
        cursor.close()
        cnx.close()

        # 7) Ritorno True se ho trovato almeno una riga.
        #    Il prof lo ha spiegato chiaramente:
        #    “Se row contiene almeno una riga, quel cliente c’è già”.
        return len(row) > 0


    # Considerazioni analoghe al metodo hasCliente()
    @staticmethod
    def hasProdotto(prod):
        # Creo la connessione al DB
        # cnx = mysql.connector.connect(
        #     user="root",
        #     password="root",
        #     host="127.0.0.1",
        #     database="sw_gestionale"
        # )
        cnx = DBConnect.getConnection()

        # Prendo un cursore (cursor) che serve per scorrere i risultati delle mie query
        cursor = cnx.cursor(dictionary=True)

        # Esegue una query SQL che scrivo all'interno di una stringa
        query = "SELECT * FROM prodotti WHERE nome = %s"
        cursor.execute(query, (prod.name,))

        row = cursor.fetchall()
        # fetchall() restituisce tutte le righe. In questo caso sarà una lista di tuple,
        # perché non ho specificato il tipo di output che mi aspetto (in cursor=cnx.cursor()).

        cursor.close()
        cnx.close()

        return len(row) > 0



if __name__ == '__main__':
    mydao = DAO()
    mydao.getAllProdotti()