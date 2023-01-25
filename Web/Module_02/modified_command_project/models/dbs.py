from abc import ABC, abstractmethod
from datetime import datetime
import os
import pickle

from .custom_exceptions import WrongNameFormat
from .fields import Name, Phone, Address, Birthday, Email
from .fields import NoteText, Tag
from .note import Note
from .person import Person
from .print_interface import ViewAllAddressBook, PrintPerson, PrintNotes


class IDB(ABC):

    @abstractmethod
    def db_load(self):
        ...

    @abstractmethod
    def db_save(self, new_db):
        ...


class AddressBook(IDB):
    def __init__(self, database):
        self.database = database
        self.persons = {}

    def db_load(self):
        if not os.path.exists(self.database):
            file = open(self.database, 'wb')
            pickle.dump({}, file)
            file.close()
        else:
            with open(self.database, 'rb') as db:
                dict_db = pickle.load(db)
                self.persons = dict_db

    def db_save(self, new_persons):
        self.persons.update(new_persons)
        file = open(self.database, 'wb')
        pickle.dump(self.persons, file)
        file.close()

    def add(self):
        """
        Adding contact to the address book with fields: name, address, phone, email, birthday
        """
        name, address, phone, email, birthday = self.get_details()

        if name.value not in self.persons:
            person = Person(name, address, phone, email, birthday)
            self.persons[name.value] = person

            return self.persons

        else:
            print("Contact already exist")

    @staticmethod
    def get_details():

        while True:
            name = input("Name: ")
            try:
                name = Name(name)
            except WrongNameFormat as e:
                print(e)
                continue
            else:
                break

        address = input("Address: ")
        if address:
            address = Address(address)

        phone = input("Phone: ")
        if phone:
            phone = Phone(phone)

        email = input("Email: ")
        if email:
            email = Email(email)

        birthday = input("Birthday [format yyyy-mm-dd]: ")
        if birthday:
            birthday = Birthday(birthday)

        return name, address, phone, email, birthday

    def find_by_name(self):
        """
        Searching contact in address book by name and printing found record as a formatted table
        """
        name = input("Enter the searching name: ")
        if name in self.persons:
            PrintPerson.print_table(self.persons[name])

        else:
            print("Contact not found")

    def search(self):
        """
        Searching contact in address book by any field and printing found contacts as a formatted table
        """
        count = 0
        obj = input('What do you want to find? ')

        for contact in self.persons.values():
            if obj.lower() in str(contact).lower():
                count += 1
                PrintPerson.print_table(contact)

        if count == 0:
            print('No matches found')
        else:
            print(f'Found {count} matches')

    def update(self):
        """
        Updating record in address book. You can change one field or all ones immediately
        """
        dict_name = input("Enter the name: ")
        print(dict_name)
        if dict_name in self.persons:
            print("Found. Enter new details and keep empty fields if no any changes")
            name, address, phone, email, birthday = self.get_details()

            name = name or self.persons[dict_name]["name"]
            address = address or self.persons[dict_name]["address"]
            phone = phone or self.persons[dict_name].phone
            email = email or self.persons[dict_name].email
            birthday = birthday or self.persons[dict_name].birthday
            self.persons[dict_name].__init__(
                name, address, phone, email, birthday)
            print("Address book successfully updated")
        else:
            print("Contact not found")

    def get_birthdays(self):
        """
        Printing contacts which have birthday in defined period
        """
        # gap_days = int(input("Enter timedelta for birthday: "))
        gap_days = 7
        current_date = datetime.now()
        result = {}

        for name in self.persons:
            bday = datetime.strptime(self.persons[name].birthday.value, '%Y-%m-%d')
            try:
                mappedbday = bday.replace(year=current_date.year)
            except ValueError:
                # 29 February cannot be mapped to non-leap year. Choose 28-Feb instead
                mappedbday = bday.replace(year=current_date.year, day=28)

            if 0 <= (mappedbday - current_date).days < gap_days:
                try:
                    result[mappedbday.strftime('%A')].append(name)
                except KeyError:
                    result[mappedbday.strftime('%A')] = [name]
            elif current_date.weekday() == 0:
                if -2 <= (mappedbday - current_date).days < 0:
                    try:
                        result[current_date.strftime('%A')].append(name)
                    except KeyError:
                        result[current_date.strftime('%A')] = [name]

        for day, names in result.items():
            print(f"{', '.join(names)} has birthday on {day}")

    def view(self):
        """
        Printing whole address book as a formatted table
        """
        if self.persons:
            ViewAllAddressBook(list(self.persons.values())).print_table()
        else:
            print("No match contacts in database")

    def delete(self):
        """
        Deleting record in address book by name
        """
        name = input("Enter the name to delete: ")
        if name in self.persons:
            del self.persons[name]
            print("Deleted the contact")
        else:
            print("Contact not found in the app")

    def reset(self):
        """
        Deleting all records in address book
        """
        self.persons = {}


class Diary(IDB):
    def __init__(self, database):
        self.database = database
        self.notes = {}

    def db_load(self):
        if not os.path.exists(self.database):
            file = open(self.database, 'wb')
            pickle.dump({}, file)
            file.close()
        else:
            with open(self.database, 'rb') as db:
                dict_db = pickle.load(db)
                self.notes = dict_db

    def db_save(self, new_notes):
        self.notes.update(new_notes)
        file = open(self.database, 'wb')
        pickle.dump(self.notes, file)
        file.close()

    def add(self):
        """
        Adding record to diary with fields note & keywords.
        """
        text, keywords = self.get_note()
        note = Note(text=NoteText(text), tag=Tag(keywords))
        self.notes[note.id] = note

        return self.notes

    def search(self):
        """
        Searching note by text or keyword and printing found notes as a formatted table
        """
        text = input("What are you looking for?: ")
        note_list = []
        for note in self.notes.values():
            if text in (note.text.value + ' '.join(note.tag.value)):

                note_list.append(note)

            else:
                print(f"no notes with such text '{text}' or tag '{text}'")

        PrintNotes.print_table(note_list, "#")

    @staticmethod
    def get_note():

        text = input('NoteText:').strip()
        keywords = input('Keywords:').strip().split(' ')

        return text, keywords

    def view(self):
        """
        Printing all notes as a formatted table
        """
        if self.notes:
            PrintNotes.print_table(list(self.notes.values()), "#")
        else:
            print("No match notes in database")

    def update(self):
        """
        Amending notes and keywords by searching keyword

        """
        note_id = input("Enter the ID to note: ")

        if note_id in self.notes:
            text, keywords = self.get_note()
            self.notes[note_id] = Note(text=NoteText(text), tag=Tag(keywords))

    def delete(self):
        """
        Deleting notes by keyword
        """
        note_id = input("Enter note ID: ")
        if note_id in self.notes:
            del self.notes[note_id]
            print("Deleted the note")
        else:
            print("note not found in the diary")

    def reset(self):
        """
        Deleting all notes in diary
        """
        self.notes = {}
