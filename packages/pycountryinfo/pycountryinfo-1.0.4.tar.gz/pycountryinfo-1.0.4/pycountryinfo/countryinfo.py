import json
from typing import List, Dict, Tuple
from .country_types import CountryInfoTypes
from importlib.resources import files

class PyCountryInfo:
    def __init__(self, country:str = ""):
        self.country_name_type:str = 'common'
        self.countries_list:List[CountryInfoTypes] | None = None
        if self.country_name_type not in ['common', 'official']:
            raise ValueError("Invalid country name type. Use 'common' or 'official'.")
        
        try:
            countries_file = files('pycountryinfo.data').joinpath('countries.json')
            with countries_file.open('r') as file:
                self.countries_list = json.load(file)
        except FileNotFoundError:
            raise ValueError("The countries data file is missing.")
        except json.JSONDecodeError:
            raise ValueError("The countries data file is not in a valid JSON format.")
        
        if not self.countries_list:
            raise ValueError("The countries data is empty or invalid.")
        
        self.name_key = 'common_name' if self.country_name_type == 'common' else 'official_name'
        self.countries_dict: Dict[str, CountryInfoTypes] = {item[self.name_key].title(): item for item in self.countries_list}
        self.country = country
        self.country_data:CountryInfoTypes | None = self.countries_dict.get(self.country.title()) 
        if self.country and not self.country_data:
            raise ValueError(f"{country} is not a valid country name. If you are using the country's official name, make sure you set the 'country_name_type' argument to 'official'.")
        
        self.nationalities:Tuple[str, ...] | None = None
        self.countries:Tuple[str, ...] | None = None
            
    def validate_country(self, country: str) -> CountryInfoTypes:
        country_data = self.countries_dict.get(country.title())
        if not country_data:
            raise ValueError(f"{country} is not a valid country name. If you are using the country's official name, make sure you set the 'country_name_type' argument to 'official'.")
        return country_data
        
    def get_nationality(self, country:str) -> str:
        return self.validate_country(country).get('nationality')
    
    def get_nationalities(self) -> Tuple[str, ...]:
        if not self.nationalities:
            self.nationalities = tuple(item['nationality'] for item in self.countries_list)
        return self.nationalities

    def is_valid_country_nationality(self, country:str, nationality:str) -> bool:
        return nationality == self.validate_country(country).get('nationality')
    
    def is_valid_nationality(self, nationality:str) -> bool:
        return nationality in self.get_nationalities()

    def get_country_from_nationality(self, nationality:str) -> str:
        country = next((item[self.name_key] for item in self.countries_list if nationality == item['nationality']), None)
        if not country:
            raise ValueError(f"{nationality} is not a valid nationality")
        return country

    def get_countries(self) -> Tuple[str, ...]:
        if not self.countries:
            self.countries = tuple(item[self.name_key] for item in self.countries_list)
        return self.countries

    def is_valid_country(self, country:str) -> bool:
        return country.title() in self.countries_dict
    
    def get_provinces(self, country:str) -> List[str]:
        return self.validate_country(country).get('provinces')

    def is_valid_country_province(self, country:str, province:str) -> bool:
        return province in self.get_provinces(country)
    


