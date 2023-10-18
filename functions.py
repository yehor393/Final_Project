from error_handl_decorator import CustomError
from classes import *
from input_format_verification import *
import difflib  # matches library
from notebook import *
from pathlib import Path
import main_sorting_files
from twilio.rest import Client
from user_config import Config
from gen_config import *

config = Config(CONFIG_FILE)
notes = NoteBook()

# Luda


def view_notes():
    message = ""
    for note in notes.values():
        message += "\n" + str(note) + "\n"
    if not message:
        message = "You have no notes yet"
    return message


def add_note(text: str, tags: str) -> str:
    tag_list = str_to_tags(tags)
    note = Note(text, tag_list)
    notes.add_note(note)
    return "Note was successfully added"


def delete_note(id: str) -> str:
    notes.delete_note(id)
    return "Note was successfully removed"


def edit_text(id: str, new_text: str) -> str:
    note = notes.find_id(id)
    note.edit_text(new_text)
    notes.save()
    return "Note was successfully edited"


def add_tags(id: str, tags: str) -> str:
    tag_list = str_to_tags(tags)
    note = notes.find_id(id)
    note.add_tags(tag_list)
    notes.save()
    return f"Tags were successfully added to the note with id {id}"


def delete_tag(id: str, tag: str) -> str:
    note = notes.find_id(id)
    note.remowe_tag(tag)
    notes.save()
    return "Tags were successfully deleted"


def find_by_tag(tags: str, show_desc: bool) -> str:
    intersec = " and " in tags
    tags = tags.replace(" and ", " ").replace(" or ", " ")
    tag_list = []
    tag_list.extend(tags.split(" "))
    for i in range(len(tag_list)):
        if not tag_list[i].startswith("#"):
            tag_list[i] = "#" + tag_list[i]

    result = notes.find_by_tag(tag_list, intersec, show_desc)

    message = ""
    for note in result:
        message += "\n" + str(note) + "\n"
    if not message:
        message = "Nothing found. Correct search conditions."
    return message


def input_note_params(param: str):
    correct = False
    value = ""
    while not correct:
        if param == "id":
            value = input('Please provide a note id: ')
            correct = value in notes

        elif param == "text":
            print('Please write your note here (double enter to finish): ')
            value = []
            while True:
                new_text = input()
                if not new_text:
                    break
                value.append(new_text)
            value = '\n'.join(value)
            correct = value != ""

        elif param == "tag":
            value = input('Please provide a tag: ')
            correct = value in notes.tag_cloud

        elif param == "tags":
            value = input('Please provide tags separated with spaces: ')
            correct = value != ""

        elif param == "show_desc":
            value = input("Show newest on the top (Y/N)? ")
            value = value.lower() == "y"
            correct = True

        if not correct:
            print("Incorrect data. Try again")

    return value


def str_to_tags(text: str) -> [str]:
    tags = []
    for tag in text.split(" "):
        if not tag:
            continue
        if not tag.startswith("#"):
            tag = "#" + tag
        tags.append(tag)
    return tags


# parameter cutoff regulates sensitivity for matching, 1.0 - full match, 0.0 - input always matches
def find_closest_match(user_input, commands):
    closest_match = difflib.get_close_matches(
        user_input, commands, n=1, cutoff=0.6)
    if closest_match:
        return closest_match[0]
    else:
        return None


def check_command(user_input, commands):
    if user_input in commands:
        return user_input

    closest_match = find_closest_match(user_input, commands)
    if closest_match:
        print(closest_match)
        return closest_match
    else:
        return user_input


# adding new contact/phone number
def add_contact(name, phone=None, birthday=None, email=None, address=None, note=None):
    if not name:
        raise CustomError("Please provide a name")
    elif name not in phone_book:
        record = Record(name, phone, birthday, email, address, note)
        phone_book.add_record(record)
        return "New contact successfully added"
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

        return "New information successfully added to the existing contact"


def change_info():  # does not do any actions, for correct functionality of commands only
    pass

# change the phone number


def change_phone(name, new_phone, old_phone):

    if not new_phone or not old_phone:
        raise CustomError(
            "Please provide a name, a new number and an old number separated by a space")

    record = phone_book[name]
    record.amend_phone(name, new_phone, old_phone)
    return "Contact successfully changed"


def remove_contact(name):

    del phone_book[name]
    return "Contact successfully removed"


def remove_info(name, field_to_remove, phone=None):

    record = phone_book[name]
    if phone:
        record.remove_phone(phone)
        return "Phone number successfully removed"

    elif field_to_remove == 'birthday':
        if hasattr(record, 'birthday'):
            del record.birthday
            return "Birthday successfully removed"
        else:
            raise CustomError("No birthday exist for this contact")

    elif field_to_remove == 'email':
        if hasattr(record, 'email'):
            del record.email
            return "Email successfully removed"
        else:
            raise CustomError("No email exist for this contact")

    elif field_to_remove == 'address':
        if hasattr(record, 'address'):
            del record.address
            return "Address successfully removed"
        else:
            raise CustomError("No address exist for this contact")

    elif field_to_remove == 'note':
        if hasattr(record, 'note'):
            del record.note
            return "Note successfully removed"
        else:
            raise CustomError("No note exist for this contact")


