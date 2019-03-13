class AirportStatus():

  def sort_airports(self, airports):
    return sorted(airports, key = lambda airport: airport.name) 

  def get_airports_status(self, codes, service):
    airports = []
    airport_codes_with_error = []

    for code in codes:
      try:
        airports.append(service(code))
      except:
        airport_codes_with_error.append(code)

    return (self.sort_airports(airports), airport_codes_with_error)

