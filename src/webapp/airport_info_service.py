import requests
import json
from src.webapp.airport import Airport


class AirportInfoService():
  def get_JSON(self, code): 
    BASEPATH = "https://soa.smext.faa.gov/asws/api/airport/status/"
    return requests.get("".join([BASEPATH, code])).text


  def create_airport(self, json_format_data):
    if 'Name' not in json_format_data:
      raise Exception

    json_data = json.loads(json_format_data)

    return Airport(json_data['IATA'], json_data['Name'],json_data['City'],
      json_data['State'],json_data['Weather']['Temp'],json_data['Delay'])


  def fetch_data(self,code):
    return self.create_airport(self.get_JSON(code))
