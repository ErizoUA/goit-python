from datetime import datetime
import os
import pickle
import re

from tools import validator
from tools import sorting

from person import Person
from note import Note
from print_interface import PrintPerson
from print_interface import PrintNotes
from print_interface import ViewAllAddressBook


CLI_UI = '''
CMD HELPER: 1.Add 2.View all 3.Search 4.Find 5.Sort 6.Update 7.Delete 8.Reset 9.File sort 10. Help 11.Exit
'''


class AddressBook:
    """
    This class manages elements of address book & diary.
    """

    def __init__(self, database):
        self.database = database
        self.persons = {}
        self.notes = {}
        if not os.path.exists(self.database):
            file_pointer = open(self.database, 'wb')
            pickle.dump({}, file_pointer)
            file_pointer.close()
        else:
            with open(self.database, 'rb') as Application:
                dict_application = pickle.load(Application)
                self.persons = dict_application.get("persons", self.persons)
                self.notes = dict_application.get("notes", self.notes)

    def add(self):
        """
        Adding record to the address book with fields: name, address, phone, email, birthday
        """
        name, _address, _phone, _email, _birthday = self.get_details()
        address = _address or "NULL"
        phone = _phone or "NULL"
        email = _email or "NULL"
        birthday = _birthday or "1900-01-01"
        if name not in self.persons:
            self.persons[name] = Person(name, address, phone, email, birthday)
        else:
            print("Contact already present")

    def add_note(self):
        """
        Adding record to diary with fields note & keywords.
        Keywords are written down together with note, each keyword is enclosed on both sides by symbol #
        """
        value, key_words = self.get_note()
        note = Note(value, key_words)
        self.notes[note.date] = note

    def view_all(self):
        """
        Printing whole address book as a formatted table
        """
        if self.persons:
            ViewAllAddressBook.print_table(self.persons)
        else:
            print("No match contacts in database")

    def view_all_notes(self):
        """
        Printing all notes as a formatted table
        """
        if self.notes:
            PrintNotes.print_table(self.notes.values(), "#")
        else:
            print("No match notes in database")

    def search(self):
        """
        Searching record in address book by name and printing found record as a formatted table
        """
        name = input("Enter the name: ")
        if name in self.persons:
            PrintPerson.print_table(self.persons[name])
        else:
            print("Contact not found")

    def search_notes(self):
        """
        Searching note by text or keyword and printing found notes as a formatted table
        """
        keyword = input("What are you looking for?: ")
        note_list_keyword = []
        note_list = []
        for note in self.notes.values():
            keywords = note.get_keywords()
            if keyword in keywords:
                note_list_keyword.append(note)

            if note not in note_list_keyword and keyword in str(note):
                note_list.append(note)

        if note_list_keyword or note_list:
            if note_list_keyword:
                PrintNotes.print_table(note_list_keyword, "by key")

            if note_list:
                PrintNotes.print_table(note_list, "by text")

        else:
            print(f"no notes with key word {keyword}")

    def find(self):
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

    @staticmethod
    def get_details():
        """
        Getting info for fields in address book from user
        :return: tuple
            fields of address book: name, address, phone, email, birthday
        """
        name = validator.name_validator()
        address = input("Address: ")
        phone = validator.phone_check()
        email = validator.email_check()
        birthday = input("Birthday [format yyyy-mm-dd]: ")
        return name, address, phone, email, birthday

    @staticmethod
    def get_note():
        """
        Getting note and keywords from user
        :return: tuple
            1st element: note
            2nd element: list of the keywords
        """
        user_input = input("Note (keywords as #words#): ")
        keywords = re.findall(r"#.+#", user_input)
        value = user_input.strip()
        return value, [keyword.replace("#", "").strip() for keyword in keywords]

    def update(self):
        """
        Updating record in address book. You can change one field or all ones immediately
        """
        dict_name = input("Enter the name: ")
        if dict_name in self.persons:
            print("Found. Enter new details and keep empty fields if no any changes")
            _name, _address, _phone, _email, _birthday = self.get_details()
            name = _name or self.persons[dict_name]["name"]
            address = _address or self.persons[dict_name]["address"]
            phone = _phone or self.persons[dict_name]["phone"]
            email = _email or self.persons[dict_name]["email"]
            birthday = _birthday or str(self.persons[dict_name]["birthday"])
            self.persons[dict_name].__init__(
                name, address, phone, email, birthday)
            print("Address book successfully updated")
        else:
            print("Contact not found")

    def update_notes(self):
        """
        Amending notes and keywords by searching keyword
        """
        keyword = input("Enter the key word to note: ")
        noteskey_to_update = []
        for noteKey in self.notes:
            if keyword in self.notes[noteKey].keyWords:
                self.notes[noteKey].print_in_table()
                print("Will be changed")
                value, key_words = self.get_note()
                self.notes[noteKey].key_words = key_words
                self.notes[noteKey].value = value
                noteskey_to_update.append(noteKey)

        if not noteskey_to_update:
            print(f"no notes with key word {keyword}")

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

    def delete_notes(self):
        """
        Deleting notes by keyword
        """
        keyword = input("Enter the key word to note: ")
        noteskey_to_del = []
        for noteKey in self.notes:
            if keyword in self.notes[noteKey].keyWords:
                self.notes[noteKey].print_in_table()
                print("Was deleted")
                noteskey_to_del.append(noteKey)

        if noteskey_to_del:
            for notekey in noteskey_to_del:
                self.notes.pop(notekey)
        else:
            print(f"no notes with key word {keyword}")

    def reset(self):
        """
        Deleting all records in address book
        """
        self.persons = {}

    def reset_notes(self):
        """
        Deleting all notes in diary
        """
        self.notes = {}

    def get_birthdays(self):
        """
        Printing contacts which have birthday in defined period
        """
        gap_days = int(input("Enter timedelta for birthday: "))
        current_date = datetime.now()
        result = {}

        for name in self.persons:
            bday = self.persons[name]["birthday"]
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
            print(f"Start reminder on {day}: {', '.join(names)}")
        return result

    @classmethod
    def help(cls):
        """
        I'm a personal assistant. I'm able to keep an address book & a diary, to sort files.
        You can use next functions:
        """
        functions = {'add': cls.add,
                     'add_note': cls.add_note,
                     'view_all': cls.view_all,
                     'view_all_notes': cls.view_all_notes,
                     'search': cls.search,
                     'search_notes': cls.search_notes,
                     'find': cls.find,
                     'update': cls.update,
                     'update_notes': cls.update_notes,
                     'delete': cls.delete,
                     'delete_notes': cls.delete_notes,
                     'reset': cls.reset,
                     'reset_notes': cls.reset_notes,
                     'sort_birthday': cls.get_birthdays,
                     'file_sort': sorting.perform
                     }
        for name, function in functions.items():
            print(name)
            print(f'\t{function.__doc__}')

    def __del__(self):
        with open(self.database, 'wb') as db:
            pickle.dump({"persons": self.persons, "notes": self.notes}, db)

    def __str__(self):
        return CLI_UI
