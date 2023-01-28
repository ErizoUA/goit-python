from abc import ABC, abstractmethod
from typing import List

from rich.console import Console
from rich.table import Table


console = Console()


class IPrint(ABC):

    @abstractmethod
    def print_table(self, *args):
        ...


class ViewAllAddressBook(IPrint):

    def __init__(self, data: List):
        self.data = data

    def print_table(self):
        table = Table(show_header=True,
                      header_style="bold blue", show_lines=True)
        table.add_column("#", style="dim", width=3, justify="center")

        table.add_column('NAME', style="yellow", min_width=15, justify="center")
        table.add_column('ADDRESS', style="yellow", min_width=15, justify="center")
        table.add_column('PHONE', style="yellow", min_width=15, justify="center")
        table.add_column('EMAIL', style="yellow", min_width=15, justify="center")
        table.add_column('BIRTHDAY', style="yellow", min_width=15, justify="center")

        for index, person in enumerate(self.data, start=1):
            row = []
            row.append(str(index))
            print(person)
            name, address, phone, email, birthday = person

            try:
                birthday = birthday.strftime('%Y-%m-%d')
            except AttributeError:
                birthday = None

            row.append(name)
            row.append(address)
            row.append(phone)
            row.append(email)
            row.append(birthday)
            table.add_row(*row)

        console.print(table)
