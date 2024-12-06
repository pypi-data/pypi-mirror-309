import unittest
import json
from typing import Dict
from country_types import AdditionalCountryInfoTypes
from country_info import PyCountryInfo

class TestPyCountryInfo(unittest.TestCase):
    def setUp(self) -> None:
        pycountryinfo = PyCountryInfo()
        self.countries_list = pycountryinfo.countries_list
        
    
    def test_additional_countries_properties(self):
        additional_countries:Dict[AdditionalCountryInfoTypes] | None = None
        with open("../data/additional_countries_data.json", 'r') as file:
            additional_countries = json.load(file)
            
        for _country in self.countries_list:
            assert 'provinces' in additional_countries[_country['common_name']], f"{_country['common_name']} in additional countries data has no 'provinces' property"
            assert 'area_geometry' in additional_countries[_country['common_name']], f"{_country['common_name']} in additional countries data has no 'area_geometry' property"            
            
    def test_countries_properties(self):
        for _country in self.countries_list:
            assert 'common_name' in _country, f"{_country['common_name']} has no 'common_name' property"
            assert 'official_name' in _country, f"{_country['common_name']} has no 'official_name' property"
            assert 'iso_codes' in _country, f"{_country['common_name']} has no 'iso_codes' property"
            assert 'region' in _country, f"{_country['common_name']} has no 'region' property"
            assert 'subregion' in _country, f"{_country['common_name']} has no 'subregion' property"
            assert 'capital' in _country, f"{_country['common_name']} has no 'capital' property"
            assert 'languages' in _country, f"{_country['common_name']} has no 'languages' property"
            assert 'population' in _country, f"{_country['common_name']} has no 'population' property"
            assert 'area' in _country, f"{_country['common_name']} has no 'area' property"
            assert 'currency' in _country, f"{_country['common_name']} has no 'currency' property"
            assert 'timezones' in _country, f"{_country['common_name']} has no 'timezones' property"
            assert 'borders' in _country, f"{_country['common_name']} has no 'borders' property"
            assert 'alt_spellings' in _country, f"{_country['common_name']} has no 'alt_spellings' property"
            assert 'calling_code' in _country, f"{_country['common_name']} has no 'calling_code' property"
            assert 'translations' in _country, f"{_country['common_name']} has no 'translations' property"
            assert 'gini_index' in _country, f"{_country['common_name']} has no 'gini_index' property"
            assert 'independent' in _country, f"{_country['common_name']} has no 'independent' property"
            assert 'latlng' in _country, f"{_country['common_name']} has no 'latlng' property"
            assert 'nationality' in _country, f"{_country['common_name']} has no 'nationality' property"
            assert 'flag' in _country, f"{_country['common_name']} has no 'flag' property"
            assert 'wiki' in _country, f"{_country['common_name']} has no 'wiki' property"
            assert 'provinces' in _country, f"{_country['common_name']} has no 'provinces' property"
            assert 'area_geometry' in _country, f"{_country['common_name']} has no 'area_geometry' property"
    
    
    def test_example_country_properties(self):
        pycountryinfo = PyCountryInfo('Ghana')
        assert pycountryinfo.country_data['common_name']
        assert pycountryinfo.country_data['official_name']
        assert pycountryinfo.country_data['iso_codes']
        assert pycountryinfo.country_data['region']
        assert pycountryinfo.country_data['subregion']
        assert pycountryinfo.country_data['capital']
        assert pycountryinfo.country_data['languages']
        assert pycountryinfo.country_data['population']
        assert pycountryinfo.country_data['area']
        assert pycountryinfo.country_data['currency']
        assert pycountryinfo.country_data['timezones']
        assert pycountryinfo.country_data['borders']
        assert pycountryinfo.country_data['alt_spellings']
        assert pycountryinfo.country_data['calling_code']
        assert pycountryinfo.country_data['translations']
        assert pycountryinfo.country_data['gini_index']
        assert pycountryinfo.country_data['independent']
        assert pycountryinfo.country_data['latlng']
        assert pycountryinfo.country_data['nationality']
        assert pycountryinfo.country_data['flag']
        assert pycountryinfo.country_data['provinces']
        assert pycountryinfo.country_data['area_geometry']
    
    
if __name__ == '__main__':
    unittest.main()   
        
        