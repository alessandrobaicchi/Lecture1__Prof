import pathlib

import mysql.connector

class DBConnect:

    # *************************** Vedi spiegazione Lezione 11 ***************************************

    _myPool = None

    def __init__(self):
        # Serve per implemantare il pattern singletone ed impedire al chiamante di creare istanze di classe.
        raise RuntimeError("Attenzione! Non devi creare un'istanza di questa classe, usa i metodi di classe.")

    @classmethod
    # Questo metodo ha un solo compito: creare una connessione al DB e restituirla.
    # Serve per centralizzare tutti i parametri di connessione in un unico punto.
    # In questo modo, se cambiano user/password/host, modifichiamo solo qui.
    def getConnection(cls):
        if cls._myPool is None:
            try:
                # Provo a creare la connessione verso il database.
                # mysql.connector.connect può sollevare un errore se qualcosa va storto
                # (password sbagliata, DB non avviato, host errato, ecc.)
                # cnx = mysql.connector.connect(
                #     user="root",
                #     password="root",
                #     host="127.0.0.1",
                #     database="sw_gestionale"
                # )

                # Invece di creare una connessione creiamo un pool di connessioni (connection pooling).
                cls._myPool = mysql.connector.pooling.MySQLConnectionPool(
                    # user = "root",
                    # password = "root",
                    # host = "127.0.0.1",
                    # database = "sw_gestionale",
                    pool_size = 3,     # Quante connessioni posso creare
                    pool_name = "myPool",
                    option_files = f"{pathlib.Path(__file__).resolve().parent}/connector.cfg"
                )

                # Se la connessione è stata creata correttamente, la restituisco al chiamante.
                # return cnx
                # Non restituisco più la connessione, ma:
                return cls._myPool.get_connection()

            except mysql.connector.Error as err:
                # Se qualcosa va storto, intercetto l'errore.
                # Il prof lo ha spiegato: stampiamo un messaggio utile per il debugging.
                print("Non riesco a collegarmi al DB!")
                print(err)
                # Restituiamo None per indicare che la connessione NON è stata creata.
                # Il DAO che chiamerà questo metodo dovrà gestire questo caso.
                return None

        else:
            # Allora il pool esiste già, e quindi restituisco direttamente la connessione
            return cls._myPool.get_connection()

