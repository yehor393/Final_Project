from collections.abc import Iterator
from error_handl_decorator import error_handling_decorator
from error_handl_decorator import CustomError
from collections import UserDict
import re
import datetime
import pickle

# classes
class Field:
    def __init__(self, value):
        self._value = None
        self.value = value
    
    def __str__(self):
        return self.value

    @property
    def value(self) -> str:
        return self._value


class Name(Field):
    @Field.value.setter
    def value(self, new_value: str):
        if new_value.isalpha():
            self._value = new_value
        else:
            raise CustomError("please provide valid name")


class Phone(Field):
    def __init__(self, value):
        super().__init__(str(value))
    
    @Field.value.setter
    def value(self, new_value: str):
        if new_value.isdigit() or new_value==None:
            self._value = new_value
        else:
            raise CustomError("phone number should contain digits only")


class Birthday(Field):
    def __init__(self, value): 
        super().__init__(value)
    
    @Field.value.setter
    def value(self, new_value: str):
        # check of birthday format
        if not re.match(r'\d{4}-\d{2}-\d{2}', new_value):
            raise CustomError("please enter a valid birthdate in the format YYYY-MM-DD")

        # convert to datetime format
        try:
            date_value = datetime.datetime.strptime(new_value, "%Y-%m-%d")
        except:
            raise CustomError("please enter a valid birthdate in the format YYYY-MM-DD")
        
        # check the date correctness
        if not (1900 <= date_value.year <= datetime.date.today().year and
                    1 <= date_value.month <= 12 and
                    1 <= date_value.day <= 31):
                raise CustomError("please enter a valid birthdate in the format YYYY-MM-DD")
        dob = date_value.date()
        self._value = dob
    

class Email(Field):
    def __init__(self, value):
        super().__init__(str(value))
    
    @Field.value.setter
    def value(self, new_value: str):
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
            return CustomError("please provide an email in the correct format")
        self._value = new_value


class Address(Field):
    def __init__(self, value):
        super().__init__(str(value))

    @Field.value.setter
    def value(self, new_value: str):
        self._value = new_value


class Note(Field):
    def __init__(self, value):
        super().__init__(str(value))

    @Field.value.setter
    def value(self, new_value: str):
        self._value = new_value


class Record:
    def __init__(self, name, phone=None, birthday=None, email=None, address=None, note=None): 
        self.name = Name(value=name)
        self.phones = []
        if phone:
            self.add_new_phone(phone)
        if birthday:
            self.birthday = Birthday(value=birthday)
        if email:
            self.email = Email(value=email)
        if address:
            self.address = Address(value=address)
        if note:
            self.note = Note(value=note)

    def days_to_birthday(self):
        current_date = datetime.date.today()
        next_birthday = datetime.date(current_date.year, self.birthday.value.month, self.birthday.value.day)
        
        if current_date > next_birthday:
            next_birthday = datetime.date(current_date.year + 1, self.birthday.value.month, self.birthday.value.day)
            
        days_until_birthday = (next_birthday - current_date).days

        return days_until_birthday

    def add_new_phone(self, phone): 
        self.phones.append(Phone(value=phone))

    def amend_phone(self, name, new_phone, old_phone): 
        phone_found = False
        for stored_phone in self.phones.copy():
            if str(stored_phone) == old_phone:
                self.phones.remove(stored_phone)
                self.add_new_phone(new_phone)
                phone_found = True

        if not phone_found:
            raise CustomError("phone number was not found")

    def remove_phone(self, phone):
        phone_found = False
        for stored_phone in self.phones.copy():
            if str(stored_phone) == phone:
                self.phones.remove(stored_phone)
                phone_found = True

        if not phone_found:
            raise CustomError("phone number was not found")


phone_book_file = r'./phone_book'


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        try:
            with open(phone_book_file, "rb") as fh:
                deserialized_book = pickle.load(fh)
            self.data = deserialized_book
        except:
            pass

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self, n): # n-number of records per page. is defined in show_page function
        contacts_per_page = n
        contacts = list(self.data.keys())
        index = 0

        while index < len(contacts):
            yield contacts[index:index + contacts_per_page]
            index += contacts_per_page

phone_book = AddressBook()


# parser
#@error_handling_decorator
def parse_input(user_input):
    for request in commands:  # commands: hello, search, show all, contact, add, remove, change
        if user_input.startswith(request):
            func = commands[request]

            if func == add_contact:
                name = input('please provide contact name: ')
                new_phone_number = input('please provide the new phone number: ') 
                birth_date = input('please provide a bithday in a format YYYY-MM-DD: ')
                email = input('please provide an email: ')
                address = input('please provide an address: ')
                note = input('please provide a note: ')
                return func(name, new_phone_number, birth_date, email, address, note)
            
            elif func == show_contact:
                name = input('please provide a contact name: ')
                return func(name)
            
            elif func == change_phone:
                name = input('please provide a contact name: ')
                new_phone_number = input('please provide the new phone number: ') 
                old_phone_number = input('please provide the phone number to be replaced: ')
                return func(name, new_phone_number, old_phone_number)
            
            elif func == show_all:
                return func()
            
            elif func == show_page:
                page = input('please provide the page to display: ')
                return func(page)
            
            elif func == remove_contact:
                name = input('please provide a contact name you want to remove: ')
                return func(name)

            elif func == remove_info: 
                name = input('please provide a contact name to delete information from: ')
                info_to_delete = input('what type of information will be deleted (phone / birthday / email / address / note): ')
                if info_to_delete == 'phone':
                    phone_number = input('please provide a phone number to delete: ')
                    return func(name, info_to_delete, phone_number)
                
                return func(name, info_to_delete)
            
            elif func == hello:
                return func()
            
            elif func == search:
                search_word = input('please provide a search request: ')
                return func(search_word)
            
            elif func == dtb:
                name = input('please provide a contact name: ')
                birth_date = input('please provide a bithday in a format YYYY-MM-DD: ')
                return func(name, birth_date) 

        
    raise CustomError("please provide a valid command")


