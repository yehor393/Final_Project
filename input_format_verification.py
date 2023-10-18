import datetime
import re
from classes import phone_book
from country_codes import country_codes
import os

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
    def phone_format_check(phone_number):
        if not phone_number:
            return None
        if re.match(r'^\+\d+$', phone_number):
            return phone_number
        else:
            print("Invalid phone format. The number must start with "+". Please try again.")
            return None

    while True:
        input_phone = input('Please provide an phone: ')
        phone = phone_format_check(input_phone)
        if phone:
            phone_digits = re.sub(r'[^\d]', '', phone)
            found_country = None
            for country, code in country_codes.items():
                if phone_digits.startswith(code):
                    found_country = country
                    break
            if found_country:
                print(f"Phone number of : {found_country}")
                return phone
            else:
                print("Country code unknown . Please try again.")

def path_input():
    def path_check(path):
        if not os.path.exists(path):
            return False
        else:
            return path

    while True:
        input_path = input("Enter the path to the folder containing unorganized files: ")
        folder_path = path_check(input_path)
        if folder_path != False:
            return folder_path
        else:
            print("Provided path is not valid. Try again") 