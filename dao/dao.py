import mysql.connector

from gestionale.core.cliente import ClienteRecord
from gestionale.core.prodotto import ProdottoRecord
from gestionale.provaCollections import prodotto


class DAO:

    # ************************************* PROTOTIPI DI METODI CHE LEGGONO DAL DB*********************************
    def getAllProdotti(self):
        # Creo la connessione al DB
        cnx = mysql.connector.connect(
            user = "root",
            password = "root",
            host="127.0.0.1",
            database="sw_gestionale"
        )

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



    def getAllClienti(self):
        # Creo la connessione al DB
        cnx = mysql.connector.connect(
            user = "root",
            password = "root",
            host="127.0.0.1",
            database="sw_gestionale"
        )

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
    def addProdotto(self,prodotto):
        # Creo la connessione al DB
        cnx = mysql.connector.connect(
            user = "root",
            password = "root",
            host="127.0.0.1",
            database="sw_gestionale"
        )

        # Prendo un cursore (cursor) che serve per scorrere i risultati delle mie query
        cursor = cnx.cursor()
        # Esegue una query SQL che scrivo all'interno di una stringa
        query = """INSERT INTO prodotti (nome,prezzo) VALUES (%s,%s)"""
        # Per migliorare la leggibilità del codice scrivo la query in una stringa a parte (qui query) che poi metto
        # nell'execute.
        cursor.execute(query, (prodotto.name,prodotto.prezzo_unitario))
        # I due parametri devono stare in una tupla, perché l'execute si aspetta una query.

        # Sto facendo un execute di una query che modifica il database, quindi, mi serve da fare il commit.
        cnx.commit()    # Questa istruzione va a modificare il database.
        cursor.close()
        cnx.close()
        return


    def addCliente(self, cliente):
        # Creo la connessione al DB
        cnx = mysql.connector.connect(
            user = "root",
            password = "root",
            host="127.0.0.1",
            database="sw_gestionale"
        )

        # Prendo un cursore (cursor) che serve per scorrere i risultati delle mie query
        cursor = cnx.cursor()
        # Esegue una query SQL che scrivo all'interno di una stringa
        query = """INSERT INTO clienti (nome,mail,categoria) VALUES (%s,%s,%s)"""
        # Per migliorare la leggibilità del codice scrivo la query in una stringa a parte (qui query) che poi metto
        # nell'execute.
        cursor.execute(query, (cliente.nome,cliente.mail,cliente.categoria))
        # I tre parametri devono stare in una tupla, perché l'execute si aspetta una query.

        # Sto facendo un execute di una query che modifica il database, quindi, mi serve da fare il commit.
        cnx.commit()    # Questa istruzione va a modificare il database.
        cursor.close()
        cnx.close()
        return



if __name__ == '__main__':
    mydao = DAO()
    mydao.getAllProdotti()