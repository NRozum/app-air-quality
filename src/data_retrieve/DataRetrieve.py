import requests

class DataRetrieve:
    """
        class responsible for API connection to retrieve web data
    """

    @staticmethod
    def getStationList():
        """returns dictionary with list of all available weather stations"""
        url = "https://api.gios.gov.pl/pjp-api/rest/station/findAll"
        try:
            stationListRequest = requests.get(url=url)
        except requests.ConnectionError:
            return False
        if stationListRequest.ok:
            return stationListRequest.json()
        else:
            return False
        
    @staticmethod
    def getMeasurementStations(stationId:int):
        """returns dictionary with list of all available weather stations measurements from station of given stationId"""
        url = f"https://api.gios.gov.pl/pjp-api/rest/station/sensors/{stationId}"

        try:
            stationListRequest = requests.get(url=url)
        except requests.ConnectionError:
            return False
        if stationListRequest.ok:
            return stationListRequest.json()
        else:
            return False
    
    @staticmethod
    def getMeasurementData(sensorId:int):
        """returns dictionary with measurement data related to a given sensorId"""
        url = f"https://api.gios.gov.pl/pjp-api/rest/data/getData/{sensorId}"
        try:
            stationListRequest = requests.get(url=url)
        except requests.ConnectionError:
            return False
        if stationListRequest.ok:
            return stationListRequest.json()
        else:
            return False



