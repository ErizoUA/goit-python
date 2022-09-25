from datetime import datetime


class Note:
    """
    A class is used to create fields to diary.
    ________________________________________________

    Attributes
    __________
    value : str
        text of the note
    keyWords : list
        a keywords list of the note
    date : datetime
        date of note creating

    Methods
    _______
    print_in_table
        used to show info about the note as a table

    """
    def __init__(self, value: str, key_words: list) -> None:
        """
        Creating fields of the diary
        :param value: str
            text of the note
        :param key_words: list
            a keywords list of the note
        """
        self.date = datetime.now().isoformat()
        self.value = value
        self.keyWords = key_words

    def get_keywords(self):
        """
        Joining all tags of the note in string
        :return: str
            string of keywords
        """
        return ", ".join(self.keyWords)

    def __str__(self):
        return "{:<25} {}".format(datetime.fromisoformat(self.date).strftime("%m/%d/%Y, %H:%M:%S"), self.value)
