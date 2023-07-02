from calendar import monthrange, isleap
from datetime import datetime


def within_one_year(d1, d2):
    """ includes leap years """
    pass

def generate_date_from_string(date_str):
    """ Expects a string with format YYYY-MM-DD. returns datetime.date """
    pass

def read_text_file(filepath):
    with open(filepath, "r") as plaintext_file:
        file_content_str = plaintext_file.read()
    return file_content_str


def convert_string_to_datetime(input: str): #-> datetime.datetime:
    """Parse a string into a datetime object"""
    pass


def convert_string_to_date(input: str): # -> datetime.date:
    """Parse a string into a date object"""
    pass


def validate_date(date):
    pass