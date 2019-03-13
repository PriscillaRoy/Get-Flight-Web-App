import sys
from src.webapp.airport_info_service import AirportInfoService
from src.webapp.airport_status import AirportStatus


class Driver():
  def __init__(self, filename):
    self.service = AirportInfoService()
    self.airport_status = AirportStatus()
    self.filename = filename

    self.driver()


  def driver(self):
    airports, errors = self.airport_status.get_airports_status(
      self.get_airport_codes(), self.service.fetch_data)

    self.printer(airports, errors)


  def printer(self, airports, errors):
    print(f'{"Name":40} {"City":20} {"State":10} {"Temperature":20} {"Delay"}')
    print('-' * 100)

    for airport in airports:
      print("{name:40} {city:20} {state:10} {temp:22} {delay:5}"
        .format(delay = "*" if airport.delay else " ", name = airport.name,
          city = airport.city, state = airport.state, temp = airport.temperature[0]))

    if len(errors): 
      print('\nError getting details for:')
      for airport_error in errors:
        print(f'{airport_error:10}')


  def get_airport_codes(self):
    with open(self.filename) as file:
      lines = [line.strip() for line in file]

    return lines

if __name__ == "__main__":
  Driver(sys.argv[1])