# show contact details of user
def show_contact(name):

    record = phone_book[name]
    phone_numbers = []

    for item in record.phones:
        phone_numbers.append(item.value)

    if len(phone_numbers) > 0:
        phone_str = f"{', '.join(phone_numbers)}"
    else:
        phone_str = 'No phone numbers'

    if hasattr(record, 'birthday'):
        birthday_str = record.birthday.value.strftime('%Y-%m-%d')
    else:
        birthday_str = 'No birthday recorded'

    if hasattr(record, 'email'):
        email_str = record.email.value
    else:
        email_str = 'No email recorded'

    if hasattr(record, 'address'):
        address_str = record.address.value
    else:
        address_str = 'No address recorded'

    if hasattr(record, 'note'):
        note_str = record.note.value
    else:
        note_str = 'No note recorded'

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
        raise CustomError("Phone book is empty")


def show_page(page):
    try:
        page_number = int(page)
        contacts_per_page = int(config["contacts_per_page"])

        if page_number < 1:
            raise CustomError("Pages start from 1")

        contact_batches = list(phone_book.iterator(contacts_per_page))

        if page_number <= len(contact_batches):
            contacts = contact_batches[page_number - 1]
            return ';\n'.join([show_contact(contact) for contact in contacts])
        else:
            raise CustomError("Page not found")

    except ValueError:
        raise CustomError("Invalid page number")


def hello():
    return ("How can I help you? Please type your command")


def search(search_word):
    result = []
    for name, record in phone_book.items():
        if len(record.phones) > 0:
            phone_numbers = ', '.join(phone.value for phone in record.phones)
        else:
            phone_numbers = 'No phone numbers recorded'
        try:
            birthday_str = record.birthday.value.strftime('%Y-%m-%d')
        except AttributeError:
            birthday_str = "No birthday recorded"

        try:
            note_str = record.note.value
        except AttributeError:
            note_str = "No note recorded"

        if (search_word in name) or (search_word in phone_numbers) or (search_word == birthday_str) or (search_word in note_str):
            result.append(show_contact(name))

    if result:
        return ';\n'.join(result)
    else:
        raise CustomError("Nothing found")


def dtb(name):
    record = phone_book[name]
    if not hasattr(record, 'birthday'):
        raise CustomError("No birthday recorded")
    return record.days_to_birthday()


# shows upcoming birthdays/
def show_birthdays_soon(days):
    result = []
    for name, record in phone_book.items():
        days_until_birthday = record.days_to_birthday()

        if days_until_birthday is not None and days_until_birthday == days:
            result.append(show_contact(name))
    if result:
        return ';\n'.join(result)
    else:
        raise CustomError(
            "There are no birthdays for the specified number of days")


def guide():
    try:
        with open(config["help_file"], 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        raise CustomError("File not found")


def sort_files(folder_path):
    main_sorting_files.main(Path(folder_path))


def send_sms(phone_number, message):
    if "account_sid" not in config or\
            "auth_token" not in config:
        return "There option are not configured"

    account_sid = config["account_sid"]
    auth_token = config["auth_token"]

    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            from_=config["account_phone"],
            body=message,
            to=phone_number)
        message = f"Message was successfully sended on number {phone_number}!"
    except Exception as e:
        raise CustomError(f"{e.args[2]}. Check your calling settings.")
    return message


def call(phone_number, message):
    if "account_sid" not in config or\
            "auth_token" not in config:
        return "There option are not configured"

    account_sid = config["account_sid"]
    auth_token = config["auth_token"]
    client = Client(account_sid, auth_token)
    try:
        message = client.calls.create(
            twiml=f'<Response><Say>{message}</Say></Response>',
            to=phone_number,
            from_=config["account_phone"],
            machine_detection="DetectMessageEnd",
            machine_detection_timeout=0
        )
        message = f"Call on number {phone_number} was successfully doned!"
    except Exception as e:
        raise CustomError(f"{e.args[2]}. Check your calling settings.")

    return message


def bot_config():
    if not config.data:
        return False
    if not "contacts_per_page" in config or not config["contacts_per_page"].isdecimal():
        config["contacts_per_page"] = input_config("contacts_per_page")

    if not "user_folder" in config or not create_folder(config["user_folder"]):
        config["user_folder"] = input_config("user_folder")

    notes.file_name = Path(config["user_folder"], config["notebook_file"])
    phone_book.file_name = Path(
        config["user_folder"], config["addressbook_file"])

    config.save_config()
    return True


def input_config(param: str):
    correct = False
    value = ""
    while not correct:
        if param == "user_folder":
            value = input(
                "Please enter path to folder where all data will be stored: ")
            correct = create_folder(value)
            response = "Path does not exist!"
        if param == "contacts_per_page":
            value = input(
                "Please enter how many contacts per page do you want to see: ")
            correct = value.isdecimal()
            response = "It should be a positive decimal value"
        if not correct:
            print(response)

    return value


def create_folder(user_string: str) -> bool:
    path = Path(user_string)
    try:
        path.mkdir(exist_ok=True)
        return True
    except:
        return False


def close_bot():
    phone_book.save_changes()
    return "Good bye!"


commands = {
    "add": add_contact,
    "contact": show_contact,
    "change field": change_info,
    "show all": show_all,
    "page": show_page,
    "remove field": remove_info,
    "remove contact": remove_contact,
    "hello": hello,
    "search": search,
    "dtb": dtb,
    "sbs": show_birthdays_soon,
    "guide": guide,
    "view notes": view_notes,
    "new note": add_note,
    "delete note": delete_note,
    "edit text": edit_text,
    "delete tag": delete_tag,
    "new tags": add_tags,
    "sort files": sort_files,
    "sms": send_sms,
    "call": call,
    "find tags": find_by_tag,
    "config": bot_config,
    "good bye": close_bot,
    "close": close_bot,
    "exit": close_bot,
}
