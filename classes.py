'''Class system for address book management'''
from collections import UserDict
from datetime import datetime, date

class Field:
    '''A class representing a field with a value.'''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    @property
    def value(self):
        '''Get the current value of the field.'''
        return self.__value

    @value.setter
    def value(self, new_value):
        '''Set the value of the field.'''
        if self.is_valid(new_value):
            self.__value = new_value
        else:
            raise ValueError

    def is_valid(self, value):
        '''Check if a value is valid for the field.'''
        return True


class Birthday(Field):
    '''A class representing a birthday field.'''
    def is_valid(self, value):
        '''Check if a value is a valid birthday.'''
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False


class Name(Field):
    '''A class representing a name field.'''
    # реалізація класу


class Phone(Field):
    '''A class representing a phone number field.'''
    # реалізація класу
    def is_valid(self, value):
        return len(value) == 10 and value.isdigit()

class Record:
    '''A class representing a contact record.'''
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.phones = []

    def add_birthday(self, birthday):
        '''Add a birthday to the contact.'''
        self.birthday = Birthday(birthday)
        return self.birthday

    def add_phone(self, phone:str):
        '''Add a phone number to the contact.'''
        phone_object = Phone(phone)
        self.phones.append(phone_object)
        return phone_object

    def days_to_birthday(self):
        '''Calculate the number of days until the next birthday.'''
        if self.birthday is None:
            return None
        date_of_birth = datetime.strptime(self.birthday.value, '%Y-%m-%d')
        new_date = date_of_birth.replace(year=date.today().year)
        result = new_date - date.today()
        if result.days < 0:
            new_date = date_of_birth.replace(year=date.today().year+1)
            result = new_date - date.today()
        return result.days

    def remove_phone(self, phone:str):
        '''Remove a phone number from the contact.'''
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return p
        return None

    def edit_phone(self, phone:str, new_phone):
        '''Edit a phone number in the contact.'''
        Phone(new_phone)
        for i in self.phones:
            if i.value == phone:
                i.value = new_phone
                return i
        raise ValueError

    def find_phone(self, phone:str):
        '''Find a phone number in the contact.'''
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None

    def __str__(self):
        return f"Contact name: {str(self.name)}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {str(self.birthday)}"

class AddressBook(UserDict):
    '''A class for storing and managing records.'''
    # реалізація класу
    def add_record(self, record):
        '''Add a record to the address book.'''
        self.data[record.name.value] = record

    def find(self, name):
        '''Find a record by name.'''
        return self.data.get(name, None)

    def delete(self, name):
        '''Delete a record by name.'''
        if name in self.data:
            return self.data.pop(name)
        return None

    def iterator(self, n):
        '''Generate an iterator over records with batch size n.'''
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i:i+n]


if __name__ == '__main__':
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
