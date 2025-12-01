from database.DB_connect import DBConnect
from model.hub import Hub
from model.spedizione import Spedizione

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO

    @staticmethod
    def readHub():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM hub"
        cursor.execute(query)
        for row in cursor:

            result.append(Hub(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_spedizione(hubs_dict):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ 
                SELECT 
                        LEAST (id_hub_origine, id_hub_destinazione ) AS hub1
                        GREATEST (id_hub_origine, id_hub_destinazione ) AS hub2
                        SUM(valore_merce)/COUNT(*) AS peso
                FROM spedizione
                GROUP BY LEAST (id_hub_origine, id_hub_destinazione )
                        GREATEST (id_hub_origine, id_hub_destinazione )
                    """
        cursor.execute(query)
        for row in cursor:
            # facendo in questo modo mi sto creando un dizionario in questo modo:
            # hub1 = {1: Hub(id, codice, nome, città, stato, latitudine, longitudine)
            # dove la chiave "1" coincide con row["hub1"]

            hub1 = hubs_dict[row["hub1"]]
            hub2 = hubs_dict[row["hub2"]]
            peso = row["peso"]

            result.append(Spedizione(hub1, hub2, peso))

        cursor.close()
        conn.close()
        return result
