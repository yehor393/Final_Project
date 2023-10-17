from Final_Project.command_parser import parse_input, bot_config
from Final_Project.classes import AddressBook

# tuple of commands to close the bot
close_app = ('exit', 'good bye', 'close') 


def main():
    while True:
        if not bot_config():
            print("There is no configuration file. Can not work without it! Good bye!")
            break
        user_input = input("your command (type 'guide' to display list of available commands): ").lower()

        result = parse_input(user_input) 
        if result is not None: 
            print(result) 
        if user_input.startswith(close_app):
            break

if __name__ == "__main__":
    main()
