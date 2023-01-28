from mongoengine import Document, StringField, connect, DateTimeField

connect(db='assistant', host='mongodb://localhost:27017')


class Contact(Document):
    name = StringField(required=True, unique=True)
    address = StringField(max_length=100)
    phone = StringField()
    email = StringField()
    birthday = DateTimeField()
