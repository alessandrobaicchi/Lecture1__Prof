import mysql.connector

class DAO:
    def getAllProdotti(self):
        cnx = mysql.connector.connect(
            user = "root",
            password = "root",
            host="127.0.0.1",
            database="sw_gestionale"
        )

        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM prodotti")
        prodotti = cursor.fetchall()
        for p in prodotti:
            print(p)

        cursor.close()
        cnx.close()
        return

if __name__ == '__main__':
    mydao = DAO()
    mydao.getAllProdotti()