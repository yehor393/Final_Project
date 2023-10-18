from command_parser import parse_input, bot_config
from classes import AddressBook

# tuple of commands to close the bot
close_app = ('exit', 'good bye', 'close') 


def main():
    if not bot_config():
        print("There is no configuration file. Can not work without it! Good bye!")
        return
    while True:
        user_input = input("your command (type 'guide' to display list of available commands): ").lower()

        result = parse_input(user_input) 
        if result is not None: 
            print(result) 
        if result == "Good bye!":
            break

if __name__ == "__main__":
    main()
