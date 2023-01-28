from datetime import datetime

from .fields import NoteText, Tag


class Note:

    def __init__(self,
                 text: NoteText = None,
                 tag: Tag = None):
        self.date = datetime.now().isoformat()
        self.text = text
        self.tag = tag
        self.id = datetime.now().strftime('%Y%m%d%H%M')

    def __str__(self):
        return "{:<25} {}".format(datetime.fromisoformat(self.date).strftime("%m/%d/%Y, %H:%M:%S"), self.id, self.text,
                                  self.tag)
