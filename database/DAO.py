from database.DB_connect import DBConnect
from model.airport import Airport
from model.connessione import Connessione


class DAO():

    @staticmethod
    def getALlNodes(Nmin, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select tmp.ID, tmp.IATA_CODE, count(*) as N
                    from (
                    SELECT a.ID , a.IATA_CODE , f.AIRLINE_ID, count(*) as n
                    FROM airports a , flights f 
                    WHERE a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID 
                    group by a.ID , a.IATA_CODE , f.AIRLINE_ID
                    ) as tmp
                    group by tmp.ID, tmp.IATA_CODE
                    having N >= %s"""
        """la query più interna:
        - Questa subquery seleziona gli aeroporti (airports a) e i voli (flights f) combinati dove l'ID dell'aeroporto 
        corrisponde all'ID dell'aeroporto di partenza (ORIGIN_AIRPORT_ID) o di destinazione (DESTINATION_AIRPORT_ID) 
        nel dataset dei voli.
        - Conta il numero di record (voli) per ciascuna combinazione di aeroporto, codice IATA e ID della compagnia aerea.
        - Raggruppa per a.ID (ID dell'aeroporto), a.IATA_CODE (codice IATA dell'aeroporto) e f.AIRLINE_ID (ID della 
        compagnia aerea).
        - Ordina i risultati per a.ID e f.AIRLINE_ID.
        
        la query esterna:
        - La query esterna seleziona i risultati della subquery interna (alias tmp) e conta il numero di righe risultanti 
        per ciascun ID e IATA_CODE.
        - Raggruppa per tmp.ID e tmp.IATA_CODE.
        - HAVING N >= 5 filtra i risultati per includere solo gli aeroporti che hanno almeno 5 record di voli 
        (sia come origine che come destinazione)."""

        cursor.execute(query, (Nmin,))

        for row in cursor:
            result.append(idMap[row["ID"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getALlEdgesV1(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID , count(*) as n
                    FROM flights f 
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID"""


        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(idMap[row["ORIGIN_AIRPORT_ID"]],
                                     idMap[row["DESTINATION_AIRPORT_ID"]],
                                      row["n"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result