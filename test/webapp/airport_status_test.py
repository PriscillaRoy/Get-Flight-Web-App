import unittest
from src.webapp.airport_status import AirportStatus
from src.webapp.airport import Airport
from src.webapp.airport_info_service import AirportInfoService


class TestAirportStatus(unittest.TestCase):
  def setUp(self):
    self.airport_status = AirportStatus()
    self.client = AirportInfoService()

    self.iah = Airport('IAH', 'George Bush Intercontinental')
    self.iad = Airport('IAD', 'Washington Dulles Airport')
    self.ord = Airport('ORD', "Chicago O'Hare")
    self.lax = Airport('LAX', "Los Angeles Intl")


  def test_canary(self):
    self.assertTrue(True)

  def test_sort_no_airport_list(self):
    self.assertEqual([], self.airport_status.sort_airports([]))

  def test_sort_one_airport_list(self):
    self.assertEqual([self.iah],
      self.airport_status.sort_airports([self.iah]))

  def test_sort_two_airport_list_already_sorted(self):
    self.assertEqual([self.iah, self.iad],
      self.airport_status.sort_airports([self.iah, self.iad]))

  def test_sort_two_airport_list_not_sorted(self):
    self.assertEqual([self.iah, self.iad],
      self.airport_status.sort_airports([self.iad, self.iah]))

  def test_sort_three_airport_list_not_sorted(self):
    self.assertEqual([self.ord, self.iah, self.iad],
      self.airport_status.sort_airports([self.iah, self.iad, self.ord]))

  def service_stub(self, code):
    codes = {'IAH': self.iah, 'IAD': self.iad, 'ORD': self.ord,
      'LAX': self.lax}

    if code == 'LAX':
      raise Exception
      
    return codes[code]

  def test_get_airport_name_from_airport_code_when_list_is_empty(self):
    self.assertEqual(([], []),
      self.airport_status.get_airports_status([], self.service_stub))

  def test_get_one_airport_name_from_airport_code(self):
    self.assertEqual(([self.iad], []),
      self.airport_status.get_airports_status(['IAD'], self.service_stub))

  def test_get_two_airport_names_by_request_of_airport_codes(self):
    self.assertEqual(([self.iah, self.iad], []),
      self.airport_status.get_airports_status(['IAH', 'IAD'],
      self.service_stub))

  def test_get_sorted_two_airport_names_by_request_of_airport_codes(self):
    self.assertEqual(([self.iah, self.iad], []),
      self.airport_status.get_airports_status(['IAD', 'IAH'],
      self.service_stub))

  def test_get_sorted_three_airport_names_by_request_of_airport_codes(self):
    self.assertEqual(([self.ord, self.iah, self.iad], []),
      self.airport_status.get_airports_status(['IAH', 'IAD', 'ORD'],
      self.service_stub))

  def test_get_airport_with_invalid_code(self):
    self.assertEqual(([], ['XYZ']),
      self.airport_status.get_airports_status(['XYZ'],
      self.service_stub))

  def test_get_two_airport_with_second_code_invalid(self):
    self.assertEqual(([self.iah], ['XYZ']),
      self.airport_status.get_airports_status(['IAH', 'XYZ'],
      self.service_stub))

  def test_get_three_airport_with_second_code_invalid(self):
    self.assertEqual(([self.ord, self.iah], ['XYZ']),
      self.airport_status.get_airports_status(['IAH', 'XYZ', 'ORD'],
      self.service_stub))

  def test_get_tree_airport_with_first_invalid_third_network_error(self):
    self.assertEqual(([self.iah], ['XYZ', 'LAX']),
      self.airport_status.get_airports_status(['XYZ', 'IAH', 'LAX'],
      self.service_stub))

if __name__ == '__main__':
  unittest.main()
