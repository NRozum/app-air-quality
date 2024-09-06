
import database.database as DB
from data_retrieve import DataRetrieve

import unittest

class TestApplication(unittest.TestCase):

    def test_creationOfDatabase(self):
        db = DB.Database('test.db')
        print("Successfully created Database")
        pass

    def test_getMeasurementStations(self):
        db = DB.Database('test.db')
        measurementStations = DataRetrieve.DataRetrieve.getMeasurementStations(stationId=11)
        if measurementStations:
            db.addMeasurementStations(json=measurementStations)
        measurementStationsDb = db.getMeasurementStations(stationId=11)
        print("Successfully obtained measurement stations data")
        pass


    def test_getStations(self):
        db = DB.Database('test.db')
        stations = DataRetrieve.DataRetrieve.getStationList()
        if stations:
            db.addStations(json=stations)
        stations_db = db.getStations()
        print("Successfully obtained stations data")
        pass

    def test_getData(self):
        db = DB.Database('test.db')
        measurementData = DataRetrieve.DataRetrieve.getMeasurementData(sensorId=52)
        if measurementData:
            db.addMeasurementData(json=measurementData, measurementStationId=52)
        measurementDataDb = db.getMeasurementData(measurementStationId=52, time_h=24)
        print("Successfully obtained measurement data")
        pass


if __name__ == '__main__':
    unittest.main()