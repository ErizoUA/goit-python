from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)
    birthday = Column(Date, nullable=True)
    contacts = relationship('ContactPerson', backref='person')


class ContactPerson(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    address = Column('address', String(100), nullable=True)
    phone = Column('phone', String(100), nullable=True)
    email = Column('email', String(100), nullable=True)
    person_id = Column('person_id', ForeignKey('persons.id', ondelete='CASCADE'), nullable=False)
