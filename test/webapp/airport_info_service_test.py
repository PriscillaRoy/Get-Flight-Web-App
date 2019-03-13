import unittest
from unittest.mock import patch
from src.webapp.airport import Airport
from src.webapp.airport_info_service import AirportInfoService


class TestAirportInfoService(unittest.TestCase):
  def setUp(self):
    self.airport_info_service = AirportInfoService()
    self.json_data = '{"Name": "George Bush Intercontinental", ' \
                     '"City": "Houston", "State":"TX", "IATA": "IAH",	"Delay": false,' \
                     ' "Weather":{"Temp": ["64.0 F (17.8 C)"]}}'

    self.invalid_json = '{"SupportedAirport":false,"Delay":false,"DelayCount":0,' \
                        '"Status":[{"Type":"","AvgDelay":"","ClosureEnd":"",' \
                        '"ClosureBegin":"","MinDelay":"","Trend":"","MaxDelay":"","EndTime":""}]}'

  def test_canary(self):
    self.assertTrue(True)

  def test_get_json_returns_json_from_service(self):
    self.assertTrue('"City":"Houston"' in self.airport_info_service.get_JSON('IAH'))

  def test_verify_airport_has_all_attributes(self):
    airport = self.airport_info_service.create_airport(self.json_data)

    self.assertEqual('IAH', airport.code)
    self.assertEqual('George Bush Intercontinental', airport.name)
    self.assertEqual('Houston', airport.city)
    self.assertEqual('TX', airport.state)
    self.assertEqual(['64.0 F (17.8 C)'], airport.temperature)
    self.assertFalse(airport.delay)

  def test_exception_when_given_JSON_has_no_name(self):
    with self.assertRaises(Exception):
      self.airport_info_service.create_airport(self.invalid_json)

  def test_fetch_data_calls_get_JSON(self):
    with patch.object(AirportInfoService, 'get_JSON', return_value = self.json_data) as mocked_method:
      self.airport_info_service.fetch_data('IAH')

    mocked_method.assert_called_with('IAH')


  def test_fetch_data_calls_create_airport(self):
    with patch.object(AirportInfoService, 'get_JSON') as mocked_get_JSON:
      with patch.object(AirportInfoService, 'create_airport') as mocked_create_airport:
        mocked_get_JSON.return_value = self.json_data
        self.airport_info_service.fetch_data('IAH')

    mocked_create_airport.assert_called_with(self.json_data)


  def test_fetch_data_returns_airport_from_create_airport(self):
    sample_airport = Airport("XYZ", "sample airport")
    
    with patch.object(AirportInfoService, 'get_JSON') :
      with patch.object(AirportInfoService, 'create_airport') as mocked_create_airport:
        mocked_create_airport.return_value = sample_airport
        response = self.airport_info_service.fetch_data('XYZ')
    
    self.assertEqual(response, sample_airport)


  def test_fetch_data_propagate_create_airport_exception(self):
    with patch.object(AirportInfoService, 'get_JSON'):
      with patch.object(AirportInfoService, 'create_airport') as mocked_method:
        mocked_method.side_effect = Exception

        with self.assertRaises(Exception):
          self.airport_info_service.fetch_data('IAH')


  def test_fetch_data_propagate_get_JSON_exception(self):
    with patch.object(AirportInfoService, 'get_JSON') as mocked_method:
      mocked_method.side_effect = Exception

      with self.assertRaises(Exception):
        self.airport_info_service.fetch_data('IAH')


if __name__ == '__main__':
  unittest.main()
