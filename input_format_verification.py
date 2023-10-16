import datetime
import re
from classes import phone_book

def name_input():
    def name_validation(name):
        if name not in phone_book:
            return False
        else: 
            return name
        
    while True:
        input_name = input('Please provide a contact name: ')
        name =  name_validation(input_name)
        if name:
            return name
        else:
            print("Please provide a valid name. Try again")

def dob_input():
    def birthday_format_check (birth_date):
        if not birth_date:
            return birth_date
        
        else:
        
            if not re.match(r'\d{4}-\d{2}-\d{2}', birth_date):
                return False
            
            # convert to datetime format
            try:
                date_value = datetime.datetime.strptime(birth_date, "%Y-%m-%d")
            except:
                return False
                
            # check the date correctness
            if not (1900 <= date_value.year <= datetime.date.today().year and
                    1 <= date_value.month <= 12 and
                    1 <= date_value.day <= 31):
                return False
        
            return date_value

    while True:
        input_birth_date = input('Please provide a bithday in a format YYYY-MM-DD: ')
        dob = birthday_format_check(input_birth_date)
        if dob != False:
            return dob
            
        else: 
            print("Please enter a valid birthdate in the format YYYY-MM-DD. Try again")


def email_input():
    def email_format_check (email):
        if not email:
            return email
        
        elif not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
            return False
        
        return email

    while True:
        input_email = input('Please provide an email: ')
        email = email_format_check(input_email)

        if email != False:
            return email
            
        else: 
            print("Please provide an email in the correct format. Try again")


def phone_input():
    def phone_format_check (phone_number):
        if not phone_number:
            return phone_number
        
        elif not re.match(r'\+\d+$', phone_number):
            return False
        
        else:
            return phone_number
        
    while True:
        input_phone = input('please provide an a phone number: ')
        phone = phone_format_check(input_phone)
        if phone != False:
            return phone
        else:
            print("Phone number should start with + and contain digits only. Try again")