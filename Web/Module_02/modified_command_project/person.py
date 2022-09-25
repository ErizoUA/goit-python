class Person:
    """
    A class is used to create fields to address book.
    ________________________________________________

    Attributes
    __________
    name : str
        name of the contact
    address : str
        address of the contact
    phone : str
        phone of the contact
    email : str
        email of the contact
    birthday : str
        birthday of the contact
    """

    def __init__(self,
                 name: str = None,
                 address: str = None,
                 phone: str = None,
                 email: str = None,
                 birthday: str = None):
        """
        Creating fields of the address book
        :param name: str
            name of the contact
        :param address: str
            address of the contact
        :param phone: str
            phone of the contact
        :param email: str
            email of the contact
        :param birthday: str
            birthday of the contact
        """
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.birthday = birthday

    def __str__(self):
        """
        Returning all data of the contact as a string
        """

        return f"{self.name}, {self.address}, {self.phone}, {self.email}, {self.birthday}"
