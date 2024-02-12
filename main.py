'''Data storage'''
import pickle
from classes import AddressBook, Record

book = AddressBook()
file_name = 'Contacts.pickle'

def input_error(func):
    '''Decorator for working with exeptions'''
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError:
            result = 'User not found'
        except ValueError:
            result = 'Phone number incorrect'
        except IndexError:
            result = 'One of parameters missed'
        return result
    return inner


def main():
    '''Main function to work with user input'''
    try:
        with open(file_name, 'rb') as file:
            data = pickle.load(file)
            book.data = data
    except:
        print('Empty AdressBook')

    while True:
        command = input()
        exit_list = ['exit', 'close', 'good bye']
        if command in exit_list:
            try:
                with open(file_name, 'wb') as file:
                    pickle.dump(book.data, file)
            except:
                print("I couldn't save record")
            print('Good bye!')
            break
        print(parser(command))

def parser(user_input):
    '''Function define key words (user commands)'''
    if user_input.lower().startswith('hello'):
        return 'How can I help you?'
    if user_input.lower().startswith('add '):
        return handler_add(user_input)
    if user_input.lower().startswith('change '):
        return handler_change(user_input)
    if user_input.lower().startswith('phone '):
        return handler_phone(user_input)
    if user_input.lower().startswith('show all'):
        return handler_show_all(user_input)
    if user_input.lower().startswith('search'):
        return handler_search(user_input)
    return 'No comand recognize'


@input_error
def handler_add(user_input):
    '''Function define actions if user command is "add"'''
    _, name, phone = user_input.split(' ')
    record = book.find(name)
    if not record:
        record = Record(name)
    record.add_phone(phone)
    book.add_record(record)

    return 'User added succesfully!'

@input_error
def handler_change(user_input):
    '''Function define actions if user command is "change"'''
    user_data = user_input.split(' ')
    check_phone_number(user_input)
    if user_data[1] in user_data_dict:
        user_data_dict.update({user_data[1] : user_data[2]})
        return 'User updated succesfully!'
    raise KeyError

@input_error
def handler_phone(user_input):
    '''Function define actions if user command is "phone"'''
    user_data = user_input.split(' ')
    user_phone = user_data_dict.get(user_data[1])
    return f'User phone number is: {user_phone}'

@input_error
def handler_show_all(user_input):
    '''Function define actions if user command is "show all"'''
    users_data = list(book.data.values())
    return ', '.join(map(str, users_data))

@input_error
def handler_search(user_input):
    _, text = user_input.split()
    users_data = book.search(text)
    return ', '.join(map(str, users_data))

if __name__ == '__main__':
    main()