# adding new contact/phone number
def add_contact (name, phone=None, birthday=None, email=None, address=None, note=None): 
    if not name:  
        raise CustomError("please provide a name")
    elif name not in phone_book:
        record = Record(name, phone, birthday, email, address, note)
        phone_book.add_record(record)
        return "new contact successfully added"
    else:
        record = phone_book[name]

        if phone:
            record.add_new_phone(phone)
        if birthday:
            record.birthday = Birthday(value=birthday)
        if email:
            record.email = Email(value=email)
        if address:
            record.address = Address(value=address)
        if note:
            record.note = Note(value=note)

        return "new information successfully added to existing contact"


# change the phone number
def change_phone (name, new_phone, old_phone):
    if name not in phone_book:
        raise CustomError('a name was not found')
    if not new_phone or not old_phone:
        raise CustomError("please provide a name, a new number and an old number divided by a space")
    
    record = phone_book[name]
    record.amend_phone(name, new_phone, old_phone)
    return "contact successfully changed"

def remove_contact(name):
    if name not in phone_book:
        raise CustomError('name not found')
    
    del phone_book[name]
    return "the contact successfully removed"

def remove_info(name, field_to_remove, phone=None):
    if name not in phone_book:
        raise CustomError('name not found')
    
    record = phone_book[name]
    if phone:
        record.remove_phone(phone)
        return "the phone number successfully removed"
    elif field_to_remove == 'birthday':
        if hasattr(record, 'birthday'):
            del record.birthday
            return "the birthday successfully removed"
        else:
            raise CustomError("no birthday exist for this contact")
        
    elif field_to_remove == 'email':
        if hasattr(record, 'email'):
            del record.email
            return "the email successfully removed"
        else:
            raise CustomError("no email exist for this contact")
    
    elif field_to_remove == 'address':
        if hasattr(record, 'address'):
            del record.address
            return "the address successfully removed"
        else:
            raise CustomError("no address exist for this contact")
    elif field_to_remove == 'note':
        if hasattr(record, 'note'):
            del record.note 
            return "the note successfully removed" 
        else:
            raise CustomError("no note exist for this contact")


# show contact details of user
def show_contact (name): 
    if name not in phone_book:
        raise CustomError("please provide a valid name")
    
    record = phone_book[name]
    phone_numbers = []
        
    for item in record.phones:
        phone_numbers.append(item.value)

    if len(phone_numbers) > 0:
        phone_str = f"{', '.join(phone_numbers)}"
    else:
        phone_str = 'no phone numbers'

    if hasattr(record, 'birthday'):
        birthday_str = record.birthday.value.strftime('%Y-%m-%d')
    else:
        birthday_str = 'no birthday recorded'
    
    if hasattr(record, 'email'):
        email_str = record.email.value
    else:
        email_str = 'no email recorded'

    if hasattr(record, 'address'):
        address_str = record.address.value
    else:
        address_str = 'no address recorded'

    if hasattr(record, 'note'):
        note_str = record.note.value
    else:
        note_str = 'no note recorded'

    return f"{name}: {phone_str}, {birthday_str}, {email_str}, {address_str}, {note_str}"


# show all contacts info
def show_all():
    contacts = []
    for record in phone_book:
        one_contact = show_contact(record)
        contacts.append(one_contact)
    if contacts:
        return ';\n'.join(contacts)
    else:
        raise CustomError("phone book is empty")


def show_page(page):
    try:
        page_number = int(page)
        contacts_per_page = 2

        if page_number < 1:
            raise CustomError("pages start from 1")

        contact_batches = list(phone_book.iterator(contacts_per_page))

        if page_number <= len(contact_batches):
            contacts = contact_batches[page_number - 1]
            return ';\n'.join([show_contact(contact) for contact in contacts])
        else:
            raise CustomError("page not found")

    except ValueError:
        raise CustomError("invalid page number")


def hello():
    return("How can I help you? Please type your command")


def search (search_word):
    result= []
    for name, record in phone_book.items():
        if len(record.phones) > 0:
            phone_numbers = ', '.join(phone.value for phone in record.phones)
        else:
            phone_numbers = 'no phone numbers recorded'
        try:
            birthday_str = record.birthday.value.strftime('%Y-%m-%d')
        except AttributeError:
            birthday_str = "no birthday recorded"

        
        if (search_word in name) or (search_word in phone_numbers) or (search_word == birthday_str) or (search_word in record.note.value):
            result.append(show_contact(name))
            

    if result:
        return ';\n'.join(result)
    else:
        raise CustomError("nothing found")


def dtb(name,notused=None, notused2=None, notused3=None):
    if name not in phone_book:
        raise CustomError("please provide a valid name")
    
    record = phone_book[name]
    if not hasattr(record, 'birthday'):
            raise CustomError ("no birthday recorded")
    return record.days_to_birthday()


commands = {
    "add": add_contact,
    "contact": show_contact,
    "change": change_phone,
    "show all": show_all,
    "page": show_page,
    "remove field": remove_info,
    "remove contact": remove_contact,
    "hello": hello,
    "search": search,
    "dtb": dtb,
}

