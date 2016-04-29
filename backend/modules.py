"""
Project: flask-rest
Author: Saj Arora
Description: Initializes all the modules in the My Clinic app
"""
import re
from flask_restful import reqparse
from google.appengine.ext import deferred

# import storm_data
from api.v1 import SageResource, SageString, SageGravatar, SageJson, SageKey, SageController, make_json_ok_response, \
    SageMethod, SageDateTime, SageInteger, SageFloat, SageText, SageComputed
from api.v1.sage_modules import SageAccountModule, SageAuthModule

account_module = SageAccountModule()
auth_module = SageAuthModule(account_module)
import unicodedata

class Validators(object):
    @classmethod
    def convert_to_float(cls, value, prop=None):
        try:
            return float(re.sub("[^0-9|^.]", "", value))
        except:
             return 0.0

    @classmethod
    def convert_to_int(cls, value, prop=None):
        try:
            return int(re.sub("[^0-9]", "", value))
        except:
            return 0

def population_module():
    return SageResource(
        uid='population_module',
        name='populations',
        model_dict={
            "year": SageInteger(validator_name='convert_to_int'),
            "state": SageString(),
            "state_fips": SageInteger(required=True, validator_name='convert_to_int'),
            "hd_index": SageFloat(validator_name='convert_to_float'),
            "life_expectancy": SageFloat(validator_name='convert_to_float'),
            "median_earning": SageInteger(validator_name='convert_to_int'),
            "health_index": SageFloat(validator_name='convert_to_float'),
            "education_index": SageFloat(validator_name='convert_to_float'),
            "income_tax": SageFloat(validator_name='convert_to_float'),
            "diabetes_adult": SageFloat(validator_name='convert_to_float'),
            "children_in_poverty": SageFloat(validator_name='convert_to_float'),
            "seniors_in_poverty": SageFloat(validator_name='convert_to_float'),
            "low_ses_students": SageFloat(validator_name='convert_to_float'),
            "high_graduates_enrolling_in_college": SageFloat(validator_name='convert_to_float'),
            "public_spending_higher_education": SageFloat(validator_name='convert_to_float'),
            "public_spending_research": SageFloat(validator_name='convert_to_float'),
            "home_internet_access_level": SageFloat(validator_name='convert_to_float'),
            "total_population": SageInteger(validator_name='convert_to_int'),
            "population_under_18": SageFloat(validator_name='convert_to_float'),
            "population_oer_65": SageFloat(validator_name='convert_to_float'),
            "urban_population": SageFloat(validator_name='convert_to_float'),
            "rural_population": SageFloat(validator_name='convert_to_float'),
            "white_not_latino_population": SageFloat(validator_name='convert_to_float'),
            "latino_population": SageFloat(validator_name='convert_to_float'),
            "african_american_population": SageFloat(validator_name='convert_to_float'),
            "asian_american_population": SageFloat(validator_name='convert_to_float'),
            "native_american_population": SageFloat(validator_name='convert_to_float'),
            "foreclure_level": SageFloat(validator_name='convert_to_float'),
            "total_homeless_population": SageInteger(validator_name='convert_to_int'),
            "homelessness_level": SageFloat(validator_name='convert_to_float'),
            "public_spending_on_transport": SageInteger(validator_name='convert_to_int'),
            "infant_mortality_rate": SageFloat(validator_name='convert_to_float'),
            "low_birth_weight_level": SageFloat(validator_name='convert_to_float'),
            "child_mortality_level": SageFloat(validator_name='convert_to_float'),
            "food_insecure_household_level": SageFloat(validator_name='convert_to_float'),
            "chld_immunization_rate": SageFloat(validator_name='convert_to_float'),
            "adult_obesity_level": SageFloat(validator_name='convert_to_float'),
            "teenage_birth_level": SageFloat(validator_name='convert_to_float'),
            "physician_level": SageFloat(validator_name='convert_to_float'),
            "smoking_level": SageFloat(validator_name='convert_to_float'),
            "binge_drinking_level": SageFloat(validator_name='convert_to_float'),
            "uninsured_level": SageFloat(validator_name='convert_to_float'),
            "medicare_insured_level": SageFloat(validator_name='convert_to_float'),
            "mediacaid_insured_level": SageFloat(validator_name='convert_to_float'),
            "total_army_recruits": SageInteger(validator_name='convert_to_int'),
            "violent_crime_level": SageInteger(validator_name='convert_to_int'),
            "property_crime_level": SageInteger(validator_name='convert_to_int'),
            "homicide_level": SageFloat(validator_name='convert_to_float'),
            "state_police_expenditure_level": SageInteger(validator_name='convert_to_int'),
            "total_prisoners": SageInteger(validator_name='convert_to_int'),
            "incarceration_rate": SageInteger(validator_name='convert_to_int'),
            "total_women_in_congression": SageInteger(validator_name='convert_to_int'),
            "total_men_in_congression": SageInteger(validator_name='convert_to_int'),
            "carbon_dioxide_emission_level": SageFloat(validator_name='convert_to_float'),
            "state_per_capita_gdp": SageInteger(validator_name='convert_to_int'),
            "state_minimum_wage": SageFloat(validator_name='convert_to_float')
        },
        validator_dict={
            'convert_to_int': Validators.convert_to_int,
            'convert_to_float': Validators.convert_to_float,
        },
        authenticate=False
    )

def storm_module():
    return SageResource(
        uid='storm_module',
        name='storms',
        model_dict={
            'id': SageInteger(),
            'start_datetime': SageDateTime(required=True),
            'end_datetime':  SageDateTime(required=True),
            'timezone': SageString(),
            'state': SageString(),
            'state_fips': SageString(),
            'year': SageComputed(lambda x: int(x.start_datetime.year),
                                 validator_type=int),
            'month': SageComputed(lambda x: int(x.start_datetime.month),
                                  validator_type=int),
            'day': SageComputed(lambda x: int(x.start_datetime.day),
                                validator_type=int),
            'name': SageString(),
            'type': SageString(),
            'type_code': SageString(),
            'fips': SageString(),
            'direct_injuries': SageInteger(),
            'indirect_injuries': SageInteger(),
            'direct_deaths': SageInteger(),
            'indirect_deaths': SageInteger(),
            'property_damage': SageFloat(),
            'crops_damage': SageFloat(),
            'magnitude': SageFloat(),
            'magnitude_type': SageString(),
            'tor_f_scale': SageString(),
            'tor_length': SageString(),
            'tor_width': SageString(),
            'latitude': SageString(),
            'longitude': SageString(),
            'has_geo': SageComputed(lambda x: True if x.latitude and x.longitude else False,
                                    validator_type=bool),
            'description': SageText()
        },
        authenticate=False
    )


def parse_fxn(self, **kwargs):
    parser = reqparse.RequestParser()
    parser.add_argument('year', type=int, required=True)
    args = parser.parse_args()
    # deferred.defer(storm_data.parse_storm_details, storm_module, args.get('year'))
    return make_json_ok_response(dict(method='parsing...'))


parse_events = SageResource(
    'event_parser_module',
    'parser',
    controllers={
        '': SageController(parse_fxn, SageMethod.POST)
    },
    authenticate=False
)