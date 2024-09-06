import sqlite3


class Database:
    """
        class responsible for connection to the database, and data management
    """

    con = None # connection to the database


    def __init__(self, path) -> None:
        
        self.con = sqlite3.connect(path)

        #init tables
        cur = self.con.cursor()
        if not self.checkIfTableExists(cur, "stations"):
            cur.execute("CREATE TABLE stations(id, stationName)")
        if not self.checkIfTableExists(cur, "measurement_stations"):
            cur.execute("CREATE TABLE measurement_stations(id, stationId, paramName, paramCode)")
        if not self.checkIfTableExists(cur, "measurement_data"):
            cur.execute("CREATE TABLE measurement_data(measurementStationId, key, value, date)")

    def addStations(self, json):
        """
            adds stations to the database
        """

        cur = self.con.cursor()
        con_str = "INSERT OR REPLACE INTO stations(id, stationName) VALUES "
        for item in json:
            con_str = con_str + f" ({item['id']}, '{item['stationName']}'),"
        con_str = con_str[:-1]
        #cur.execute(f"INSERT INTO stations(id, stationName) VALUES ({item['id']}, '{item['stationName']}')")
        cur.execute(con_str)
        self.con.commit()
        self.removeDuplicates(cur=cur,tableName='stations', identifierName='id')

    def addMeasurementStations(self, json):
        """
            Add information about measurement stations to the database
        """
        cur = self.con.cursor()
        con_str = "INSERT OR REPLACE INTO measurement_stations(id, stationId, paramName, paramCode) VALUES "
        for item in json:
            con_str = con_str + f" ({item['id']}, {item['stationId']}, '{item['param']['paramName']}', '{item['param']['paramCode']}'),"
        con_str = con_str[:-1]
        #cur.execute(f"INSERT INTO stations(id, stationName) VALUES ({item['id']}, '{item['stationName']}')")
        cur.execute(con_str)
        self.con.commit()
        self.removeDuplicates(cur=cur, tableName='measurement_stations', identifierName='id')

    def addMeasurementData(self, json, measurementStationId):
        """
            Add measurement data to the database
        """
        cur = self.con.cursor()
        con_str = "INSERT OR REPLACE INTO measurement_data(measurementStationId, key, value, date) VALUES "
        for item in json['values']:
            if item['value'] is not None:
                con_str = con_str + f" ({measurementStationId}, '{json['key']}', {item['value']}, '{item['date']}'),"
        con_str = con_str[:-1]
        #cur.execute(f"INSERT INTO stations(id, stationName) VALUES ({item['id']}, '{item['stationName']}')")
        cur.execute(con_str)
        self.con.commit()
        self.removeDuplicates(cur=cur, tableName='measurement_data', identifierName="date, key, measurementStationId")

    def getMeasurementData(self, measurementStationId:int, time_h:float):
        """
            provides measurement data from a given measurementStationId from last X hours
        """
        cur = self.con.cursor()
        con_str = f"SELECT key, value, date FROM  measurement_data WHERE date >=datetime('now', '-{time_h} Hour') AND measurementStationId={measurementStationId};"
        res = cur.execute(con_str)
        return res.fetchall()
    
    def getStations(self):
        """returns the list of stations"""
        cur = self.con.cursor()
        con_str = f"SELECT * FROM  stations"
        res = cur.execute(con_str)
        return res.fetchall()
    
    def getMeasurementStations(self, stationId):
        """
            returns measurement stations for a given stationId
        """
        cur = self.con.cursor()
        con_str = f"SELECT * FROM  measurement_stations WHERE stationId={stationId};"
        res = cur.execute(con_str)
        return res.fetchall()


    def checkIfTableExists(self, cur, tableName:str):
        """tests if the table exists"""
        res = cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}';")
        return res.fetchone() is not None
    
    def removeDuplicates(self, cur, tableName:str, identifierName:str):
        """remove duplicates from a given table"""
        sql = f"""
        DELETE FROM {tableName}
            WHERE ROWID NOT IN (
            SELECT MIN(ROWID) 
            FROM {tableName} 
            GROUP BY {identifierName}
                    );
            """
        cur.execute(sql)
        self.con.commit()