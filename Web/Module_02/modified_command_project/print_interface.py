from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List

from rich.console import Console
from rich.table import Table

from person import Person


console = Console()


class IPrint(ABC):

    @abstractmethod
    def print_table(self, *args):
        ...


class PrintPerson(IPrint):

    def print_table(self: Person):
        """
        Printing data of the contact as a formatted table
        :return: None
        """
        table = Table(show_header=False,
                      header_style="bold blue", show_lines=True)

        table.add_row(
            f'[cyan]{self.name}[/cyan]', f'[cyan]{self.address}[/cyan]', f'[cyan]{self.phone}[/cyan]',
            f'[cyan]{self.email}[/cyan]', f'[cyan]{self.birthday}[/cyan]'
        )
        console.print(table)


class ViewAllAddressBook(IPrint):

    def print_table(self: Dict[str, Person]):

        table = Table(show_header=True,
                      header_style="bold blue", show_lines=True)
        table.add_column("#", style="dim", width=3, justify="center")
        table.add_column("NAME", min_width=12, justify="center")
        table.add_column("ADDRESS", min_width=10, justify="center")
        table.add_column("PHONE", min_width=18, justify="center")
        table.add_column("EMAIL", min_width=18, justify="center")
        table.add_column("BIRTHDAY", min_width=15, justify="center")
        for idx, person in enumerate(self.values(), start=1):
            _ = person.__dict__
            table.add_row(
                str(idx), f'[cyan]{_["name"]}[/cyan]',
                f'[cyan]{_["address"]}[/cyan]', f'[cyan]{_["phone"]}[/cyan]',
                f'[cyan]{_["email"]}[/cyan]', f'[cyan]{_["birthday"]}[/cyan]'
            )
        console.print(table)


class PrintNotes(IPrint):

    def print_table(self: List, table_name: str):
        """
        Printing notes as a formatted table
        :param : list
            list of the selected notes
        :param table_name: str
            name of the formatted table
        :return: None
         """

        table = Table(show_header=True,
                      header_style="bold blue", show_lines=True)
        table.add_column(table_name, style="dim",
                         width=5, justify="center")
        table.add_column("DATE", min_width=12, justify="center")
        table.add_column("VALUE", min_width=50, justify="center")

        for idx, note in enumerate(self, start=1):
            table.add_row(str(
                idx), f'[cyan]{datetime.fromisoformat(note.date).strftime("%m/%d/%Y, %H:%M:%S")}[/cyan]',
                f'[cyan]{note.value}[/cyan]')

        console.print(table)
