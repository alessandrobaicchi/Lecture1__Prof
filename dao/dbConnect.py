import mysql.connector

class DBConnect:

    # *************************** Vedi spiegazione Lezione 11 ***************************************

    @classmethod
    # Questo metodo ha un solo compito: creare una connessione al DB e restituirla.
    # Serve per centralizzare tutti i parametri di connessione in un unico punto.
    # In questo modo, se cambiano user/password/host, modifichiamo solo qui.
    def getConnection(cls):

        try:
            # Provo a creare la connessione verso il database.
            # mysql.connector.connect può sollevare un errore se qualcosa va storto
            # (password sbagliata, DB non avviato, host errato, ecc.)
            cnx = mysql.connector.connect(
                user="root",
                password="root",
                host="127.0.0.1",
                database="sw_gestionale"
            )

            # Se la connessione è stata creata correttamente, la restituisco al chiamante.
            return cnx

        except mysql.connector.Error as err:
            # Se qualcosa va storto, intercetto l'errore.
            # Il prof lo ha spiegato: stampiamo un messaggio utile per il debugging.
            print("Non riesco a collegarmi al DB!")
            print(err)

            # Restituiamo None per indicare che la connessione NON è stata creata.
            # Il DAO che chiamerà questo metodo dovrà gestire questo caso.
            return None